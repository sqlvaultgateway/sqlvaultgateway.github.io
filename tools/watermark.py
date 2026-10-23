"""Captures publiques : largeur réduite + filigrane discret « SQLVault Gateway · démonstration ».
Python avec Pillow : python watermark.py source.png sortie.jpg [largeur]"""
import sys
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 1100
im = Image.open(src).convert('RGB')
im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)

layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', max(13, width // 64))
text = 'SQLVault Gateway · démonstration'
tw, th = d.textbbox((0, 0), text, font=font)[2:]
# motif diagonal très léger sur toute l'image
tile = Image.new('RGBA', (tw + 160, th + 120), (0, 0, 0, 0))
ImageDraw.Draw(tile).text((0, 0), text, font=font, fill=(11, 31, 58, 22))
tile = tile.rotate(18, expand=True)
for y in range(-tile.height, im.height + tile.height, tile.height):
    for x in range(-tile.width, im.width + tile.width, tile.width):
        layer.alpha_composite(tile, (x + (y // tile.height % 2) * tile.width // 2, y))
# mention lisible en bas à droite
pad = width // 80
d.rounded_rectangle((im.width - tw - 3 * pad, im.height - th - 3 * pad, im.width - pad, im.height - pad), radius=pad, fill=(11, 31, 58, 170))
d.text((im.width - tw - 2 * pad, im.height - th - 2 * pad - 2), text, font=font, fill=(255, 255, 255, 235))
Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB').save(out, quality=78, optimize=True)
print(out, im.size)
