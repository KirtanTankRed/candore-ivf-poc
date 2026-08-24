from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
src = HERE.parent / "src" / "assets" / "brand" / "logo-dark.png"
out = HERE.parent / "public" / "favicon.png"

img = Image.open(src).convert("RGBA")
print("mode:", img.mode, "size:", img.size)

alpha = img.split()[-1]
w, h = img.size

col_has_content = [alpha.crop((x, 0, x + 1, h)).getbbox() is not None for x in range(w)]

start = next(i for i, v in enumerate(col_has_content) if v)
gap_start = next(i for i in range(start, w) if not col_has_content[i])
print("content starts at x=", start, "gap starts at x=", gap_start)

diamond = img.crop((0, 0, gap_start, h))
diamond = diamond.crop(diamond.split()[-1].getbbox())
print("diamond size:", diamond.size)

# Pad to a square canvas so it renders cleanly as a favicon at any size.
side = max(diamond.size)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(diamond, ((side - diamond.size[0]) // 2, (side - diamond.size[1]) // 2), diamond)
canvas.save(out)
print("saved:", out, canvas.size)
