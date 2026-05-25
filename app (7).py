```python
# =====================================================
# TECH MAHINDRA SMART CANTEEN SYSTEM
# FINAL ERROR-FREE VERSION
# =====================================================

import streamlit as st
from datetime import datetime
import json
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Tech Mahindra Smart Canteen",
    page_icon="🍽️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background-color: #f5f5f5;
}

/* TITLE */

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #D9232D;
}

.sub-title {
    color: #666;
    font-size: 16px;
}

/* BUTTONS */

.stButton > button {
    background-color: #D9232D;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 12px;
    font-weight: bold;
}

/* HIDE STREAMLIT */

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATA FILE
# =====================================================

DATA_FILE = "ratings_data.json"

# =====================================================
# FOOD DATA
# =====================================================

default_data = {

    "Lunch": {

        "Vendor A": [
            "Dal Rice",
            "Paneer Butter Masala",
            "Roti"
        ],

        "Vendor B": [
            "Biryani",
            "Chicken Curry",
            "Naan"
        ],

        "Vendor C": [
            "Rajma Chawal",
            "Mix Veg",
            "Jeera Rice"
        ],

        "Vendor D": [
            "Fried Rice",
            "Noodles",
            "Soup"
        ],

        "Vendor E": [
            "Butter Chicken",
            "Dal Makhani",
            "Paneer Tikka"
        ]
    }
}

# =====================================================
# INITIALIZE RATINGS
# =====================================================

def initialize_ratings():

    ratings = {}

    for meal, vendors in default_data.items():

        for vendor, foods in vendors.items():

            for food in foods:

                key = f"{meal}|{vendor}|{food}"

                ratings[key] = {
                    "total_rating": 0,
                    "votes": 0,
                    "feedbacks": []
                }

    return ratings

# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    fresh_data = initialize_ratings()

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w") as f:
            json.dump(fresh_data, f)

        return fresh_data

    try:

        with open(DATA_FILE, "r") as f:
            existing_data = json.load(f)

        for key in existing_data:

            if key in fresh_data:
                fresh_data[key].update(existing_data[key])

    except:
        fresh_data = initialize_ratings()

    return fresh_data

# =====================================================
# SAVE DATA
# =====================================================

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

ratings_data = load_data()

# =====================================================
# SENTIMENT ANALYSIS
# =====================================================

def analyze_sentiment(feedbacks):

    if not feedbacks:
        return "🟡 Neutral"

    positive_words = [
        "good", "great", "excellent",
        "amazing", "awesome", "love",
        "tasty", "best", "fresh"
    ]

    negative_words = [
        "bad", "worst", "cold",
        "dirty", "poor", "awful"
    ]

    positive = 0
    negative = 0

    for feedback in feedbacks:

        feedback = feedback.lower()

        for word in positive_words:

            if word in feedback:
                positive += 1

        for word in negative_words:

            if word in feedback:
                negative += 1

    if positive > negative:
        return "🟢 Positive"

    elif negative > positive:
        return "🔴 Negative"

    else:
        return "🟡 Neutral"

# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([1,6])

with col1:
    st.image("logo.png", width=90)

with col2:

    st.markdown(
        """
        <div class="main-title">
        Tech Mahindra Smart Canteen
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
        Intelligent Food Experience & Feedback Platform
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

meal_data = default_data["Lunch"]

# =====================================================
# TOP 5 DISHES
# =====================================================

st.markdown("## Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():

    for food in foods:

        key = f"Lunch|{vendor}|{food}"

        votes = ratings_data[key]["votes"]

        avg = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 0
        )

        top_dishes.append({
            "Food": food,
            "Vendor": vendor,
            "Rating": round(avg, 1)
        })

top_dishes = sorted(
    top_dishes,
    key=lambda x: x["Rating"],
    reverse=True
)[:5]

# =====================================================
# HORIZONTAL CARDS
# =====================================================

cols = st.columns(len(top_dishes))

for idx, dish in enumerate(top_dishes):

    stars = "★" * int(round(dish["Rating"]))

    with cols[idx]:

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:18px;
        border-left:6px solid #D9232D;
        box-shadow:0px 4px 14px rgba(0,0,0,0.08);
        min-height:240px;
        ">

        <h2>{idx+1}. {dish['Food']}</h2>

        <p><b>{dish['Vendor']}</b></p>

        <p style="
        font-size:24px;
        color:#D9232D;
        ">
        {stars}
        </p>

        <h3>{dish['Rating']}/5</h3>

        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# RATE FOOD SECTION
# =====================================================

st.markdown("## Rate Food Item")

tabs = st.tabs(list(meal_data.keys()))

for tab, vendor in zip(tabs, meal_data.keys()):

    with tab:

        selected_food = st.selectbox(
            f"Select Food - {vendor}",
            meal_data[vendor]
        )

        key = f"Lunch|{vendor}|{selected_food}"

        votes = ratings_data[key]["votes"]

        avg = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 0
        )

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:18px;
        border-left:6px solid #D9232D;
        box-shadow:0px 4px 14px rgba(0,0,0,0.08);
        ">

        <h2>{selected_food}</h2>

        <p><b>Vendor:</b> {vendor}</p>

        <p><b>Rating:</b> {round(avg,1)}/5</p>

        <p><b>Total Orders:</b> {votes}</p>

        </div>
        """, unsafe_allow_html=True)

        user_rating = st.feedback(
            "stars",
            key=f"feedback_{key}"
        )

        user_text = st.text_area(
            "Optional Feedback",
            key=f"text_{key}"
        )

        if st.button(
            f"Submit Rating - {selected_food}",
            key=f"btn_{key}"
        ):

            if user_rating is not None:

                ratings_data[key]["total_rating"] += (
                    user_rating + 1
                )

                ratings_data[key]["votes"] += 1

                if user_text.strip() != "":

                    ratings_data[key]["feedbacks"].append(
                        user_text
                    )

                save_data(ratings_data)

                st.success(
                    "Feedback Submitted Successfully ✅"
                )

                st.rerun()

            else:

                st.warning(
                    "Please select star rating."
                )

st.markdown("---")

# =====================================================
# ADMIN DASHBOARD
# =====================================================

st.markdown("## Admin Dashboard")

vendor_orders = {}
sentiment_scores = {}

for vendor, foods in meal_data.items():

    total_orders = 0

    all_feedbacks = []

    for food in foods:

        key = f"Lunch|{vendor}|{food}"

        total_orders += ratings_data[key]["votes"]

        all_feedbacks.extend(
            ratings_data[key]["feedbacks"]
        )

    vendor_orders[vendor] = total_orders

    sentiment_scores[vendor] = analyze_sentiment(
        all_feedbacks
    )

admin_cols = st.columns(5)

for idx, vendor in enumerate(vendor_orders):

    with admin_cols[idx]:

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:18px;
        border-left:6px solid #D9232D;
        box-shadow:0px 4px 14px rgba(0,0,0,0.08);
        min-height:200px;
        ">

        <h3>{vendor}</h3>

        <p>
        <b>Total Orders:</b>
        {vendor_orders[vendor]}
        </p>

        <p>
        <b>Sentiment:</b>
        {sentiment_scores[vendor]}
        </p>

        </div>
        """, unsafe_allow_html=True)
```
