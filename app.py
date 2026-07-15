import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="NutriGuard AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.metric-card{
    background:#F8F9FA;
    padding:15px;
    border-radius:12px;
    border:1px solid #E0E0E0;
}

.title{
    text-align:center;
    color:#2E8B57;
}

.footer{
    text-align:center;
    color:gray;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.markdown(
    "<h1 class='title'>🥗 NutriGuard AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
"""
### Educational Nutrition Analysis for Diabetes Management

Analyze everyday Indian and Korean meals to understand:

- Carbohydrates
- Protein
- Fat
- Fiber
- Estimated Glycemic Index (GI)
- Estimated Glycemic Load (GL)
- Healthier meal alternatives

**Educational Tool Only — Not Medical Advice**
"""
)

st.divider()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.header("⚙ Settings")

    language = st.selectbox(
        "Language",
        [
            "English",
            "한국어 (Coming Soon)",
            "हिन्दी (Coming Soon)"
        ]
    )

    st.divider()

    st.subheader("About")

    st.write(
        """
NutriGuard AI is an educational Medical IT project
designed to improve nutrition literacy for diabetes
management.

Built using:

- Python
- Streamlit
- Pandas
- Plotly
"""
    )

    st.divider()

    st.info(
        "Future Version:\n\n"
        "• AI Food Recognition\n"
        "• Barcode Scanner\n"
        "• OCR Food Labels\n"
        "• Larger Food Database"
    )

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "meal_history" not in st.session_state:
    st.session_state.meal_history = []

# -------------------------------------------------
# FOOD DATABASE
# -------------------------------------------------

food_database = {

"White Rice Bibimbap":{
"food_name":"White Rice Bibimbap",
"calories":530,
"carbs":74,
"protein":18,
"fat":14,
"fiber":4,
"gi":73,
"gl":35,
"healthy_swap":"Brown Rice Bibimbap",
"swap_reason":"Brown rice contains more fiber and produces a lower estimated glycemic impact."
},

"Brown Rice Bibimbap":{
"food_name":"Brown Rice Bibimbap",
"calories":520,FFF
"carbs":60,
"protein":18,
"fat":14,
"fiber":8,
"gi":50,
"gl":18,
"healthy_swap":"Extra vegetables + tofu",
"swap_reason":"Higher fiber may help slow glucose absorption."
},

"Kimchi Fried Rice":{
"food_name":"Kimchi Fried Rice",
"calories":480,
"carbs":68,
"protein":15,
"fat":14,
"fiber":3,
"gi":72,
"gl":32,
"healthy_swap":"Brown Rice Kimchi Bowl",
"swap_reason":"Whole grains increase fiber while reducing estimated glycemic impact."
},

"Bulgogi":{
"food_name":"Bulgogi",
"calories":390,
"carbs":18,
"protein":28,
"fat":19,
"fiber":2,
"gi":35,
"gl":6,
"healthy_swap":"Lean Bulgogi with Salad",
"swap_reason":"More vegetables increase fiber."
},

"Kimchi":{
"food_name":"Kimchi",
"calories":25,
"carbs":4,
"protein":2,
"fat":0,
"fiber":2,
"gi":15,
"gl":1,
"healthy_swap":"Current meal is already healthy",
"swap_reason":"Fermented vegetables are naturally low in carbohydrates."
},

"Chapati":{
"food_name":"Whole Wheat Chapati",
"calories":120,
"carbs":20,
"protein":4,
"fat":2,
"fiber":3,
"gi":52,
"gl":10,
"healthy_swap":"Current meal is already healthy",
"swap_reason":"Whole wheat provides dietary fiber."
},

"Paratha":{
"food_name":"Paratha",
"calories":310,
"carbs":40,
"protein":6,
"fat":13,
"fiber":2,
"gi":70,
"gl":28,
"healthy_swap":"Whole Wheat Chapati",
"swap_reason":"Chapati generally contains less fat and lower glycemic impact."
},

"Rajma Chawal":{
"food_name":"Rajma Chawal",
"calories":520,
"carbs":72,
"protein":18,
"fat":9,
"fiber":12,
"gi":58,
"gl":20,
"healthy_swap":"Brown Rice Rajma",
"swap_reason":"Brown rice provides more fiber."
},

"Chana Masala":{
"food_name":"Chana Masala",
"calories":280,
"carbs":36,
"protein":14,
"fat":7,
"fiber":10,
"gi":28,
"gl":8,
"healthy_swap":"Current meal is already healthy",
"swap_reason":"High fiber legumes support slower carbohydrate absorption."
},

"Chole Bhature":{
"food_name":"Chole Bhature",
"calories":690,
"carbs":82,
"protein":18,
"fat":28,
"fiber":8,
"gi":76,
"gl":39,
"healthy_swap":"Chana Masala + Chapati",
"swap_reason":"Reduces refined flour and overall glycemic load."
}

}

# -------------------------------------------------
# HELPER FUNCTION
# -------------------------------------------------

def glycemic_level(gl):

    if gl < 10:
        return "Low"

    elif gl < 20:
        return "Moderate"

    else:
        return "High"
        # -------------------------------------------------
# IMAGE UPLOAD
# -------------------------------------------------

st.header("📷 Upload Your Meal")

uploaded_file = st.file_uploader(
    "Choose an image of your meal",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Meal",
        use_container_width=True
    )

    st.success("Image uploaded successfully!")

    st.markdown("---")

    st.subheader("🍽 Confirm Meal")

    st.subheader("🍽 Confirm Meal")

st.info(
    "🤖 Automatic food recognition will be added in a future version. "
    "For this MVP, please confirm your meal from the list below."
)

selected_food = st.selectbox(
    "🔍 Search or select your meal",
    sorted(food_database.keys()),
    help="Type a few letters to quickly find your meal."
)

result = food_database[selected_food]

st.markdown("---")

st.header("📊 Nutrition Analysis")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Calories",
        f"{result['calories']} kcal"
    )

        st.metric(
            "Carbohydrates",
            f"{result['carbs']} g"
        )

    with col2:

        st.metric(
            "Protein",
            f"{result['protein']} g"
        )

        st.metric(
            "Fat",
            f"{result['fat']} g"
        )

    with col3:

        st.metric(
            "Fiber",
            f"{result['fiber']} g"
        )

        st.metric(
            "Estimated GI",
            result["gi"]
        )

    st.markdown("---")

    st.header("🩺 Glycemic Assessment")

    impact = glycemic_level(result["gl"])

    left, right = st.columns([1,1])

    with left:

        st.metric(
            "Estimated Glycemic Load",
            result["gl"]
        )

    with right:

        if impact == "Low":

            st.success("🟢 LOW Glycemic Impact")

        elif impact == "Moderate":

            st.warning("🟡 MODERATE Glycemic Impact")

        else:

            st.error("🔴 HIGH Glycemic Impact")

    st.markdown("---")

    st.header("💡 Why did the meal receive this rating?")

    reasons = []

    if result["carbs"] > 60:
        reasons.append("High carbohydrate content")

    if result["fiber"] < 5:
        reasons.append("Low dietary fiber")

    if result["gi"] > 70:
        reasons.append("High Glycemic Index")

    if result["fat"] > 20:
        reasons.append("Higher fat content")

    if len(reasons) == 0:
        reasons.append(
            "Balanced nutritional profile."
        )

    for reason in reasons:

        st.write(f"✅ {reason}")
        # -------------------------------------------------
# HEALTHIER ALTERNATIVE
# -------------------------------------------------

st.divider()

st.header("🥗 Healthier Alternative")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Current Meal")

    st.info(result["food_name"])

with col2:

    st.subheader("Recommended Swap")

    st.success(result["healthy_swap"])

st.subheader("💡 Why is this healthier?")

benefits = [
    "Higher dietary fiber",
    "Lower estimated Glycemic Load (GL)",
    "Slower glucose absorption",
    "Better post-meal blood sugar control"
]

for benefit in benefits:
    st.write(f"✅ {benefit}")

st.info(result["swap_reason"])

# -------------------------------------------------
# SAVE MEAL HISTORY
# -------------------------------------------------

st.divider()

meal = {
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "Food": result["food_name"],
    "Calories": result["calories"],
    "Carbs": result["carbs"],
    "GI": result["gi"],
    "GL": result["gl"],
    "Impact": impact
}

st.session_state.meal_history.append(meal)

# -------------------------------------------------
# MEAL HISTORY
# -------------------------------------------------

st.header("📋 Meal History")

history = pd.DataFrame(st.session_state.meal_history)

st.dataframe(
    history,
    use_container_width=True
)

# -------------------------------------------------
# WEEKLY TREND
# -------------------------------------------------

st.subheader("📈 Glycemic Load Trend")

fig = px.bar(
    history,
    x="Food",
    y="GL",
    color="Impact",
    title="Meal Glycemic Load",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# EDUCATIONAL RESOURCES
# -------------------------------------------------

st.divider()

st.header("📚 Learn More")

st.markdown("""
### Understanding Glycemic Index (GI)

- Low GI: 55 or less
- Medium GI: 56–69
- High GI: 70+

Foods with lower GI generally raise blood sugar more slowly.

---

### Understanding Glycemic Load (GL)

GL combines:

- Glycemic Index
- Amount of carbohydrate

This provides a better estimate of the meal's potential impact on blood glucose.

---

### Healthy Eating Tips

✅ Choose whole grains

✅ Eat more vegetables

✅ Include legumes

✅ Prefer high-fiber foods

✅ Limit sugary drinks

✅ Watch portion sizes
""")

# -------------------------------------------------
# DISCLAIMER
# -------------------------------------------------

st.divider()

st.warning("""
### ⚠ Educational Disclaimer

NutriGuard AI is intended **only for educational and nutrition awareness purposes**.

• Nutrition values are estimated using publicly available food composition databases.

• Food recognition and portion estimation are approximate.

• Glycemic Index (GI) and Glycemic Load (GL) are educational estimates.

• This application does **not** diagnose diabetes or recommend treatment.

• Always consult a qualified healthcare professional for medical advice.
""")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.markdown(
"""
<div class="footer">

Developed by <b>Kashish</b>

Medical IT Portfolio Project

Python • Streamlit • Pandas • Plotly

Educational Nutrition Analysis for Diabetes Management

</div>
""",
unsafe_allow_html=True
)
