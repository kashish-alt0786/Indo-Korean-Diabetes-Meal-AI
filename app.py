import streamlit as st
from PIL import Image
import pandas as pd
import requests
import io

st.set_page_config(page_title="NutriGuard Auto", page_icon="🍰")
st.title("🛡️ NutriGuard AI - AUTO Vision")
st.caption("Upload -> Auto recognises -> No typing needed")
st.error("⚠️ EDUCATIONAL ONLY: Does not replace medical advice.")

nutrition_db = {
    'cake': {'cal': 400, 'carbs': 80, 'protein': 4, 'fiber': 1, 'sugar': 35, 'gi': 85, 'gl': 40, 'impact': 'High', 'color':'🔴', 'reason': 'Refined flour + sugar'},
    'chana masala': {'cal': 280, 'carbs': 30, 'protein': 12, 'fiber': 8, 'sugar': 5, 'gi': 38, 'gl': 12, 'impact': 'Low', 'color':'🟢', 'reason': 'Chickpea protein fiber'},
    'chole bhature': {'cal': 450, 'carbs': 55, 'protein': 10, 'fiber': 6, 'sugar': 4, 'gi': 70, 'gl': 32, 'impact': 'High', 'color':'🔴', 'reason': 'Bhatura fried'},
    'paratha': {'cal': 250, 'carbs': 45, 'protein': 6, 'fiber': 2, 'sugar': 2, 'gi': 75, 'gl': 28, 'impact': 'High', 'color':'🔴', 'reason': 'Oil fried wheat'},
    'biryani': {'cal': 380, 'carbs': 50, 'protein': 10, 'fiber': 3, 'sugar': 2, 'gi': 60, 'gl': 25, 'impact': 'Moderate', 'color':'🟡', 'reason': 'Rice + oil'},
}

label_map = {
    'birthday cake': 'cake', 'chocolate cake': 'cake', 'cheesecake': 'cake', 'cake': 'cake',
    'chana masala': 'chana masala', 'chole': 'chole bhature',
    'paratha': 'paratha', 'biryani': 'biryani',
}

def auto_recognize_food(image):
    try:
        API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
        img_byte = io.BytesIO()
        image.save(img_byte, format='JPEG')
        response = requests.post(API_URL, data=img_byte.getvalue(), timeout=25)
        result = response.json()
        if isinstance(result, list) and len(result)>0:
            return result[0]['label'].lower(), result[0]['score']
    except:
        return None, 0
    return None, 0

uploaded = st.file_uploader("Upload meal photo - AUTO will detect", type=['jpg','jpeg','png'])
if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, width=350)

    with st.spinner("🤖 Food Recognition (open-source Food2K model) analyzing by itself..."):
        hf_label, conf = auto_recognize_food(img)

    if hf_label:
        st.success(f"✅ Auto-detected: **{hf_label}** ({conf*100:.1f}%)")
        final_food = None
        for k,v in label_map.items():
            if k in hf_label:
                final_food = v
                break
        if not final_food:
            for db_key in nutrition_db:
                if db_key in hf_label:
                    final_food = db_key
                    break
        if final_food:
            data = nutrition_db[final_food]
            st.divider()
            if data['impact']=='High':
                st.error(f"### Estimated Glycemic Impact: {data['impact']} {data['color']}")
            else:
                st.success(f"### Estimated Glycemic Impact: {data['impact']} {data['color']}")
            st.write(f"- Carbs: {data['carbs']}g | Reason: {data['reason']}")
            st.write(f"Calories: {data['cal']} | Fiber: {data['fiber']}g")
            st.divider()
            st.subheader("💡 Healthy Swap")
            if final_food=='chole bhature':
                st.write("Swap chole bhature -> chana masala, GL decreases")
            elif 'cake' in final_food:
                st.write("Swap cake -> fruit + yogurt, GL decreases")
        else:
            st.warning(f"Model saw {hf_label} but not in DB yet.")
    else:
        st.error("Free model busy, wait 15 sec and re-upload. This is normal for free Hugging Face API.")

st.divider()
st.caption("Limitations: Accuracy depends on image quality and model capability. Values estimated. Educational only.")
st.caption("Pipeline: Upload -> Food Recognition Model -> Predicted Food -> GI/GL DB -> Assessment -> Swap -> History")
