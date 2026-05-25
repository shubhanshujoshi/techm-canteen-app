# ---------------------------------------------------
# IMPORTS
# ---------------------------------------------------

import streamlit as st
from datetime import datetime
import json
import os
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Tech Mahindra Smart Canteen",
    page_icon="logo.png",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.cdnfonts.com/css/aptos');

html, body, [class*="css"] {
    font-family: 'Aptos', sans-serif;
}

.stApp {
    background-color: #f5f5f5;
    color: #111111;
}

/* HEADER */

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #D9232D;
    letter-spacing: 0.5px;
}

.sub-title {
    color: #555555;
    font-size: 16px;
    margin-top: -5px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e5e5;
}

/* BUTTONS */

.stButton > button {
    background-color: #D9232D;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #b71c26;
    transform: scale(1.02);
}

/* CARDS */

.food-card,
.best-card,
.admin-card {

    background: white;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 18px;

    border-left: 6px solid #D9232D;

    box-shadow:
    0px 4px 14px rgba(0,0,0,0.08);

    transition: 0.3s;
}

.food-card:hover,
.best-card:hover,
.admin-card:hover {

    transform: translateY(-4px);

    box-shadow:
    0px 8px 22px rgba(0,0,0,0.12);
}

/* TABS */

.stTabs [data-baseweb="tab"] {
    color: #D9232D;
    font-weight: 600;
    font-size: 15px;
}

.stTabs [aria-selected="true"] {
    background-color: #D9232D !important;
    color: white !important;
    border-radius: 10px;
}

/* STARS */

[data-testid="stFeedback"] button {
    transform: scale(1.6);
    margin-right: 10px;
}

/* INPUTS */

.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px !important;
}

/* HIDE FOOTER */

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* TOP DISHES SCROLL */

.scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 18px;
    padding-bottom: 10px;
}

.scroll-container::-webkit-scrollbar {
    height: 8px;
}

.scroll-container::-webkit-scrollbar-thumb {
    background: #D9232D;
    border-radius: 10px;
}

.scroll-card {
    min-width: 250px;
    background: white;
    padding: 20px;
    border-radius: 18px;
    border-left: 6px solid #D9232D;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA FILE
# ---------------------------------------------------

DATA_FILE = "ratings_data.json"

# ---------------------------------------------------
# FOOD DATA
# ---------------------------------------------------

default_data = {

    "Breakfast": {
        "Vendor A": ["Poha", "Upma", "Tea", "Coffee", "Sandwich"],
        "Vendor B": ["Idli", "Dosa", "Coffee", "Vada", "Pongal"],
        "Vendor C": ["Paratha", "Curd", "Tea", "Aloo Puri", "Lassi"],
        "Vendor D": ["Bread Omelette", "Boiled Eggs", "Tea", "Maggi", "Milk"],
        "Vendor E": ["Cornflakes", "Milk", "Banana Shake", "Oats", "Fruit Bowl"]
    },

    "Lunch": {
        "Vendor A": ["Dal Rice", "Paneer Butter Masala", "Roti", "Veg Pulao", "Salad"],
        "Vendor B": ["Biryani", "Raita", "Cold Drink", "Chicken Curry", "Naan"],
        "Vendor C": ["Rajma Chawal", "Salad", "Papad", "Mix Veg", "Jeera Rice"],
        "Vendor D": ["Fried Rice", "Manchurian", "Noodles", "Spring Roll", "Soup"],
        "Vendor E": ["Butter Chicken", "Jeera Rice", "Roti", "Dal Makhani", "Paneer Tikka"]
    },

    "Snacks": {
        "Vendor A": ["Samosa", "Tea", "Coffee", "Burger", "French Fries"],
        "Vendor B": ["Puff", "Cold Coffee", "Burger", "Pizza Slice", "Momos"],
        "Vendor C": ["Momos", "Spring Roll", "Tea", "Sandwich", "Cold Drink"],
        "Vendor D": ["French Fries", "Pizza Slice", "Pepsi", "Pasta", "Garlic Bread"],
        "Vendor E": ["Pasta", "Garlic Bread", "Milkshake", "Brownie", "Nachos"]
    },

    "Dinner": {
        "Vendor A": ["Dal Tadka", "Roti", "Rice", "Kheer", "Paneer Curry"],
        "Vendor B": ["Kadhai Paneer", "Naan", "Lassi", "Butter Chicken", "Soup"],
        "Vendor C": ["Khichdi", "Curd", "Pickle", "Veg Curry", "Rice"],
        "Vendor D": ["Hakka Noodles", "Soup", "Manchurian", "Fried Rice", "Spring Roll"],
        "Vendor E": ["Butter Chicken", "Rice", "Roti", "Dal Fry", "Ice Cream"]
    }
}

# ---------------------------------------------------
# INITIALIZE RATINGS
# ---------------------------------------------------

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

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

def load_data():

    fresh_data = initialize_ratings()

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w") as f:
            json.dump(fresh_data, f, indent=4)

        return fresh_data

    try:

        with open(DATA_FILE, "r") as f:
            existing_data = json.load(f)

        for key in existing_data:

            if key in fresh_data:

                fresh_data[key].update(existing_data[key])

                if "feedbacks" not in fresh_data[key]:
                    fresh_data[key]["feedbacks"] = []

    except:
        fresh_data = initialize_ratings()

    return fresh_data

# ---------------------------------------------------
# SAVE DATA
# ---------------------------------------------------

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------------------------------
# REAL SENTIMENT ANALYSIS
# ---------------------------------------------------

def analyze_sentiment(feedbacks):

    if not feedbacks:
        return "🟡 Neutral"

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for text in feedbacks:

        analysis = TextBlob(text)

        polarity = analysis.sentiment.polarity

        if polarity > 0.15:
            positive_count += 1

        elif polarity < -0.15:
            negative_count += 1

        else:
            neutral_count += 1

    total = len(feedbacks)

    positive_ratio = positive_count / total
    negative_ratio = negative_count / total

    if positive_ratio >= 0.5:
        return "🟢 Positive"

    elif negative_ratio >= 0.4:
        return "🔴 Negative"

    else:
        return "🟡 Neutral"

ratings_data = load_data()

# ---------------------------------------------------
# CURRENT MEAL
# ---------------------------------------------------

current_hour = datetime.now().hour

def get_current_meal():

    if 6 <= current_hour < 11:
        return "Breakfast"

    elif 11 <= current_hour < 16:
        return "Lunch"

    elif 16 <= current_hour < 19:
        return "Snacks"

    else:
        return "Dinner"

auto_meal = get_current_meal()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Admin Controls")

show_admin = st.sidebar.button("Admin View")

if st.sidebar.button("Reset All Ratings"):

    ratings_data = initialize_ratings()

    save_data(ratings_data)

    st.sidebar.success("Ratings Reset Successfully")

    st.rerun()

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(auto_meal)
)

meal_data = default_data[selected_meal]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

col1, col2 = st.columns([1,7])

with col1:
    st.image("logo.png", width=80)

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
        f"""
        <div class="sub-title">
        Intelligent Food Experience & Feedback Platform
        <br>
        Currently Serving: <b>{selected_meal}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# TOP 5 HIGHEST RATED
# ---------------------------------------------------

st.markdown("## Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

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

html_cards = ""

for idx, dish in enumerate(top_dishes):

    stars = "★" * int(round(dish["Rating"]))

    html_cards += f"""
    <div class="scroll-card">

    <h3>{idx+1}. {dish['Food']}</h3>

    <p><b>{dish['Vendor']}</b></p>

    <p style="font-size:22px; color:#D9232D;">
    {stars}
    </p>

    <p>
    <b>{dish['Rating']}/5</b>
    </p>

    </div>
    """

st.markdown(
    f"""
    <div class="scroll-container">
    {html_cards}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
