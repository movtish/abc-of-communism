import numpy as np, pandas as pd, statsmodels.formula.api as smf
from inference import Model


def run():
    rng = np.random.default_rng(812)
    n = 80
    d = pd.DataFrame(
        dict(
            x=rng.normal(size=n),
            z=rng.normal(size=n),
            g=np.repeat(np.arange(10), 8),
            a=np.tile(np.arange(8), 10),
            w=rng.uniform(0.5, 3, n),
        )
    )
    d["y"] = 1 + 0.7 * d.x - 0.3 * d.z + rng.normal(size=n) + d.g / 10 + d.a / 5
    f = "y ~ x + z + C(g) + C(a)"
    m = Model(f, d, "w", "g")
    res = m.evaluate({"x": 1}, bootstrap=63)
    r = smf.wls(f, d, weights=d.w).fit(
        cov_type="cluster", cov_kwds={"groups": d.g}, use_t=True
    )
    assert np.isclose(res["b"], r.params["x"], rtol=1e-9)
    assert np.isclose(res["se_cr1"], r.bse["x"], rtol=1e-9)
    assert np.isclose(res["cr2_working_variance_ratio"], 1, rtol=1e-7)
    # CR2 with singleton clusters is HC2, and the t df is contrast-specific.
    mh = Model("y ~ x + z", d, None, None)
    rh = smf.ols("y ~ x + z", d).fit(cov_type="HC2")
    assert np.isclose(
        mh.evaluate({"x": 1}, jackknife=False)["se_cr2"], rh.bse["x"], rtol=1e-8
    )
    # Check a nonzero restricted null and the full-refit bootstrap against
    # an independent statsmodels fit of each synthetic dependent variable.
    c = m.contrast({"x": 1})
    null = 0.25
    P = m.P
    bread = P @ P.T
    b0 = m.beta - (bread @ c) * ((c @ m.beta - null) / (c @ bread @ c))
    u0 = m.y - m.X @ b0
    obs = (c @ m.beta - null) / res["se_cr1"]
    rng = np.random.default_rng(20261108)
    sgn = rng.choice([-1.0, 1.0], size=(10, 63))
    exc = 0
    for b in range(63):
        ystar = m.X @ b0
        for gi, i in enumerate(m.ix):
            ystar[i] += u0[i] * sgn[gi, b]
        dd = m.d.copy()
        dd["ystar"] = ystar / np.sqrt(dd.w)
        rr = smf.wls("ystar ~ x + z + C(g) + C(a)", dd, weights=dd.w).fit(
            cov_type="cluster", cov_kwds={"groups": dd.g}
        )
        exc += abs((rr.params["x"] - null) / rr.bse["x"]) >= abs(obs) - 1e-12
    assert m.wild(c, null, 63)["wcr_exceed"] == exc
    # A perfectly collinear requested coefficient must not be reported.
    d["xcopy"] = d.x
    try:
        Model("y ~ x + xcopy", d, None, "g").evaluate({"x": 1})
        raise AssertionError("unidentified contrast accepted")
    except ValueError:
        pass
    d["only_g0"] = (d.g == 0).astype(int)
    scarce = Model("y ~ only_g0", d, None, "g").evaluate({"only_g0": 1})
    assert "cr2_unavailable" in scarce and "p_cr2" not in scarce
    assert scarce.get("jackknife_not_identified")
    print(
        "PASS: CR1 vs statsmodels; CR2 vs HC2; restricted WCR vs full refits; estimability guard"
    )


if __name__ == "__main__":
    run()
