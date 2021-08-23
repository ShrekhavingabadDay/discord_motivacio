from PIL import Image, ImageDraw, ImageFont
import uuid

def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    w, h = draw.textsize(t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)

def fit_text(img, text, color, font):
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 2
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, fill=color)
        y += h

def generate(image_path, font_path, text):
    img = Image.open(image_path)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 26)

    fit_text(img, text, "white", font)

    image_name = str(uuid.uuid4()) + ".jpg"
    img.save(image_name)

    return image_name
'''
def fit_text(t, max_len, d, font, w, W, H):

    final_height = 0

    output = ''
    current_line = ''
    c_count = 0

    for word in t.split(' '):

        c_count += len(word)

        if c_count >= max_len:
            output += ('\n' + word + ' ')

            _,f = d.textsize(current_line, font=font)
            final_height += f

            c_count = 0
            current_line = ''
        else:
            output += (word + ' ')
            current_line += (word + ' ')
    print(W, w, H, final_height)

    d.multiline_text( ( (W-w)/2, (H-final_height)/2 ), t, fill = "white", font=font, align='center')
'''
    

