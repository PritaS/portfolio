"""Create an optimized static-site copy without changing source files.
Requires Python 3.11+ and Pillow: python -m pip install Pillow
"""
from pathlib import Path
import argparse
import base64
import hashlib
import io
import re
import shutil
from PIL import Image

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=root / 'optimized-site')
args = parser.parse_args()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=False)  # never overwrite an existing site
html = (root / 'index.html').read_text()
for source in root.iterdir():
    if source.is_file() and source.name != 'index.html' and source.suffix.lower() in {'.html', '.png', '.jpg', '.jpeg', '.webp'}:
        shutil.copy2(source, out / source.name)

def encode(image):
    image.thumbnail((1800, 1800))
    buffer = io.BytesIO()
    image.save(buffer, 'WEBP', quality=85, method=6)
    return buffer.getvalue()

profile = root / 'picofme (2).png'
if profile.exists():
    with Image.open(profile) as image:
        image.thumbnail((1000, 1000))
        (out / 'profile.webp').write_bytes(encode(image))
    html = html.replace('picofme (2).png', 'profile.webp')

def externalize(match):
    raw = base64.b64decode(match.group(2), validate=True)
    name = 'assets/images/' + hashlib.sha256(raw).hexdigest()[:16] + '.webp'
    dest = out / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(raw)) as image:
        dest.write_bytes(encode(image))
    return name

html = re.sub(r'data:image/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=]+)', externalize, html)
(out / 'index.html').write_text(html)
print(f'Optimized copy: {out}; source unchanged. Review image fidelity before deployment.')
