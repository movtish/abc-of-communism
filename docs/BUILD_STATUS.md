# Building the PDFs

The repository includes both manuscript PDFs. To rebuild them, install Tectonic 0.17.0 and run from the repository root.

```sh
python scripts/build_articles.py --tectonic /path/to/tectonic
```

The first build downloads TeX packages and fonts. Once cached, they can be reused with `--offline`. Build files go to `build/`; finished PDFs go to `paper/` and `jnea/`. `validation/article_pdf_build.json` records the PDF hashes and the sources used in each build.

The Russian manuscript uses OpenType Tempora with XeTeX. Its pdfLaTeX branch uses T2A fonts.

To rebuild the English notes, run the following commands.

```sh
python -m pip install -r requirements-docs.txt
python scripts/build_docs.py
```

For the Russian article, regenerate tables and figures after calculating the main results.

```sh
python scripts/jnea2_tables.py
python scripts/jnea2_figures.py
```
