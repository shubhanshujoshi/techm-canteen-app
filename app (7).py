# =====================================================
# TECH MAHINDRA SMART CANTEEN SYSTEM
# MOBILE SWIPE VERSION (FINAL)
# =====================================================

import streamlit as st
from datetime import datetime
import json
import os
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Tech Mahindra Smart Canteen",
    page_icon="logo.png",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

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
}

.sub-title {
    color: #555555;
    font-size: 16px;
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
}

/* CARDS */

.food-card,
.top-card,
.best-card,
.admin-card {

    background: white;
    padding: 22px;

    border-radius: 18px;

    border-left: 6px solid #D9232D;

    box-shadow:
    0px 4px 14px rgba(0,0,0,0.08);

    margin-bottom: 18px;

    min-height: 260px;
}

/* SWIPE CONTAINER */

.swipe-container {

    display: flex;

    overflow-x: auto;

    gap: 18px;

    padding-bottom: 10px;

    scroll-snap-type: x mandatory;
}

.swipe-container::-webkit-scrollbar {
    display: none;
}

.swipe-card {

    flex: 0 0 85%;

    scroll-snap-align: start;
}

/* TABS */

.stTabs [data-baseweb="tab"] {
    color: #D9232D;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #D9232D !important;
    color: white !important;
    border-radius: 10px;
}

/* STARS */

[data-testid="stFeedback"] button {
    transform: scale(1.5);
    margin-right: 10px;
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

/* MOBILE */

@media screen and (max-width: 768px) {

    .main-title {
        font-size: 30px;
    }

    .swipe-card {
        flex: 0 0 92%;
    }
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
            json.dump(fresh_data, f, indent=4)

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
        json.dump(data, f, indent=4)

ratings_data = load_data()

# =====================================================
# CURRENT MEAL
# =====================================================

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

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Admin Controls")

show_admin = st.sidebar.button("Admin View")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(auto_meal)
)

meal_data = default_data[selected_meal]

# =====================================================
# HEADER
# =====================================================

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

# =====================================================
# TOP 5 DISHES (SWIPE MODE)
# =====================================================

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

html = '<div class="swipe-container">'

for idx, dish in enumerate(top_dishes):

    stars = "★" * int(round(dish["Rating"]))

    html += f"""

    <div class="swipe-card">

        <div class="top-card">

            <h2>{idx+1}. {dish['Food']}</h2>

            <p><b>{dish['Vendor']}</b></p>

            <p style="font-size:24px; color:#D9232D;">
            {stars}
            </p>

            <h3>{dish['Rating']}/5</h3>

        </div>

    </div>
    """

html += "</div>"

st.components.v1.html(html, height=320, scrolling=True)

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
            meal_data[vendor],
            key=vendor
        )

        key = f"{selected_meal}|{vendor}|{selected_food}"

        votes = ratings_data[key]["votes"]

        avg = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 0
        )

        st.markdown(
            f"""
            <div class="food-card">

            <h2>{selected_food}</h2>

            <p><b>Vendor:</b> {vendor}</p>

            <p><b>Rating:</b> {round(avg,1)}/5</p>

            <p><b>Total Orders:</b> {votes}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

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

                st.success("Feedback Submitted Successfully ✅")

                st.rerun()

            else:

                st.warning("Please select star rating.")
