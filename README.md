# 🌿 PlantCare AI

An AI-powered plant disease detection application that analyzes a leaf image and predicts the most likely plant condition. It also provides an AI-generated explanation with general care guidance.

🔗 **Live Demo:** https://platcareai-l7nfk7e29otxwkheakmkjf.streamlit.app/

## ✨ Features

* 📷 Upload a plant leaf image
* 🔍 Predict the plant condition using an AI image classification model
* 📊 Display prediction confidence
* 🏆 Show the top 3 predictions
* 🌱 Use beginner-friendly disease names
* 💡 Generate an AI explanation using Groq
* 🩺 Provide general symptoms and care information
* 📱 Simple and responsive Streamlit interface
* ⚠️ Includes a disclaimer that the prediction is not a professional diagnosis

## 🤖 AI Model

PlantCare AI uses **MobileNetV2** with transfer learning for image classification.

### Model Details

| Feature                  | Details            |
| ------------------------ | ------------------ |
| Architecture             | MobileNetV2        |
| Input Size               | 224 × 224          |
| Number of Classes        | 15                 |
| Dataset                  | PlantVillage       |
| Best Validation Accuracy | 91.06%             |
| Framework                | TensorFlow / Keras |

The model is trained to classify common conditions affecting pepper, potato, and tomato leaves.

## 🌿 Supported Conditions

The model supports 15 classes:

* Pepper Bell — Bacterial Spot
* Pepper Bell — Healthy
* Potato — Early Blight
* Potato — Late Blight
* Potato — Healthy
* Tomato — Bacterial Spot
* Tomato — Early Blight
* Tomato — Late Blight
* Tomato — Leaf Mold
* Tomato — Septoria Leaf Spot
* Tomato — Spider Mites
* Tomato — Target Spot
* Tomato — Yellow Leaf Curl Virus
* Tomato — Mosaic Virus
* Tomato — Healthy

## 🧠 AI Plant Health Advisor

After prediction, PlantCare AI can generate a simple explanation using the **Groq API**.

The explanation covers:

1. What the detected condition means
2. Common symptoms
3. General care steps
4. When to seek advice from a plant or agriculture expert

The AI explanation is designed to complement the image prediction and does not treat the prediction as certain.

## 🛠️ Technologies Used

* Python
* Streamlit
* TensorFlow
* Keras
* MobileNetV2
* NumPy
* Pillow
* Groq API
* python-dotenv

## 📁 Project Structure

```text
PlantCare-AI/
│
├── app.py
├── predict.py
├── train_model.py
├── explore_dataset.py
├── plant_disease_model.keras
├── requirements.txt
├── runtime.txt
└── .gitignore
```

The PlantVillage dataset and API credentials are not included in the repository.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/dineshkumar678rb/PlatCare_AI.git
cd PlatCare_AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

🔗 **Live Application:**
https://platcareai-l7nfk7e29otxwkheakmkjf.streamlit.app/

The Groq API key is stored using Streamlit Secrets rather than being included in the source code.

## ⚠️ Disclaimer

PlantCare AI is an educational AI-based plant disease detection tool. Predictions may be incorrect and should not be considered a professional agricultural diagnosis. For serious or uncertain plant health problems, consult a qualified agriculture or plant health professional.

## 👨‍💻 Author

**Dinesh Kumar R B**

BCA Student - CHRIST (Deemed to be University)

GitHub: https://github.com/dineshkumar678rb
