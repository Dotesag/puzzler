from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


def create_photo(image_path, divisions, output_path):
    img = Image.open(image_path)
    width, height = img.size

    draw = ImageDraw.Draw(img)

    cell_width = width / divisions
    cell_height = height / divisions

    for i in range(1, divisions):
        x = i * cell_width
        draw.line([(x, 0), (x, height)], fill="black", width=5)

    for i in range(1, divisions):
        y = i * cell_height
        draw.line([(0, y), (width, y)], fill="black", width=5)

    img.save(output_path)


create_photo("asset/template.png", 4, "output.png")