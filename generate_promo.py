"""Generate a 小红书 promotional post for the IQ test."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 720, 1080  # 2:3 vertical for Xiaohongshu
img = Image.new('RGB', (W, H), '#f8f9ff')
draw = ImageDraw.Draw(img)

# Try to find a good Chinese font
font_dirs = [
    r'C:\Windows\Fonts',
    r'C:\Users\user\AppData\Local\Microsoft\Windows\Fonts',
]
font_paths = [
    'msyhbd.ttc', 'msyh.ttc',   # Microsoft YaHei
    'SIMHEI.TTF', 'SIMSUN.TTC', # SimHei, SimSun
    'SourceHanSansSC-Bold.otf', 'SourceHanSansSC-Regular.otf',
]
fonts = {}
for name, size in [('title', 52), ('subtitle', 26), ('cta', 22), ('body', 18), ('label', 16), ('qnum', 14)]:
    found = None
    for fd in font_dirs:
        for fp in font_paths:
            p = os.path.join(fd, fp)
            if os.path.exists(p):
                try:
                    found = ImageFont.truetype(p, size)
                    break
                except:
                    pass
        if found: break
    if found is None:
        found = ImageFont.load_default()
    fonts[name] = found

# === TOP GRADIENT BAR ===
for y in range(240):
    r = int(99 + (248 - 99) * y / 240)
    g = int(102 + (250 - 102) * y / 240)
    b = int(241 + (255 - 241) * y / 240)
    for x in range(W):
        draw.point((x, y), (r, g, b))

# === HEADER ===
draw.text((W//2, 60), '🧠 图形推理挑战', fill='#4f46e5', font=fonts['title'], anchor='mt')

# === DECORATIVE LINE ===
for i in range(120):
    x = W//2 - 60 + i
    y = 105
    r = int(99 + (139 - 99) * i / 120)
    g = int(102 + (92 - 102) * i / 120)
    b = int(241 + (246 - 241) * i / 120)
    draw.point((x, y), (r, g, b))

draw.text((W//2, 135), '测测你的图形推理能力', fill='#6b7280', font=fonts['subtitle'], anchor='mt')
draw.text((W//2, 170), '3×3矩阵中缺失的图案是什么？', fill='#9ca3af', font=fonts['body'], anchor='mt')

# === GRID BACKGROUND ===
grid_x, grid_y = W//2 - 160, 220
box_size, gap = 100, 6
grid_bg_color = (255, 255, 255)

# Draw grid background
draw.rounded_rectangle(
    [grid_x - 12, grid_y - 12, grid_x + 3*box_size + 2*gap + 12, grid_y + 3*box_size + 2*gap + 12],
    radius=16, fill='#ffffff', outline='#e0e7ff', width=2
)

# Grid content - a colorful matrix with shapes
grid_data = [
    [('●', '#3b82f6'), ('○', '#f59e0b'), ('●', '#3b82f6')],
    [('○', '#f59e0b'), ('●', '#3b82f6'), ('○', '#f59e0b')],
    [('●', '#3b82f6'), ('○', '#f59e0b'), ('?', '#6366f1')],
]

for row in range(3):
    for col in range(3):
        cx = grid_x + col * (box_size + gap) + box_size // 2
        cy = grid_y + row * (box_size + gap) + box_size // 2
        
        # Cell background
        draw.rounded_rectangle(
            [cx - box_size//2, cy - box_size//2, cx + box_size//2, cy + box_size//2],
            radius=10, fill='#f0f2ff' if row == 2 and col == 2 else '#f8f9ff'
        )
        
        symbol, color = grid_data[row][col]
        if row == 2 and col == 2:
            # Dashed border for missing cell
            for offset in range(4, box_size//2 - 4, 8):
                draw.arc(
                    [cx - box_size//2 + 4, cy - box_size//2 + 4, 
                     cx + box_size//2 - 4, cy + box_size//2 - 4],
                    0, 360, fill='#6366f1', width=2
                )
        
        if symbol == '?':
            draw.text((cx, cy), '?', fill='#6366f1', font=fonts['title'], anchor='mm')
        else:
            draw.text((cx, cy), symbol, fill=color, font=fonts['title'], anchor='mm')

# === OPTIONS ROW ===
opt_y = grid_y + 3*box_size + 2*gap + 45
draw.text((W//2, opt_y - 30), '选项：', fill='#6b7280', font=fonts['body'], anchor='mm')

options = [('●', '#3b82f6', 0), ('○', '#f59e0b', 1), ('◎', '#8b5cf6', 2),
           ('◉', '#6366f1', 3), ('⊙', '#14b8a6', 4), ('◌', '#ec4899', 5)]

option_size = 65
start_x = W//2 - (len(options) * (option_size + 8)) // 2 + option_size // 2

for i, (sym, color, idx) in enumerate(options):
    ox = start_x + i * (option_size + 8)
    oy = opt_y + 8
    
    # Option box
    draw.rounded_rectangle(
        [ox - option_size//2, oy - option_size//2, ox + option_size//2, oy + option_size//2],
        radius=12, fill='#ffffff', outline='#e0e7ff', width=2
    )
    # Number
    draw.text((ox - 18, oy - 22), str(idx + 1), fill='#c7d2fe', font=fonts['qnum'], anchor='mm')
    # Symbol
    draw.text((ox, oy + 2), sym, fill=color, font=fonts['subtitle'], anchor='mm')

# === DIVIDER ===
div_y = opt_y + option_size + 50
for x in range(W//2 - 80, W//2 + 80):
    draw.point((x, div_y), (196, 181, 253))

# === PRICE / CTA SECTION ===
cta_y = div_y + 40

# Follow + DM instruction box
draw.rounded_rectangle(
    [W//2 - 200, cta_y, W//2 + 200, cta_y + 110],
    radius=16, fill='#eef2ff', outline='#c7d2fe', width=2
)

# Helper: draw text centered at a y position, with exact center alignment
def center_text(draw, text, font, y, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = W // 2 - tw // 2
    draw.text((x, y), text, fill=fill, font=font)

center_text(draw, '关注 + 私信', fonts['subtitle'], cta_y + 18, '#4f46e5')
center_text(draw, '发送「IQ测试」', fonts['cta'], cta_y + 55, '#6366f1')
center_text(draw, '获取15题完整测试 + 答案解析', fonts['body'], cta_y + 85, '#9ca3af')

# === BOTTOM ===
bottom_y = H - 50
center_text(draw, '📕 小红书搜：Stanley Wong', fonts['body'], bottom_y - 10, '#c7d2fe')
center_text(draw, '或直接私信我', fonts['label'], bottom_y + 15, '#d1d5db')

# === SAMPLE BADGE ===
draw.rounded_rectangle(
    [W//2 - 50, 15, W//2 + 50, 42],
    radius=20, fill='#4f46e5'
)
draw.text((W//2, 28), '🔥 热门测试', fill='#ffffff', font=fonts['label'], anchor='mm')

# Upscale 2x for HD quality
img = img.resize((W*2, H*2), Image.LANCZOS)

# Save
out_path = r'C:\Users\user\.openclaw\workspace\iq_test_promo.png'
img.save(out_path, 'PNG')
print(f'Saved to {out_path}')
print(f'Size: {img.size}')
