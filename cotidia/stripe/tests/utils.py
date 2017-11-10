import io

from PIL import Image


def generate_image_file(file_type="PNG", size=(100, 100)):
    """Return an image file instance of given type and size.

    Accepted file types are: JPEG, PNG, BMP
    """

    if file_type not in ['JPEG', 'PNG', 'BMP']:
        raise Exception("File type {0} is not accepted.".format(file_type))

    _file = io.BytesIO()
    image = Image.new('RGBA', size=size, color=(155, 0, 0))
    image.save(_file, file_type)
    _file.name = 'test.{0}'.format(file_type)
    _file.seek(0)
    return _file
