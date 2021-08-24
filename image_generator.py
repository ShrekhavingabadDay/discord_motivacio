from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import uuid
import kacsa
import requests

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness==255 else brightness / scale

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

    brightness_enhancer = ImageEnhance.Brightness(img)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 30)

    brightness_factor = 0.2 / calculate_brightness(img)
    img = brightness_enhancer.enhance(brightness_factor)

    fit_text(img, text, "white", font)

    image_name = str(uuid.uuid4()) + ".jpg"
    img.save(image_name)

    return image_name

def download_image(keywords):
    img_url = kacsa.get_image_url(keywords)
    
    if not img_url:
        return None

    img_data = requests.get(img_url).content

    img_name = str(uuid.uuid4()) + ".jpg"

    with open( img_name, "wb" ) as handler:
        handler.write(img_data)
    return img_name

