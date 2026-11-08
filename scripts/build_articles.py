"""Compile the English and Russian manuscripts with Tectonic."""

from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = "https://data1b.fullyjustified.net/tlextras-2022.0r0.tar"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_sha256(path):
    data = path.read_bytes()
    if path.suffix in {".tex", ".bib"}:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def build(engine, language, offline):
    folder, stem = {
        "en": ("paper", "ABC_of_Communism"),
        "ru": ("jnea", "article_jnea"),
    }[language]
    source = ROOT / folder
    output = ROOT / "build" / folder
    output.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment["TECTONIC_CACHE_DIR"] = str(ROOT / ".tectonic-cache")
    command = [
        str(engine),
        "--bundle",
        BUNDLE,
        "--untrusted",
        "--keep-logs",
        "--keep-intermediates",
        "--outdir",
        str(output),
    ]
    if offline:
        command.append("--only-cached")
    command.append(stem + ".tex")
    subprocess.run(command, cwd=source, env=environment, check=True)
    pdf = output / (stem + ".pdf")
    if not pdf.is_file():
        raise FileNotFoundError(pdf)
    shutil.copyfile(pdf, source / pdf.name)
    names = json.loads(
        (ROOT / "validation/manuscript_files.json").read_text(encoding="utf-8")
    )
    inputs = [ROOT / name for name in names if name.startswith(folder + "/")]
    if language == "en":
        inputs.append(ROOT / "paper/refs.bib")
    text = "\n".join(
        p.read_text(encoding="utf-8") for p in inputs if p.suffix == ".tex"
    )
    names = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)
    for name in names:
        candidates = [source / name, source / "figures" / name, ROOT / "figures" / name]
        for candidate in candidates:
            choices = (
                [candidate]
                if candidate.suffix
                else [candidate.with_suffix(ext) for ext in [".pdf", ".png", ".jpg"]]
            )
            match = next((p for p in choices if p.is_file()), None)
            if match:
                inputs.append(match)
                break
    return {
        "language": language,
        "source": (source / (stem + ".tex")).relative_to(ROOT).as_posix(),
        "pdf": (source / pdf.name).relative_to(ROOT).as_posix(),
        "pdf_sha256": sha256(pdf),
        "source_hashes": {
            p.relative_to(ROOT).as_posix(): source_sha256(p)
            for p in sorted(set(inputs))
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tectonic", type=Path)
    parser.add_argument("--language", choices=["en", "ru", "both"], default="both")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    local = ROOT / ".tools" / "tectonic" / "tectonic.exe"
    engine = args.tectonic or (local if local.is_file() else shutil.which("tectonic"))
    if not engine:
        raise SystemExit("Install Tectonic or supply its path with --tectonic.")
    version = subprocess.check_output([str(engine), "--version"], text=True).strip()
    languages = ["en", "ru"] if args.language == "both" else [args.language]
    target = ROOT / "validation" / "article_pdf_build.json"
    articles = (
        {
            item["language"]: item
            for item in json.loads(target.read_text(encoding="utf-8"))["articles"]
        }
        if target.exists()
        else {}
    )
    for lang in languages:
        articles[lang] = build(engine, lang, args.offline)
    record = {
        "engine": version,
        "bundle": BUNDLE,
        "offline": args.offline,
        "articles": [articles[lang] for lang in sorted(articles)],
    }
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
