# Portfolio asset optimization

Use Python 3.11+, install Pillow, then run `python scripts/optimize-assets.py`. It creates `optimized-site/`, refuses to overwrite an existing output, keeps source untouched and generates a WebP display image. Review image fidelity and all links before deploying the output directory. PNG source is retained.

The optimized binary is not committed by this text-only PR. Generating a copy is not a deployment. The HTML patch only adds async decoding and high fetch priority to the hero image.
