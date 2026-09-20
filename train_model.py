import tensorflow as tf
from tensorflow.keras import layers, models

dataset_path = "plantvillage"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# Load training data
train_data = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Load validation data
validation_data = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_data.class_names
num_classes = len(class_names)

print("Number of classes:", num_classes)

# Data augmentation
data_augmentation = models.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])

# MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

# Build model
inputs = layers.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)

outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(inputs, outputs)

# Compile
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Save the best model during training
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "plant_disease_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    mode="max"
)

# Train the model
history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=10,
    callbacks=[checkpoint]
)

print("Best model saved as plant_disease_model.keras")