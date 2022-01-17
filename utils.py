import os
from flask import current_app
import secrets
from PIL import Image

def save_image(img):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pictures', picture_fn)

    output_size = (500, 500)
    img = Image.open(img)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn