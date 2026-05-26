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
    layout="wide",
    initial_sidebar_state="expanded"
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

/* APP */

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

/* MOBILE */

@media (max-width: 768px) {

    .main-title {
        font-size: 28px !important;
    }

    .sub-title {
        font-size: 14px !important;
    }

}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e5e5;
}

/* BUTTONS */

.stButton > button {
    background-color: #D9232D;
    color: white !important;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #b71c26;
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
}

/* SWIPE CONTAINER */

.swipe-container {

    display: flex;

    overflow-x: auto;
    overflow-y: hidden;

    gap: 18px;

    padding-bottom: 12px;

    scroll-behavior: smooth;

    -webkit-overflow-scrolling: touch;
}

/* HIDE SCROLLBAR */

.swipe-container::-webkit-scrollbar {
    display: none;
}

/* SWIPE CARDS */

.swipe-card {

    min-width: 260px;
    max-width: 260px;

    flex-shrink: 0;
}

/* FEEDBACK */

[data-testid="stFeedback"] button {
    transform: scale(1.4);
    margin-right: 10px;
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

/* FOOTER */

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
                    "feedbacks": [],
                    "positive_votes": 0
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
# SENTIMENT ANALYSIS
# ---------------------------------------------------

def analyze_sentiment(feedbacks):

    if not feedbacks:
        return "Neutral"

    positive_words = [
        "good", "great", "excellent", "amazing",
        "awesome", "tasty", "love", "nice",
        "best", "fresh", "fantastic", "delicious"
    ]

    negative_words = [
        "bad", "worst", "cold", "stale",
        "awful", "hate", "poor", "dirty",
        "disgusting", "late", "waste"
    ]

    positive_count = 0
    negative_count = 0

    for feedback in feedbacks:

        feedback = feedback.lower()

        for word in positive_words:

            if word in feedback:
                positive_count += 1

        for word in negative_words:

            if word in feedback:
                negative_count += 1

    if positive_count > negative_count:
        return "Positive"

    elif negative_count > positive_count:
        return "Negative"

    else:
        return "Neutral"

# ---------------------------------------------------
# LOAD RATINGS
# ---------------------------------------------------

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

    st.sidebar.success("All ratings reset successfully")

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
    st.image("logo.png", width=90)

with col2:

    st.markdown(
        f"""
        <div class="main-title">
        Tech Mahindra Smart Canteen
        </div>

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
# TOP RATED DISHES
# ---------------------------------------------------

st.markdown("## Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        votes = ratings_data[key]["votes"]

        avg_rating = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 0
        )

        top_dishes.append({
            "Food": food,
            "Vendor": vendor,
            "Rating": round(avg_rating, 1)
        })

top_dishes = sorted(
    top_dishes,
    key=lambda x: x["Rating"],
    reverse=True
)[:5]

top_html = """
<div class="swipe-container">
"""

for idx, dish in enumerate(top_dishes):

    stars = "★" * int(round(dish["Rating"]))

    top_html += f"""

    <div class="swipe-card">

        <div class="top-card">

            <h3>{idx+1}. {dish['Food']}</h3>

            <p><b>{dish['Vendor']}</b></p>

            <p style="font-size:22px; color:#D9232D;">
            {stars}
            </p>

            <p><b>{dish['Rating']}/5</b></p>

        </div>

    </div>
    """

top_html += "</div>"

st.components.v1.html(top_html, height=260)

st.markdown("---")

# ---------------------------------------------------
# RATE FOOD
# ---------------------------------------------------

st.markdown("## Rate Food Item")

vendors = list(meal_data.keys())

tabs = st.tabs(vendors)

for tab, vendor in zip(tabs, vendors):

    with tab:

        foods = meal_data[vendor]

        selected_food = st.selectbox(
            f"Select Food - {vendor}",
            foods,
            key=f"{vendor}_food"
        )

        key = f"{selected_meal}|{vendor}|{selected_food}"

        votes = ratings_data[key]["votes"]

        avg_rating = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 0
        )

        sentiment = analyze_sentiment(
            ratings_data[key]["feedbacks"]
        )

        st.markdown(
            f"""
            <div class="food-card">

                <h3>{selected_food}</h3>

                <p><b>Vendor:</b> {vendor}</p>

                <p><b>Rating:</b> {round(avg_rating,1)}/5</p>

                <p><b>Total Orders:</b> {votes}</p>

                <p><b>Sentiment:</b> {sentiment}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        user_rating = st.feedback(
            "stars",
            key=f"feedback_{key}"
        )

        user_feedback = st.text_area(
            "Optional Feedback",
            placeholder="Write your feedback here...",
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

                if user_rating >= 3:
                    ratings_data[key]["positive_votes"] += 1

                if user_feedback.strip() != "":

                    ratings_data[key]["feedbacks"].append(
                        user_feedback
                    )

                save_data(ratings_data)

                st.success("Feedback Submitted Successfully")

                st.rerun()

            else:

                st.warning("Please select star rating.")

st.markdown("---")

# ---------------------------------------------------
# BEST SELLING ITEMS
# ---------------------------------------------------

st.markdown("## Best Selling Dish Of Each Vendor")

best_html = """
<div class="swipe-container">
"""

for vendor in meal_data.keys():

    best_food = None
    best_votes = -1
    best_rating = 0

    for food in meal_data[vendor]:

        key = f"{selected_meal}|{vendor}|{food}"

        votes = ratings_data[key]["votes"]

        avg_rating = (
            ratings_data[key]["total_rating"] / votes
            if votes > 0 else 0
        )

        if votes > best_votes:

            best_votes = votes
            best_food = food
            best_rating = round(avg_rating,1)

    best_html += f"""

    <div class="swipe-card">

        <div class="best-card">

            <h4>{vendor}</h4>

            <p><b>{best_food}</b></p>

            <p>Rating: {best_rating}/5</p>

            <p>Orders: {best_votes}</p>

        </div>

    </div>
    """

best_html += "</div>"

st.components.v1.html(best_html, height=240)

# ---------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------

if show_admin:

    st.markdown("---")

    st.markdown("## Admin Dashboard")

    vendor_ratings = {}
    vendor_satisfaction = {}
    vendor_orders = {}

    for vendor, foods in meal_data.items():

        total_rating = 0
        total_votes = 0
        positive_votes = 0

        for food in foods:

            key = f"{selected_meal}|{vendor}|{food}"

            total_rating += ratings_data[key]["total_rating"]

            total_votes += ratings_data[key]["votes"]

            positive_votes += ratings_data[key]["positive_votes"]

        average_rating = (
            round(total_rating / total_votes, 1)
            if total_votes > 0 else 0
        )

        satisfaction = (
            round((positive_votes / total_votes) * 100, 1)
            if total_votes > 0 else 0
        )

        vendor_ratings[vendor] = average_rating
        vendor_satisfaction[vendor] = satisfaction
        vendor_orders[vendor] = total_votes

    st.markdown("### Vendor Performance")

    admin_cols = st.columns(len(vendor_ratings))

    for idx, vendor in enumerate(vendor_ratings):

        with admin_cols[idx]:

            st.markdown(
                f"""
                <div class="admin-card">

                    <h4>{vendor}</h4>

                    <p><b>Average Rating:</b> {vendor_ratings[vendor]}/5</p>

                    <p><b>Customer Satisfaction:</b> {vendor_satisfaction[vendor]}%</p>

                    <p><b>Total Orders:</b> {vendor_orders[vendor]}</p>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Orders Served By Vendors")

    chart_data = pd.DataFrame({
        "Orders Served": list(vendor_orders.values())
    }, index=list(vendor_orders.keys()))

    st.line_chart(chart_data)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Built for Tech Mahindra Smart Canteen Management System"
)
