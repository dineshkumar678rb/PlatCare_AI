import streamlit as st
import tensorflow as tf
import numpy as np
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="centered"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(91, 143, 93, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(61, 107, 70, 0.16),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #0b1710 0%,
            #12251a 45%,
            #0b1710 100%
        );
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
    max-width: 900px;
}


/* ---------- Hero ---------- */

.hero-icon {
    text-align: center;
    font-size: 48px;
    margin-bottom: 5px;
}

.hero-title {
    text-align: center;
    color: #f3f8f3;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 8px;
}

.hero-ai {
    color: #8fc69c;
}

.hero-subtitle {
    text-align: center;
    color: #aebcaf;
    font-size: 17px;
    line-height: 1.6;
}


/* ---------- Section headings ---------- */

.section-heading {
    color: #f4f8f4;
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 8px;
}

.section-description {
    color: #9eac9f;
    font-size: 14px;
    margin-bottom: 18px;
}


/* ---------- Upload ---------- */

div[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.045);
    border: 1px solid rgba(143, 198, 156, 0.25);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
}

div[data-testid="stFileUploader"] section {
    background: transparent;
}

div[data-testid="stFileUploader"] label {
    color: #dfe9df !important;
}


/* ---------- Button ---------- */

.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 15px;
    border: 1px solid rgba(143, 198, 156, 0.35);
    background: linear-gradient(
        135deg,
        #4f8a61,
        #356d49
    );
    color: white;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(48, 105, 66, 0.30);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #609d70,
        #417d54
    );
    border-color: #8fc69c;
    transform: translateY(-1px);
    box-shadow: 0 12px 30px rgba(48, 105, 66, 0.40);
}


/* ---------- Image ---------- */

img {
    border-radius: 20px;
}


/* ---------- Native containers ---------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.045);
    border: 1px solid rgba(143, 198, 156, 0.18);
    border-radius: 22px;
}


/* ---------- Metrics ---------- */

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(143, 198, 156, 0.15);
    border-radius: 16px;
    padding: 14px;
}

[data-testid="stMetricLabel"] {
    color: #91b999 !important;
}

[data-testid="stMetricValue"] {
    color: #f5faf5 !important;
}


/* ---------- Progress ---------- */

.stProgress > div > div > div > div {
    background: linear-gradient(
        90deg,
        #4f8a61,
        #8fc69c
    );
}

.stProgress > div > div {
    background-color: rgba(255, 255, 255, 0.08);
}


/* ---------- Expander ---------- */

[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(143, 198, 156, 0.18);
    border-radius: 18px;
    margin-top: 25px;
}

[data-testid="stExpander"] summary {
    color: #e9f2e9;
}


/* ---------- Divider ---------- */

hr {
    border-color: rgba(143, 198, 156, 0.12);
}


/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: #657469;
    font-size: 12px;
    margin-top: 45px;
    padding-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Class names
# -----------------------------

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


# -----------------------------
# Friendly names
# -----------------------------

friendly_names = {
    "Pepper__bell___Bacterial_spot": "Pepper Bell — Bacterial Spot",
    "Pepper__bell___healthy": "Pepper Bell — Healthy",
    "Potato___Early_blight": "Potato — Early Blight",
    "Potato___Late_blight": "Potato — Late Blight",
    "Potato___healthy": "Potato — Healthy",
    "Tomato_Bacterial_spot": "Tomato — Bacterial Spot",
    "Tomato_Early_blight": "Tomato — Early Blight",
    "Tomato_Late_blight": "Tomato — Late Blight",
    "Tomato_Leaf_Mold": "Tomato — Leaf Mold",
    "Tomato_Septoria_leaf_spot": "Tomato — Septoria Leaf Spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Tomato — Spider Mites",
    "Tomato__Target_Spot": "Tomato — Target Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Tomato — Yellow Leaf Curl Virus",
    "Tomato__Tomato_mosaic_virus": "Tomato — Mosaic Virus",
    "Tomato_healthy": "Tomato — Healthy"
}


# -----------------------------
# Disease information
# -----------------------------

disease_info = {

    "Pepper__bell___Bacterial_spot": {
        "description": "A bacterial disease that can cause small dark spots on pepper leaves and fruit.",
        "symptoms": "Small brown or dark spots, yellowing around leaf spots, and lesions on fruit.",
        "care": "Remove badly affected leaves, avoid overhead watering, improve airflow, and keep foliage dry."
    },

    "Pepper__bell___healthy": {
        "description": "The leaf appears healthy based on the trained model.",
        "symptoms": "No major disease symptoms detected by the model.",
        "care": "Continue regular watering, sunlight, nutrition, and monitoring."
    },

    "Potato___Early_blight": {
        "description": "A fungal disease commonly associated with dark lesions on potato leaves.",
        "symptoms": "Brown circular spots that may develop concentric rings and yellowing around affected areas.",
        "care": "Remove affected foliage, improve airflow, avoid wetting leaves, and maintain good field hygiene."
    },

    "Potato___Late_blight": {
        "description": "A serious potato disease that can spread quickly under cool and humid conditions.",
        "symptoms": "Dark irregular leaf lesions and rapid browning of affected foliage.",
        "care": "Remove affected plant material, improve airflow, avoid prolonged leaf wetness, and monitor nearby plants."
    },

    "Potato___healthy": {
        "description": "The leaf appears healthy based on the trained model.",
        "symptoms": "No major disease symptoms detected by the model.",
        "care": "Continue regular plant care and monitor the leaves for changes."
    },

    "Tomato_Bacterial_spot": {
        "description": "A bacterial disease that affects tomato leaves, stems, and fruit.",
        "symptoms": "Small dark spots on leaves and possible lesions on fruit.",
        "care": "Avoid overhead watering, remove affected material, improve airflow, and keep tools clean."
    },

    "Tomato_Early_blight": {
        "description": "A fungal disease that commonly affects older tomato leaves first.",
        "symptoms": "Dark spots with ring-like patterns, often followed by yellowing of surrounding tissue.",
        "care": "Remove affected leaves, improve airflow, avoid wetting foliage, and maintain good plant hygiene."
    },

    "Tomato_Late_blight": {
        "description": "A disease that can spread rapidly in cool and humid conditions.",
        "symptoms": "Dark irregular patches on leaves and rapid deterioration of affected tissue.",
        "care": "Remove affected material, reduce leaf moisture, improve airflow, and monitor nearby plants."
    },

    "Tomato_Leaf_Mold": {
        "description": "A fungal disease that commonly develops under humid conditions.",
        "symptoms": "Yellow areas on upper leaf surfaces with mold-like growth on the underside.",
        "care": "Improve ventilation, reduce humidity around foliage, and avoid overhead watering."
    },

    "Tomato_Septoria_leaf_spot": {
        "description": "A fungal disease that produces numerous small spots on tomato leaves.",
        "symptoms": "Small circular spots with darker edges, often beginning on lower leaves.",
        "care": "Remove affected leaves, keep foliage dry, improve airflow, and clear infected plant debris."
    },

    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "description": "Spider mites are tiny pests that feed on plant tissue and can weaken tomato plants.",
        "symptoms": "Fine speckling, yellowing, leaf damage, and sometimes fine webbing.",
        "care": "Inspect the underside of leaves, wash foliage gently when appropriate, and maintain healthy plant conditions."
    },

    "Tomato__Target_Spot": {
        "description": "A fungal disease that produces target-like lesions on tomato leaves.",
        "symptoms": "Circular brown lesions that may develop concentric rings.",
        "care": "Remove affected foliage, improve airflow, avoid overhead watering, and maintain garden hygiene."
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "description": "A viral disease that can cause strong changes in tomato leaf growth and color.",
        "symptoms": "Yellowing, upward curling of leaves, reduced growth, and possible stunting.",
        "care": "Remove severely affected plants when appropriate and control insect vectors such as whiteflies."
    },

    "Tomato__Tomato_mosaic_virus": {
        "description": "A viral disease that can affect tomato leaves and plant growth.",
        "symptoms": "Mottled or mosaic-like leaf patterns and possible reduced plant growth.",
        "care": "Remove affected plants when necessary, sanitize tools, and avoid spreading plant sap between plants."
    },

    "Tomato_healthy": {
        "description": "The leaf appears healthy based on the trained model.",
        "symptoms": "No major disease symptoms detected by the model.",
        "care": "Continue regular watering, sunlight, nutrition, and monitoring."
    }
}


# -----------------------------
# AI Explanation
# -----------------------------

def get_ai_explanation(disease, confidence):

    prompt = f"""
You are a friendly plant health AI advisor.

The image classification model detected:
Plant condition: {disease}
Confidence: {confidence:.2f}%

Explain this result to a beginner in simple language.

Include:
1. What this condition means
2. What symptoms they may notice
3. General care steps
4. When they should seek advice from a plant or agriculture expert

Keep the answer concise and practical.
Do not claim that the AI diagnosis is certain.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# -----------------------------
# Load model
# -----------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "plant_disease_model.keras"
    )


model = load_model()


# -----------------------------
# Hero
# -----------------------------

st.markdown(
    '<div class="hero-icon">🌿</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">'
    'PlantCare <span class="hero-ai">AI</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Intelligent plant health detection.<br>'
    'Upload a leaf and let AI analyze it.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------
# Upload section
# -----------------------------

st.markdown(
    '<div class="section-heading">Check your plant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload a clear image of a plant leaf for AI-powered analysis.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "jpeg", "png"],
    label_visibility="visible"
)


# -----------------------------
# Analysis
# -----------------------------

if uploaded_file is not None:

    image = tf.keras.utils.load_img(
        uploaded_file,
        target_size=(224, 224)
    )

    st.image(
        image,
        caption="Uploaded Leaf",
        use_container_width=True
    )

    st.write("")

    analyze = st.button(
        "🔍  Start Analysis"
    )

    if analyze:

        with st.spinner("Analyzing your plant..."):

            image_array = tf.keras.utils.img_to_array(
                image
            )

            image_array = np.expand_dims(
                image_array,
                axis=0
            )

            predictions = model.predict(
                image_array,
                verbose=0
            )[0]

            predicted_index = int(
                np.argmax(predictions)
            )

            confidence = float(
                predictions[predicted_index] * 100
            )

            prediction = class_names[
                predicted_index
            ]

            display_name = friendly_names[
                prediction
            ]

            info = disease_info[
                prediction
            ]


        # -----------------------------
        # Result
        # -----------------------------

        st.markdown(
            '<div class="section-heading">'
            'AI Detection'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                f"### 🌿 {display_name}"
            )

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )


        # -----------------------------
        # Health status
        # -----------------------------

        if "healthy" in prediction.lower():

            st.success(
                "🌱 The model indicates that this plant appears healthy."
            )

        else:

            st.warning(
                "🌿 The model detected a possible plant health condition."
            )


        # -----------------------------
        # Top 3 predictions
        # -----------------------------

        st.markdown(
            '<div class="section-heading">'
            'Top 3 Predictions'
            '</div>',
            unsafe_allow_html=True
        )

        top_3_indices = np.argsort(
            predictions
        )[-3:][::-1]

        for rank, index in enumerate(
            top_3_indices,
            start=1
        ):

            name = friendly_names[
                class_names[index]
            ]

            probability = float(
                predictions[index] * 100
            )

            with st.container(border=True):

                st.markdown(
                    f"**{rank}. {name}**"
                )

                st.caption(
                    f"{probability:.2f}% confidence"
                )

                st.progress(
                    float(predictions[index])
                )


        # -----------------------------
        # Disease information
        # -----------------------------

        st.markdown(
            '<div class="section-heading">'
            'About This Condition'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                "### 🌱 Description"
            )

            st.write(
                info["description"]
            )

            st.markdown(
                "### 🔎 Common Symptoms"
            )

            st.write(
                info["symptoms"]
            )

            st.markdown(
                "### 🌿 General Care"
            )

            st.write(
                info["care"]
            )


        # -----------------------------
        # AI Advisor
        # -----------------------------

        st.markdown(
            '<div class="section-heading">'
            '🤖 AI Plant Health Advisor'
            '</div>',
            unsafe_allow_html=True
        )

        with st.spinner("Preparing AI explanation..."):

            try:

                ai_explanation = get_ai_explanation(
                    display_name,
                    confidence
                )

                with st.container(border=True):

                    st.markdown(
                        "### 💡 AI Explanation"
                    )

                    st.markdown(
                        ai_explanation
                    )

            except Exception as e:

                with st.container(border=True):

                    st.warning(
                        "The AI explanation could not be generated right now."
                    )

                    st.caption(
                        "Your plant disease prediction is still available above."
                    )


# -----------------------------
# Model information
# -----------------------------

with st.expander("🤖  About the AI Model"):

    st.markdown("""
    **PlantCare AI** uses a **MobileNetV2 transfer learning model**
    trained to classify plant leaf images.

    **Model details:**

    - 🌿 Training images: **20,638**
    - 🧬 Classes: **15**
    - 🖼️ Image size: **224 × 224**
    - 📚 Training images: **16,511**
    - 🔬 Validation images: **4,127**
    - 📈 Best validation accuracy: **91.06%**
    - 🎯 Best result: **Epoch 9**
    """)


# -----------------------------
# Disclaimer
# -----------------------------

with st.container(border=True):

    st.markdown(
        "### ⚠️ Important"
    )

    st.write(
        "PlantCare AI provides an AI-based prediction from the "
        "uploaded image. It is intended for educational and "
        "informational purposes and should not replace professional "
        "agricultural or plant-health advice."
    )


# -----------------------------
# Footer
# -----------------------------

st.markdown(
    '<div class="footer">'
    'PlantCare AI · AI-powered plant health detection'
    '</div>',
    unsafe_allow_html=True
)