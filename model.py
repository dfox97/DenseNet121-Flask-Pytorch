import json
from torchvision import models
from interface import transform_image

# Make sure to pass `pretrained` as `True` to use the pretrained weights:
model = models.densenet121(pretrained=True)
# Since we are using our model only for inference, switch to `eval` mode:
model.eval()


imagenet_class_index = json.load(open(r'./imagenet_class_index.json'))


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)

    predicted_idx = str(y_hat.item())
    print(predicted_idx)
    return imagenet_class_index[predicted_idx]

# TESTING
# with open(r"./dog.jpg", 'rb') as f:
#     image_bytes = f.read()
#     print(get_prediction(image_bytes=image_bytes))
