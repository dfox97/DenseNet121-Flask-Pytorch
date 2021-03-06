import io

import torchvision.transforms as transforms
from PIL import Image


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

# TESTING
# with open(r"./static/uploads/dog.jpg", 'rb') as f:
#     image_bytes = f.read()
#     tensor = transform_image(image_bytes=image_bytes)
#     print(tensor)
