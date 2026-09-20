import tensorflow as tf
import numpy as np

# Load the trained model
model = tf.keras.models.load_model("plant_disease_model.keras")

# Class names
class_names = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# Enter image path
image_path = input("Enter image path: ").strip('"')
# Load and prepare image
image = tf.keras.utils.load_img(
    image_path,
    target_size=(224, 224)
)

image_array = tf.keras.utils.img_to_array(image)
image_array = np.expand_dims(image_array, axis=0)

# Make prediction
predictions = model.predict(image_array)
predicted_index = np.argmax(predictions[0])
confidence = predictions[0][predicted_index] * 100

print("\nPrediction:", class_names[predicted_index])
print(f"Confidence: {confidence:.2f}%")