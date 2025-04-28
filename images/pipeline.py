from .transformations import convert_image_format, resize_image


def process_image_pipeline(image_file, config):
    from PIL import Image
    img = Image.open(image_file)
    original_image_format = img.format
    transformations = []
    if "resize" in config:
        transformations.append(lambda i: resize_image(i, config["resize"]))
    if "format" in config:
        transformations.append(lambda i: convert_image_format(i, config["format"]))

    for transform in transformations:
        img = transform(img)

    return img, original_image_format
