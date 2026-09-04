# -*- coding: utf-8 -*-
"""生成 LinkedIn / 微信分享用的 OG 图：assets/og.png（1200×630）"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), 'og.png')
W, H, S = 1200, 630, 2

PAPER = (251, 246, 238)
CARD = (255, 255, 255)
LINE = (239, 230, 215)
INK = (51, 48, 43)
MUTED = (156, 146, 136)
ACCENT = (224, 112, 60)

FONTS = ['/System/Library/Fonts/PingFang.ttc',
         '/System/Library/Fonts/STHeiti Medium.ttc',
         '/System/Library/Fonts/Hiragino Sans GB.ttc']


def font(size, bold=False):
    for path in FONTS:
        if not os.path.exists(path):
            continue
        for idx in ([4, 3, 2] if bold else [2, 1, 0]):
            try:
                return ImageFont.truetype(path, size, index=idx)
            except Exception:
                continue
    return ImageFont.load_default()


def main():
    w, h = W * S, H * S
    img = Image.new('RGB', (w, h), PAPER)
    d = ImageDraw.Draw(img)

    pad = 40 * S
    d.rounded_rectangle([pad, pad, w - pad, h - pad], radius=32 * S,
                        fill=CARD, outline=LINE, width=2 * S)

    # 左边：虚线圆印章「待批」
    side = 320 * S
    stamp = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    c = side // 2
    r = 118 * S
    box = [c - r, c - r, c + r, c + r]
    a = 0
    while a < 360:
        sd.arc(box, a, min(a + 13, 360), fill=MUTED + (235,), width=7 * S)
        a += 20
    fs = font(76 * S, bold=True)
    b = sd.textbbox((0, 0), '待批', font=fs)
    sd.text((c - (b[2] - b[0]) / 2 - b[0], c - (b[3] - b[1]) / 2 - b[1]),
            '待批', font=fs, fill=MUTED + (235,))
    stamp = stamp.rotate(9, resample=Image.BICUBIC, center=(c, c))
    img.paste(stamp, (128 * S, (h - side) // 2), stamp)

    # 右边：标题和两行副标题
    x = 470 * S
    d.text((x, 218 * S), '谁允许我买的？', font=font(72 * S, bold=True), fill=INK)
    d.text((x, 330 * S), '花钱之前，先找个人批一下', font=font(34 * S), fill=MUTED)
    d.text((x, 386 * S), 'Ask a friend before you buy it', font=font(30 * S), fill=MUTED)

    bar_h = 8 * S
    d.rounded_rectangle([x, 452 * S, x + 76 * S, 452 * S + bar_h],
                        radius=bar_h / 2, fill=ACCENT)

    img.resize((W, H), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, colors=48) \
        .save(OUT, optimize=True)
    print('生成 og.png', os.path.getsize(OUT), '字节')


if __name__ == '__main__':
    main()
