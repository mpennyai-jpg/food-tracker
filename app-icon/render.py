from PIL import Image, ImageDraw

S = 4           # supersample
N = 512 * S

def px(v): return v * S

img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# background gradient inside rounded square
grad = Image.new("RGB", (1, 512))
for y in range(512):
    t = y / 511
    r = int(0x17 + (0x0d - 0x17) * t)
    g = int(0x30 + (0x1a - 0x30) * t)
    b = int(0x3c + (0x22 - 0x3c) * t)
    grad.putpixel((0, y), (r, g, b))
grad = grad.resize((N, N))
mask = Image.new("L", (N, N), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, N - 1, N - 1], radius=px(112), fill=255)
img.paste(grad, (0, 0), mask)

d = ImageDraw.Draw(img)
# subtle teal hairline
d.rounded_rectangle([px(13), px(13), px(499), px(499)], radius=px(102),
                    outline=(45, 212, 191, 70), width=px(6))

WHITE = (232, 251, 247, 255)
TEAL = (45, 212, 191, 255)
w = px(30)

def thick_line(p1, p2, color, width):
    d.line([p1, p2], fill=color, width=width)
    r = width // 2
    for (x, y) in (p1, p2):
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)

P = lambda x, y: (px(x), px(y))

# roof
thick_line(P(74, 252), P(256, 106), WHITE, w)
thick_line(P(256, 106), P(438, 252), WHITE, w)
# walls
thick_line(P(118, 238), P(118, 404), WHITE, w)
thick_line(P(394, 238), P(394, 404), WHITE, w)
thick_line(P(118, 404), P(394, 404), WHITE, w)

# pine tree
d.polygon([P(256, 192), P(314, 268), P(198, 268)], fill=TEAL)
d.polygon([P(256, 248), P(332, 334), P(180, 334)], fill=TEAL)
d.rounded_rectangle([px(239), px(322), px(273), px(384)], radius=px(8), fill=TEAL)

base = img.resize((512, 512), Image.LANCZOS)
base.save("icon-512.png")
for size, name in [(192, "icon-192.png"), (180, "apple-touch-icon.png"), (96, "preview-96.png"), (48, "preview-48.png")]:
    base.resize((size, size), Image.LANCZOS).save(name)
print("ok")
