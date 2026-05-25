# =====================================================
# TECH MAHINDRA SMART CANTEEN SYSTEM
# MOBILE OPTIMIZED VERSION
# =====================================================

import streamlit as st
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

/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #111111 !important;
}

/* MAIN APP */

.stApp {
    background-color: #f4f4f4;
    color: #111111 !important;
}

/* FORCE TEXT VISIBILITY */

h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #111111 !important;
}

/* TITLE */

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #D9232D !important;
}

.sub-title {
    color: #444 !important;
    font-size: 17px;
    margin-top: -10px;
}

/* BUTTON */

.stButton > button {
    background-color: #D9232D;
    color: white !important;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #b71c24;
    color: white;
}

/* INPUTS */

textarea, input {
    background-color: white !important;
    color: black !important;
}

/* =====================================================
TOP FOOD SLIDER
===================================================== */

.slider-container {
    display: flex;
    overflow-x: auto;
    gap: 18px;
    padding-bottom: 15px;
    scroll-behavior: smooth;
}

.slider-container::-webkit-scrollbar {
    height: 8px;
}

.slider-container::-webkit-scrollbar-thumb {
    background: #D9232D;
    border-radius: 20px;
}

/* FOOD CARD */

.food-card {
    min-width: 280px;
    max-width: 280px;
    background: white;
    border-radius: 24px;
    padding: 22px;
    flex-shrink: 0;
    border-left: 7px solid #D9232D;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}

.food-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 12px;
    color: #111111 !important;
}

.food-vendor {
    font-size: 20px;
    font-weight: 600;
    color: #444 !important;
}

.food-stars {
    color: #D9232D !important;
    font-size: 28px;
    margin-top: 20px;
}

.food-rating {
    font-size: 42px;
    font-weight: 800;
    margin-top: 25px;
    color: #111111 !important;
}

/* =====================================================
INFO CARD
===================================================== */

.info-card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    border-left: 6px solid #D9232D;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* =====================================================
MOBILE
===================================================== */

@media only screen and (max-width: 768px) {

    .main-title {
        font-size: 30px;
    }

    .food-card {
        min-width: 85%;
    }

    .food-title {
        font-size: 26px;
    }

    .food-rating {
        font-size: 34px;
    }

}

/* HIDE STREAMLIT */

#MainMenu {
    visibility: hidden;
}

footer {
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

# =====================================================
# INITIALIZE DATA
# =====================================================

def initialize_ratings():

    ratings = {}

    for vendor, foods in default_data.items():

        for food in foods:

            key = f"{vendor}|{food}"

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
# HEADER
# =====================================================

st.markdown(
    """
    <div class="main-title">
    🍽️ Tech Mahindra Smart Canteen
    </div>

    <div class="sub-title">
    Intelligent Food Experience & Feedback Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# =====================================================
# TOP 5 HIGHEST RATED
# =====================================================

st.markdown("## ⭐ Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in default_data.items():

    for food in foods:

        key = f"{vendor}|{food}"

        votes = ratings_data[key]["votes"]

        avg = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 4.2
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

slider_html = '<div class="slider-container">'

for idx, dish in enumerate(top_dishes):

    stars = "★" * int(round(dish["Rating"]))

    slider_html += f"""

    <div class="food-card">

        <div class="food-title">
        {idx+1}. {dish['Food']}
        </div>

        <div class="food-vendor">
        {dish['Vendor']}
        </div>

        <div class="food-stars">
        {stars}
        </div>

        <div class="food-rating">
        {dish['Rating']}/5
        </div>

    </div>

    """

slider_html += "</div>"

st.markdown(slider_html, unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# RATE FOOD SECTION
# =====================================================

st.markdown("## 🍴 Rate Food Item")

vendors = list(default_data.keys())

selected_vendor = st.selectbox(
    "Select Vendor",
    vendors
)

selected_food = st.selectbox(
    "Select Food",
    default_data[selected_vendor]
)

key = f"{selected_vendor}|{selected_food}"

votes = ratings_data[key]["votes"]

avg = (
    ratings_data[key]["total_rating"] / votes
    if votes > 0 else 0
)

st.markdown(f"""
<div class="info-card">

<h2>{selected_food}</h2>

<p><b>Vendor:</b> {selected_vendor}</p>

<p><b>Average Rating:</b> {round(avg,1)}/5</p>

<p><b>Total Ratings:</b> {votes}</p>

</div>
""", unsafe_allow_html=True)

user_rating = st.feedback(
    "stars",
    key="rating"
)

user_feedback = st.text_area(
    "Write Feedback"
)

if st.button("Submit Feedback"):

    if user_rating is not None:

        ratings_data[key]["total_rating"] += (
            user_rating + 1
        )

        ratings_data[key]["votes"] += 1

        if user_feedback.strip() != "":

            ratings_data[key]["feedbacks"].append(
                user_feedback
            )

        save_data(ratings_data)

        st.success("✅ Feedback Submitted Successfully")

        st.rerun()

    else:

        st.warning("Please select star rating")

st.markdown("---")

# =====================================================
# ADMIN DASHBOARD
# =====================================================

st.markdown("## 📊 Admin Dashboard")

cols = st.columns(5)

for idx, vendor in enumerate(default_data.keys()):

    total_votes = 0

    for food in default_data[vendor]:

        key = f"{vendor}|{food}"

        total_votes += ratings_data[key]["votes"]

    with cols[idx]:

        st.markdown(f"""
        <div class="info-card">

        <h3>{vendor}</h3>

        <p><b>Total Orders:</b> {total_votes}</p>

        </div>
        """, unsafe_allow_html=True)
