import os
from PIL import Image, ImageDraw, ImageFont

from .transliterate import to_latin


async def create_ticket_image(tg_id, event_id, fullname: str) -> str:
    # Tasvirni ochish
    img = Image.open('data/images/invitation.jpg')
    draw = ImageDraw.Draw(img)

    # Shrift va rang sozlamalari
    font_path = 'data/fonts/GoldenPlains-Demo.ttf'
    font = ImageFont.truetype(font_path, 270)
    text_color = (255, 255, 255)

    # Agar ism kirill alifbosida bo'lsa, lotinga o'tkazish
    if not fullname.isascii():
        fullname = to_latin(fullname)

    # Ism va familiyani ajratish
    name, surname = (fullname.split(' ', 1) + [""])[:2]

    # Name va surname uchun pozitsiyalarni hisoblash (markazlashtirilgan)
    image_center_x = img.width / 2

    # Name pozitsiyasi
    name_box = draw.textbbox((0, 0), name, font=font)
    name_width = name_box[2] - name_box[0]
    name_position = (image_center_x - name_width / 2, 2530)
    draw.text(name_position, name, font=font, fill=text_color)

    # Agar surname mavjud bo'lsa, surname pozitsiyasi
    if surname:
        surname_box = draw.textbbox((0, 0), surname, font=font)
        surname_width = surname_box[2] - surname_box[0]
        surname_position = (image_center_x - surname_width / 2, 2740)
        draw.text(surname_position, surname, font=font, fill=text_color)

    # Rasmni saqlash
    os.makedirs("media/ticket_images/", exist_ok=True)
    save_image_name = f"media/ticket_images/{tg_id}_{event_id}.jpg"
    img.save(save_image_name)

    return f"ticket_images/{tg_id}_{event_id}.jpg"
