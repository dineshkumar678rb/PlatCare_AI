import os
import matplotlib.pyplot as plt
from PIL import Image

dataset_path = "plantvillage"

classes = os.listdir(dataset_path)

plt.figure(figsize=(12, 12))

for i, class_name in enumerate(classes):
    class_path = os.path.join(dataset_path, class_name)
    images = os.listdir(class_path)

    image_path = os.path.join(class_path, images[0])
    image = Image.open(image_path)

    plt.subplot(5, 4, i + 1)
    plt.imshow(image)
    plt.title(class_name, fontsize=8)
    plt.axis("off")

plt.tight_layout()
plt.show()