# Article PDF build

Both current articles were built on 8 November 2026 with Tectonic 0.17.0 and the TeX Live 2022 bundle. The English PDF includes the online appendix. All pages were rendered and checked. No unresolved references or missing glyphs were found.

The default relay host could not be resolved. The build uses the direct storage URL specified by the Tectonic project's redirect configuration, `https://data1b.fullyjustified.net/tlextras-2022.0r0.tar`. The required packages and fonts are cached locally in `.tectonic-cache/`. The local executable is `.tools/tectonic/tectonic.exe`. These downloaded files are excluded from Git.

```sh
python scripts/build_articles.py --offline
```

For a fresh installation, [download Tectonic](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0), then supply its path and allow the first run to retrieve packages.

```sh
python scripts/build_articles.py --tectonic /path/to/tectonic
```

The Russian article selects the OpenType Tempora fonts under XeTeX. Its pdfLaTeX branch retains the original T2A font setup. This preserves the intended typeface while avoiding lost Cyrillic characters with the Unicode engine. The article content and numerical estimates are unchanged.

The build script writes both PDFs to their manuscript folders, keeps intermediate output under `build/` and records PDF and source hashes in `validation/article_pdf_build.json`. The release checker reports whether those hashes still match the current files.

The older PDFs remain in the local archive. The English methods and evidence notes in `docs/` are separate from the article PDFs.
