from PIL import Image, ImageDraw


def read_image(path: str):
    image = Image.open(path)
    return image


def draw_red_circle(image: Image.Image, xy: tuple[float, float, float, float]):
    draw = ImageDraw.Draw(image)
    draw.ellipse(xy=xy, fill=None, outline=(255, 0, 0), width=5)
    return image


def get_size(image: Image.Image):
    return image.size
