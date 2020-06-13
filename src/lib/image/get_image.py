from PIL import ImageGrab, Image

def get_image(resize_factor):
    screenshot = ImageGrab.grab()
    new_size = (
        int(screenshot.size[0] * resize_factor),
        int(screenshot.size[1] * resize_factor)
    )
    return screenshot.resize(new_size, Image.ANTIALIAS)