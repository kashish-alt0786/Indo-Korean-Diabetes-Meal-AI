# No need for dark, Streamlit light theme is default on mobile
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Indo-Korean Diabetes Meal AI", layout="wide")
st.title("🇮🇳🇰🇷 Indo-Korean Diabetes Meal AI")
st.caption("Upload a photo of Indian or Korean food → Get carbs, GI, and insulin help")

# --- Indo-Korean Food Database (Carbs matter for diabetes) ---
nutrition_db = {
    # Indian
    'roti': {'carbs': 15, 'sugar': 0.5, 'gi': 'Low', 'safe': True, 'note': 'Whole wheat, good fiber'},
    'dal': {'carbs': 20, 'sugar': 1, 'gi': 'Low', 'safe': True, 'note': 'Protein + fiber helps sugar'},
    'rice': {'carbs': 45, 'sugar': 0.1, 'gi': 'High', 'safe': False, 'note': 'White rice spikes fast'},
    'rajma': {'carbs': 40, 'sugar': 2, 'gi': 'Medium', 'safe': True, 'note': 'Fiber slows sugar'},
    'idli': {'carbs': 30, 'sugar': 1, 'gi': 'Medium', 'safe': True, 'note': 'Steamed, better than fried'},
    'dosa': {'carbs': 35, 'sugar': 1, 'gi': 'High', 'safe': False, 'note': 'Crispy = oil + high GI'},
    'curd': {'carbs': 4, 'sugar': 4, 'gi': 'Low', 'safe': True, 'note': 'Good for gut'},
    'paneer': {'carbs': 3, 'sugar': 1, 'gi': 'Low', 'safe': True, 'note': 'Low carb, high protein'},
    # Korean
    'kimchi': {'carbs': 2, 'sugar': 1, 'gi': 'Low', 'safe': True, 'note': 'Fermented, very good'},
    'bibimbap': {'carbs': 60, 'sugar': 5, 'gi': 'Medium', 'safe': True, 'note': 'Mix rice + veggies'},
    'bulgogi': {'carbs': 10, 'sugar': 8, 'gi': 'Low', 'safe': True, 'note': 'Watch sugar marinade'},
    'tteokbokki': {'carbs': 80, 'sugar': 15, 'gi': 'Very High', 'safe': False, 'note': 'Rice cake = sugar bomb'},
    'kimbap': {'carbs': 50, 'sugar': 3, 'gi': 'Medium', 'safe': False, 'note': 'White rice roll'},
    'japchae': {'carbs': 30, 'sugar': 6, 'gi': 'Medium', 'safe': True, 'note': 'Glass noodles better'},
    'samgyeopsal': {'carbs': 0, 'sugar': 0, 'gi': 'Low', 'safe': True, 'note': 'Pork belly, 0 carb'},
}

# Sidebar for insulin ratio
st.sidebar.header("💉 Insulin Settings")
ic_ratio = st.sidebar.number_input("Your I:C Ratio (1 unit per X g carbs)", value=10, min_value=1)
current_food = st.sidebar.selectbox("Demo: Select food (if no photo AI yet)", [""] + list(nutrition_db.keys()))

uploaded_file = st.file_uploader("Upload your meal photo", type=['jpg','png','jpeg'])

selected = None
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Your meal", width=400)
    st.info("MVP Demo: AI detection coming in v2. For now, use sidebar selector to see carbs logic.")
    selected = current_food
else:
    selected = current_food

if selected and selected in nutrition_db:
    data = nutrition_db[selected]
    st.divider()
    st.subheader(f"Detected: {selected.title()}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Carbs", f"{data['carbs']} g")
    c2.metric("Sugar", f"{data['sugar']} g")
    c3.metric("Glycemic Index", data['gi'])
    insulin = round(data['carbs'] / ic_ratio, 1)
    c4.metric("Insulin Needed", f"{insulin} units")

    if data['safe']:
        st.success(f"✅ SAFE: {data['note']}")
    else:
        st.error(f"⚠️ SPIKE RISK: {data['note']}")

    st.caption(f"For {data['carbs']}g carbs with ratio 1:{ic_ratio}, take ~{insulin} units. Always confirm with doctor.")

st.divider()
st.write("**Roadmap v2:** Add YOLOv8 food detection + USDA + Korean Rural Dev DB")
