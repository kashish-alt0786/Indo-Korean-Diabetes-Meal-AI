import streamlit as st
from PIL import Image
import pandas as pd
import requests
import io
from datetime import datetime

st.set_page_config(page_title="NutriGuard AI - AUTO Vision", page_icon="🛡️", layout="wide")
st.title("🛡️ NutriGuard AI - AUTO Vision")
st.caption("Indo-Korean Diabetes Meal AI | Upload → Auto recognises → No typing needed")
st.error("⚠️ EDUCATIONAL ONLY: Does not replace medical advice. Estimates only.")

nutrition_db = {
    'cake': {'cal':400,'carbs':80,'protein':4,'fiber':1,'gi':85,'gl':40,'impact':'High','color':'🔴','reason':'Refined flour + sugar','better':'brown rice','better_carbs':38,'better_gi':50},
    'chapati': {'cal':120,'carbs':15,'protein':3,'fiber':3,'gi':45,'gl':10,'impact':'Low','color':'🟢','reason':'Whole wheat fiber','better':'chapati','better_carbs':15,'better_gi':45},
    'chana masala': {'cal':280,'carbs':30,'protein':12,'fiber':8,'gi':38,'gl':12,'impact':'Low','color':'🟢','reason':'Chickpea protein fiber','better':'chana masala','better_carbs':30,'better_gi':38},
    'chole bhature': {'cal':450,'carbs':55,'protein':10,'fiber':6,'gi':70,'gl':32,'impact':'High','color':'🔴','reason':'Bhatura deep fried','better':'chana masala','better_carbs':30,'better_gi':38},
    'samosa': {'cal':250,'carbs':30,'protein':4,'fiber':2,'gi':70,'gl':22,'impact':'High','color':'🔴','reason':'Deep fried maida','better':'chana masala','better_carbs':30,'better_gi':38},
    'dosa': {'cal':200,'carbs':35,'protein':4,'fiber':1,'gi':65,'gl':20,'impact':'Moderate','color':'🟡','reason':'Rice + lentil fermented','better':'idli','better_carbs':25,'better_gi':50},
    'idli': {'cal':150,'carbs':25,'protein':5,'fiber':2,'gi':50,'gl':12,'impact':'Low','color':'🟢','reason':'Steamed fermented','better':'idli','better_carbs':25,'better_gi':50},
    'biryani': {'cal':380,'carbs':50,'protein':10,'fiber':3,'gi':60,'gl':25,'impact':'Moderate','color':'🟡','reason':'Rice + oil','better':'brown rice','better_carbs':38,'better_gi':50},
    'kimchi': {'cal':20,'carbs':2,'protein':1,'fiber':1,'gi':15,'gl':1,'impact':'Low','color':'🟢','reason':'Fermented low carb','better':'kimchi','better_carbs':2,'better_gi':15},
    'bibimbap': {'cal':350,'carbs':50,'protein':13,'fiber':6,'gi':50,'gl':18,'impact':'Moderate','color':'🟡','reason':'Mixed rice veggies','better':'brown rice bibimbap','better_carbs':38,'better_gi':50},
    'tteokbokki': {'cal':350,'carbs':80,'protein':4,'fiber':1,'gi':85,'gl':40,'impact':'High','color':'🔴','reason':'Rice cake sweet sauce','better':'kimchi','better_carbs':2,'better_gi':15},
    'kimbap': {'cal':300,'carbs':45,'protein':8,'fiber':3,'gi':60,'gl':20,'impact':'Moderate','color':'🟡','reason':'Rice + seaweed','better':'bibimbap','better_carbs':50,'better_gi':50},
    'white rice': {'cal':200,'carbs':45,'protein':3,'fiber':0,'gi':80,'gl':30,'impact':'High','color':'🔴','reason':'Refined grain low fiber','better':'brown rice','better_carbs':38,'better_gi':50},
    'brown rice': {'cal':180,'carbs':38,'protein':4,'fiber':3,'gi':50,'gl':16,'impact':'Low','color':'🟢','reason':'Whole grain fiber','better':'brown rice','better_carbs':38,'better_gi':50},
    'pizza': {'cal':350,'carbs':40,'protein':12,'fiber':2,'gi':70,'gl':28,'impact':'High','color':'🔴','reason':'Refined base cheese','better':'salad','better_carbs':8,'better_gi':15},
}

label_map = {
    'birthday cake':'cake','chocolate cake':'cake','cake':'cake',
    'chana masala':'chana masala','chole':'chole bhature','samosa':'samosa',
    'dosa':'dosa','idli':'idli','biryani':'biryani','kimchi':'kimchi',
    'bibimbap':'bibimbap','tteokbokki':'tteokbokki','rice cake':'tteokbokki',
    'kimbap':'kimbap','gimbap':'kimbap','white rice':'white rice','brown rice':'brown rice','pizza':'pizza'
}

def recognize(image):
    try:
        API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        r = requests.post(API_URL, data=buf.getvalue(), timeout=25)
        result = r.json()
        if isinstance(result, list) and result:
            return result
    except:
        return None
    return None

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded = st.file_uploader("Upload meal photo - AUTO will detect", type=['jpg','jpeg','png'])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    c1, c2 = st.columns([1,1.2])
    with c1:
        st.image(img, use_container_width=True)

    with c2:
        with st.spinner("🤖 Food Recognition analyzing..."):
            results = recognize(img)

        if results:
            top = results[0]
            # 1. Confidence
            st.subheader("🔍 Estimated Food Identification")
            st.markdown(f"**Detected Food:** {top['label'].title()}")
            st.markdown(f"**Confidence:** {top['score']*100:.1f}%")
            st.caption("Recognition depends on image quality, lighting, and angle.")

            with st.expander("Show Top 3 Possible Matches (Transparency)"):
                for r in results[:3]:
                    st.write(f"• {r['label'].title()} — {r['score']*100:.1f}%")

            # Map
            hf = top['label'].lower()
            food = None
            for k,v in label_map.items():
                if k in hf:
                    food = v
                    break

            if food in nutrition_db:
                d = nutrition_db[food]
                st.session_state.history.append({'food':food,'impact':d['impact'],'time':datetime.now().strftime("%H:%M")})

                st.divider()
                if d['impact']=='High':
                    st.error(f"### Estimated Glycemic Impact: {d['impact']} {d['color']}")
                elif d['impact']=='Moderate':
                    st.warning(f"### Estimated Glycemic Impact: {d['impact']} {d['color']}")
                else:
                    st.success(f"### Estimated Glycemic Impact: {d['impact']} {d['color']}")

                # 2. Nutrition sources
                st.subheader("📊 Nutrition Estimate")
                st.write(f"Calories: {d['cal']} | Carbs: {d['carbs']}g | Protein: {d['protein']}g | Fiber: {d['fiber']}g | GI: {d['gi']} | GL: {d['gl']}")
                st.info("Nutritional values are estimated using publicly available food composition databases such as USDA FoodData Central, ICMR-NIN Food Composition Tables, and the Korean Food Composition Database (RDA).")
                st.write(f"Reason: {d['reason']}")

                # 4. Comparison table
                st.subheader("🔄 Current Meal vs Healthier Alternative")
                better = nutrition_db.get(d['better'], d)
                comp = pd.DataFrame({
                    '': ['Current Meal', 'Healthier Alternative'],
                    'Meal': [food.title(), d['better'].title()],
                    'Carbs': [f"{d['carbs']}g", f"{better['carbs']}g"],
                    'GI': [d['gi'], better['gi']],
                    'Impact': [d['impact'], better['impact']]
                })
                st.table(comp)
                if d['carbs'] > better['carbs']:
                    st.success(f"💡 Swap saves ~{d['carbs']-better['carbs']}g carbs, lowers GI from {d['gi']} to {better['gi']}")
            else:
                st.warning(f"Detected as {hf.title()} but not in DB yet. Confidence shown above for transparency.")
        else:
            st.error("Model busy. Wait 15 sec and re-upload.")

# History
if st.session_state.history:
    st.divider()
    st.subheader("📈 Weekly Meal Log")
    df = pd.DataFrame(st.session_state.history)
    st.bar_chart(df['impact'].value_counts())

# 3. Limitations
st.divider()
st.subheader("⚠️ Limitations & Responsible AI")
st.markdown("""
- Recognition depends on image quality, lighting, and camera angle.
- Portion sizes are estimated, not measured.
- Nutrition values are approximate from public databases.
- Educational use only. Does not replace medical advice or insulin dosing.
""")

st.caption("Pipeline: Upload → Open-source Food Recognition (nateraw/food, Food2K) → Predicted Food → GI/GL DB (USDA/ICMR/Korean) → Risk Assessment → Healthy Swap → History")
