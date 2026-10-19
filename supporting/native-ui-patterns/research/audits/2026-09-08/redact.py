"""Replace text or blur regions in a screenshot.

Usage: python3 redact.py <src> <dst.png> <spec.tsv>
spec.tsv rows (tab-separated):
  text	y0	y1	x0	x1	align	placeholder	[weight]
     search box in original pixels around the text to replace; align right|left;
     weight optional, e.g. Bold (SFNS.ttf variable-font axis name)
  blur	x0	y0	x1	y1	[radius]
     Gaussian-blur the box (default radius 40)
  box	y0	y1	x0	x1	[pad_y]
     cover the text found in the search box with a black rounded pill (the manual-redaction look)
  circle	cx	cy	r	[radius]
     Gaussian-blur a circular region, for example a photo avatar
For text: the script finds the text bounding box inside the search box (non-background
pixels), paints it with the background color sampled at the box corner, and draws the
placeholder with SFNS.ttf sized to the found height, in the darkest sampled color.
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/System/Library/Fonts/SFNS.ttf"


def bbox_in(img, y0, y1, x0, x1, bg, tol=18):
    px = img.load()
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y][:3]
            if abs(r - bg[0]) > tol or abs(g - bg[1]) > tol or abs(b - bg[2]) > tol:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def darkest(img, box):
    px = img.load()
    best = (255, 255, 255)
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            c = px[x, y][:3]
            if sum(c) < sum(best):
                best = c
    return best


def load_font(size, weight):
    f = ImageFont.truetype(FONT, size)
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception as exc:  # noqa: BLE001
            print("weight not applied:", exc)
    return f


def fit_font(text, target_h, weight):
    size = target_h
    for _ in range(40):
        f = load_font(size, weight)
        l, t, r, b = f.getbbox(text)
        h = b - t
        if abs(h - target_h) <= 1:
            return f
        size += 1 if h < target_h else -1
    return load_font(size, weight)


def replace_text(img, draw, y0, y1, x0, x1, align, placeholder, weight="", original=""):
    bg = img.getpixel((x0, y0))
    box = bbox_in(img, y0, y1, x0, x1, bg)
    if box is None:
        print("no text found in", (y0, y1, x0, x1))
        return
    color = darkest(img, box)
    draw.rectangle(box, fill=bg)
    # size by the original string when given, so descenders do not inflate the placeholder
    font = fit_font(original or placeholder, box[3] - box[1], weight)
    ol, ot, orr, ob = font.getbbox(original or placeholder)
    l, t, r, b = font.getbbox(placeholder)
    t = ot
    w = r - l
    x = box[2] - w - l if align == "right" else box[0] - l
    draw.text((x, box[1] - t), placeholder, font=font, fill=color)
    print("replaced", box, "->", placeholder)


def black_box(img, draw, y0, y1, x0, x1, pad_y=22, pad_left=12, pad_right=40):
    """Cover the text found in the search box with a black pill, like a manual redaction."""
    bg = img.getpixel((x0, y0))
    box = bbox_in(img, y0, y1, x0, x1, bg)
    if box is None:
        print("no text found in", (y0, y1, x0, x1))
        return
    top, bottom = box[1] - pad_y, box[3] + pad_y
    rect = (box[0] - pad_left, top, box[2] + pad_right, bottom)
    draw.rounded_rectangle(rect, radius=(bottom - top) // 2, fill=(0, 0, 0))
    print("boxed", box, "->", rect)


def blur(img, x0, y0, x1, y1, radius=40):
    region = img.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(radius))
    img.paste(region, (x0, y0))
    print("blurred", (x0, y0, x1, y1), "radius", radius)


def blur_circle(img, cx, cy, r, radius=40):
    box = (cx - r, cy - r, cx + r, cy + r)
    region = img.crop(box).filter(ImageFilter.GaussianBlur(radius))
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    img.paste(region, box[:2], mask)
    print("blurred circle", (cx, cy, r), "radius", radius)


def main(src, dst, spec):
    opened = Image.open(src)
    icc = opened.info.get("icc_profile")
    img = opened.convert("RGB")
    draw = ImageDraw.Draw(img)
    for line in open(spec, encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        op = parts[0]
        if op == "text":
            y0, y1, x0, x1 = map(int, parts[1:5])
            align, placeholder = parts[5], parts[6]
            weight = parts[7] if len(parts) > 7 else ""
            original = parts[8] if len(parts) > 8 else ""
            replace_text(img, draw, y0, y1, x0, x1, align, placeholder, weight, original)
        elif op == "blur":
            x0, y0, x1, y1 = map(int, parts[1:5])
            radius = int(parts[5]) if len(parts) > 5 else 40
            blur(img, x0, y0, x1, y1, radius)
        elif op == "box":
            y0, y1, x0, x1 = map(int, parts[1:5])
            pad_y = int(parts[5]) if len(parts) > 5 else 22
            black_box(img, draw, y0, y1, x0, x1, pad_y)
        elif op == "circle":
            cx, cy, r = map(int, parts[1:4])
            radius = int(parts[4]) if len(parts) > 4 else 40
            blur_circle(img, cx, cy, r, radius)
        else:
            print("unknown op", op)
    extra = {"icc_profile": icc} if icc else {}
    if dst.lower().endswith((".jpg", ".jpeg")):
        img.save(dst, "JPEG", quality=95, **extra)
    else:
        img.save(dst, "PNG", **extra)
    print("icc profile kept" if icc else "no icc profile in source")


if __name__ == "__main__":
    main(*sys.argv[1:4])
