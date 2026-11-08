# Building the documents

The manuscript PDFs are included. Building them requires Tectonic 0.17.0.

```sh
python scripts/build_articles.py --tectonic /path/to/tectonic
```

The first run downloads the required TeX packages. Later runs can use `--offline`. Intermediate files go under `build/`; the PDFs are copied to `paper/` and `jnea/`. PDF and source hashes are recorded in `validation/article_pdf_build.json`.

The Russian manuscript uses the OpenType Tempora fonts with XeTeX and the T2A setup with pdfLaTeX.

To regenerate the supplementary notes, install `requirements-docs.txt` and run `python scripts/build_docs.py`. To regenerate the Russian tables and figures, run `python scripts/jnea2_tables.py` and `python scripts/jnea2_figures.py` after the main number calculation.
