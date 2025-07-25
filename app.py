import streamlit as st
from PIL import Image
import requests
import os

# Load Hugging Face token securely
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/models/nateraw/plant-disease"

# UI settings
st.set_page_config(page_title="CropScanAI", layout="centered")
st.title("🌿 CropScanAI: Plant Disease Detector")
st.markdown("Upload a **clear crop leaf image**. We’ll identify the plant, detect disease, and give instant treatment advice.")

uploaded = st.file_uploader("📷 Upload crop image", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="📤 Uploaded Image", use_column_width=True)

    with st.spinner("🧠 Diagnosing... please wait..."):
        response = requests.post(
            MODEL_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            files={"file": uploaded}
        )

    output = response.json()

    if isinstance(output, list):
        prediction = output[0]["label"]
        st.success("✅ Prediction complete!")
        st.markdown(f"**🪴 Predicted:** `{prediction}`")

        prediction_lower = prediction.lower()
        if "blight" in prediction_lower:
            st.info("🧪 **Advice:** Apply copper-based fungicide and remove infected leaves.")
        elif "spot" in prediction_lower:
            st.info("🌱 **Advice:** Remove affected leaves and consider a sulfur spray.")
        elif "mildew" in prediction_lower:
            st.info("🧴 **Advice:** Remove affected leaves and use neem oil spray.")
        elif "healthy" in prediction_lower:
            st.info("💚 **No disease detected.** Keep up your good practices!")
        else:
            st.warning("⚠️ No specific advice available. Try re-uploading a clearer image.")
    else:
        st.error("❌ Could not analyze image. Please try again.")
