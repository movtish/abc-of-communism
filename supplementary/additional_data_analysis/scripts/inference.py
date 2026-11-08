"""Calculate cluster inference for weighted least-squares contrasts.

CR1 uses the design rank and a t distribution with G minus one degrees
of freedom. CR2 uses an identity working covariance after weighting and
contrast-specific Satterthwaite degrees of freedom. The restricted wild
bootstrap imposes a scalar null and refits fixed effects. Population
weights define the estimand; they are not inverse sampling variances."""

import numpy as np
import pandas as pd
import patsy
from scipy import stats


def design(formula, data, weight=None, cluster=None):
    d = data.copy()
    if weight:
        d = d.loc[d[weight].notna() & (d[weight] > 0)]
    if cluster:
        d = d.loc[d[cluster].notna()]
    d = d.reset_index(drop=True)
    y, X = patsy.dmatrices(formula, d, return_type="dataframe", NA_action="drop")
    d = d.loc[X.index].copy()
    sw = np.sqrt(d[weight].to_numpy(float)) if weight else np.ones(len(d))
    return d, y.to_numpy().ravel() * sw, X.to_numpy() * sw[:, None], list(X.columns)


class Model:
    def __init__(self, formula, data, weight=None, cluster=None):
        self.d, self.y, self.X, self.names = design(formula, data, weight, cluster)
        self.n, self.k = self.X.shape
        self.P = np.linalg.pinv(self.X)
        self.rank = np.linalg.matrix_rank(self.X)
        self.beta = self.P @ self.y
        self.u = self.y - self.X @ self.beta
        self.cluster = cluster
        labels = (
            self.d[cluster].astype(str)
            if cluster
            else pd.Series(np.arange(self.n).astype(str))
        )
        self.labels = list(pd.unique(labels))
        self.ix = [np.flatnonzero(np.asarray(labels) == g) for g in self.labels]
        self.G = len(self.ix)
        self.cf = self.G / (self.G - 1) * (self.n - 1) / (self.n - self.rank)

    def contrast(self, terms):
        c = np.zeros(self.k)
        for name, value in terms.items():
            c[self.names.index(name)] = value
        if np.linalg.norm(c - c @ self.P @ self.X) > 1e-7 * max(1, np.linalg.norm(c)):
            raise ValueError("Contrast not identified: " + repr(terms))
        return c

    def evaluate(
        self, terms, cr2=True, jackknife=True, bootstrap=0, seed=20261108, null=0.0
    ):
        c = self.contrast(terms)
        v = c @ self.P
        theta = float(c @ self.beta)
        scores = np.array([v[i] @ self.u[i] for i in self.ix])
        se = float(np.sqrt(self.cf * (scores @ scores)))
        df = self.G - 1 if self.cluster else self.n - self.rank
        p = float(2 * stats.t.sf(abs((theta - null) / se), df)) if se else np.nan
        out = dict(
            n=self.n,
            rank=self.rank,
            clusters=self.G,
            b=theta,
            se_cr1=se,
            p_cr1=p,
            df_cr1=df,
            ci_low_cr1=theta - stats.t.ppf(0.975, df) * se,
            ci_high_cr1=theta + stats.t.ppf(0.975, df) * se,
        )
        s2 = np.array([v[i] @ v[i] for i in self.ix])
        out["effective_clusters_design"] = float(s2.sum() ** 2 / (s2 @ s2))
        if cr2:
            vv = []
            sc = []
            for i in self.ix:
                # Symmetric generalized inverse square root; cluster FE can
                # create null directions, which have zero estimable score.
                H = self.X[i] @ self.P[:, i]
                V = np.eye(len(i)) - (H + H.T) / 2
                ev, U = np.linalg.eigh(V)
                inv = np.zeros_like(ev)
                ok = ev > 1e-9
                inv[ok] = ev[ok] ** -0.5
                a = (U * inv) @ (U.T @ v[i])
                sc.append(a @ self.u[i])
                z = np.zeros(self.n)
                z[i] = a
                z -= self.P.T @ (self.X.T @ z)
                vv.append(z)
            vv = np.asarray(vv)
            C = vv @ vv.T
            df2 = float(np.trace(C) ** 2 / np.sum(C * C))
            se2 = float(np.linalg.norm(sc))
            ratio = float(np.trace(C) / (v @ v))
            out["cr2_working_variance_ratio"] = ratio
            if np.isclose(ratio, 1, rtol=1e-6, atol=1e-7):
                out.update(
                    se_cr2=se2,
                    df_cr2=df2,
                    p_cr2=float(2 * stats.t.sf(abs((theta - null) / se2), df2)),
                    ci_low_cr2=theta - stats.t.ppf(0.975, df2) * se2,
                    ci_high_cr2=theta + stats.t.ppf(0.975, df2) * se2,
                )
            else:
                # A generalized inverse is not a valid bias correction when
                # the target score has mass in an uncorrectable null direction.
                out["cr2_unavailable"] = (
                    "working covariance cannot be reproduced (cluster leverage)"
                )
        if jackknife:
            leave = []
            ident = True
            for i in self.ix:
                mask = np.ones(self.n, bool)
                mask[i] = False
                Xp = self.X[mask]
                Pp = np.linalg.pinv(Xp)
                if np.linalg.norm(c - c @ Pp @ Xp) > 1e-7 * max(1, np.linalg.norm(c)):
                    ident = False
                    break
                leave.append(float(c @ Pp @ self.y[mask]))
            if ident:
                leave = np.asarray(leave)
                sej = float(
                    np.sqrt((self.G - 1) / self.G * np.sum((leave - leave.mean()) ** 2))
                )
                out.update(
                    se_jackknife=sej,
                    p_jackknife=float(2 * stats.t.sf(abs((theta - null) / sej), df)),
                    loo_min=float(leave.min()),
                    loo_max=float(leave.max()),
                    max_loo_shift=float(np.max(abs(leave - theta))),
                )
            else:
                out["jackknife_not_identified"] = True
        if bootstrap:
            out.update(self.wild(c, null, bootstrap, seed, exact=self.G <= 12))
        return out

    def wild(self, c, null=0.0, B=9999, seed=20261108, exact=False):
        v = c @ self.P
        theta = float(c @ self.beta)
        bread = self.P @ self.P.T
        beta0 = self.beta - (bread @ c) * ((theta - null) / (c @ bread @ c))
        fitted = self.X @ beta0
        u0 = self.y - fitted
        observed = (theta - null) / np.sqrt(
            self.cf * sum((v[i] @ self.u[i]) ** 2 for i in self.ix)
        )
        rng = np.random.default_rng(seed)
        exceed = 0
        done = 0
        if exact:
            B = 2**self.G
        # Matrix batches explicitly re-fit the entire nuisance design.
        for lo in range(0, B, 256):
            size = min(256, B - lo)
            if exact:
                sgn = (
                    2
                    * (
                        (
                            np.arange(lo, lo + size, dtype=np.int64)[None, :]
                            >> np.arange(self.G, dtype=np.int64)[:, None]
                        )
                        & 1
                    )
                    - 1
                )
            else:
                sgn = rng.choice([-1.0, 1.0], size=(self.G, size))
            ys = np.tile(fitted[:, None], (1, size))
            for gi, i in enumerate(self.ix):
                ys[i] += u0[i, None] * sgn[gi]
            betas = self.P @ ys
            res = ys - self.X @ betas
            meat = np.zeros(size)
            for i in self.ix:
                meat += (v[i] @ res[i]) ** 2
            ts = (c @ betas - null) / np.sqrt(self.cf * meat)
            exceed += int(np.sum(abs(ts) >= abs(observed) - 1e-12))
            done += size
        return dict(
            wcr_p=exceed / done if exact else (exceed + 1) / (done + 1),
            wcr_exceed=exceed,
            wcr_draws=done,
            wcr_enumerated=bool(exact),
            wcr_t=float(observed),
        )
