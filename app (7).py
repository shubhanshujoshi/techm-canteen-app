import streamlit as st
from datetime import datetime
import json
import os

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

/* Global Font */

html, body, [class*="css"] {
    font-family: Aptos, "Segoe UI", sans-serif;
}

/* Background */

.stApp {
    background-color: #f5f5f5;
    color: #111111;
}

/* Dark Mode */

@media (prefers-color-scheme: dark) {

    .stApp {
        background-color: #111111 !important;
        color: white !important;
    }

    p, h1, h2, h3, h4, h5, h6, label, div {
        color: white !important;
    }

    .food-card,
    .top-rated-box,
    .best-seller-box,
    .search-card {
        background-color: #1e1e1e !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }

    .stTextInput > div > div > input {
        background-color: #1e1e1e !important;
        color: white !important;
    }
}

/* Header Container */

.header-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
}

/* Logo */

.logo-img {
    width: 55px;
}

/* Main Title */

.main-title {
    background: linear-gradient(90deg, #E20031, #ff4d6d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 28px;
    font-weight: 700;
    line-height: 1.2;
}

/* Subtitle */

.sub-title {
    color: #555555;
    font-size: 15px;
    margin-top: 2px;
}

/* Cards */

.food-card,
.top-rated-box,
.best-seller-box,
.search-card {
    background-color: white;
    padding: 18px;
    border-radius: 16px;
    border-top: 5px solid #E20031;
    margin-bottom: 18px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

/* Tabs */

.stTabs [data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 600;
    color: #E20031;
}

.stTabs [aria-selected="true"] {
    background-color: #E20031 !important;
    color: white !important;
    border-radius: 10px;
}

/* Buttons */

.stButton > button {
    background-color: #E20031;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background-color: #b80028;
    color: white;
}

/* Search */

.stTextInput > div > div > input {
    border: 2px solid #E20031;
    border-radius: 10px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: white;
}

/* Mobile Responsive */

@media (max-width: 768px) {

    .header-container {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .main-title {
        font-size: 24px;
    }

    .logo-img {
        width: 50px;
    }
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
                    "votes": 0
                }

    return ratings

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

def load_data():

    fresh_data = initialize_ratings()

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w") as f:
            json.dump(fresh_data, f)

        return fresh_data

    with open(DATA_FILE, "r") as f:
        existing_data = json.load(f)

    for key in existing_data:

        if key in fresh_data:
            fresh_data[key] = existing_data[key]

    with open(DATA_FILE, "w") as f:
        json.dump(fresh_data, f)

    return fresh_data

# ---------------------------------------------------
# SAVE DATA
# ---------------------------------------------------

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

ratings_data = load_data()

# ---------------------------------------------------
# RESET BUTTON
# ---------------------------------------------------

st.sidebar.markdown("## ⚙️ Controls")

if st.sidebar.button("🔄 Reset All Ratings"):

    ratings_data = initialize_ratings()

    save_data(ratings_data)

    st.sidebar.success("All ratings reset successfully.")

    st.rerun()

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

st.sidebar.title("🍽 Meal Filters")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(auto_meal)
)

current_meal = selected_meal

meal_data = default_data[selected_meal]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class="header-container">

    <img src="data:image/png;base64,"
    class="logo-img">

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 8])

with col1:
    st.image("logo.png", width=55)

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
            Currently Serving: <b>{current_meal}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

search_query = st.text_input(
    "🔍 Search Food Item",
    placeholder="Search all food items..."
)

# ---------------------------------------------------
# SEARCH RESULTS
# ---------------------------------------------------

if search_query:

    st.markdown("## 🔎 Search Results")

    found = False

    for meal, vendors in default_data.items():

        for vendor, foods in vendors.items():

            for food in foods:

                if search_query.lower() in food.lower():

                    found = True

                    key = f"{meal}|{vendor}|{food}"

                    total_rating = ratings_data[key]["total_rating"]

                    votes = ratings_data[key]["votes"]

                    avg_rating = (
                        round(total_rating / votes, 1)
                        if votes > 0 else 0
                    )

                    stars = "⭐" * int(round(avg_rating))

                    st.markdown(
                        f"""
                        <div class="search-card">

                        <h4>🍽️ {food}</h4>

                        <p><b>Meal:</b> {meal}</p>

                        <p><b>Vendor:</b> {vendor}</p>

                        <p>
                        ⭐ <b>Rating:</b>
                        {stars} ({avg_rating}/5)
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    user_rating = st.feedback(
                        "stars",
                        key=f"search_{key}"
                    )

                    if st.button(
                        f"Submit Rating for {food}",
                        key=f"search_btn_{key}"
                    ):

                        if user_rating is not None:

                            ratings_data[key]["total_rating"] += (
                                user_rating + 1
                            )

                            ratings_data[key]["votes"] += 1

                            save_data(ratings_data)

                            st.success(
                                f"You rated {food} {user_rating + 1}⭐"
                            )

                            st.rerun()

    if not found:
        st.warning("No food item found.")

st.markdown("---")

# ---------------------------------------------------
# TOP 5
# ---------------------------------------------------

st.markdown("## 🏆 Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        total_rating = ratings_data[key]["total_rating"]

        votes = ratings_data[key]["votes"]

        avg_rating = (
            round(total_rating / votes, 1)
            if votes > 0 else 0
        )

        top_dishes.append({
            "Food": food,
            "Vendor": vendor,
            "Rating": avg_rating
        })

top_dishes = sorted(
    top_dishes,
    key=lambda x: x["Rating"],
    reverse=True
)

for idx, dish in enumerate(top_dishes[:5], start=1):

    stars = "⭐" * int(round(dish["Rating"]))

    st.markdown(
        f"""
        <div class="top-rated-box">

        <h4>#{idx} 🍽️ {dish['Food']}</h4>

        <p><b>Vendor:</b> {dish['Vendor']}</p>

        <p><b>Rating:</b> {stars} ({dish['Rating']}/5)</p>

        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# BEST SELLERS
# ---------------------------------------------------

st.markdown("## 🔥 Best Selling Dish Of Each Vendor")

for vendor, foods in meal_data.items():

    best_food = None
    best_votes = -1
    best_rating = 0

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        votes = ratings_data[key]["votes"]

        total_rating = ratings_data[key]["total_rating"]

        avg_rating = (
            round(total_rating / votes, 1)
            if votes > 0 else 0
        )

        if votes > best_votes:

            best_votes = votes
            best_food = food
            best_rating = avg_rating

    stars = "⭐" * int(round(best_rating))

    st.markdown(
        f"""
        <div class="best-seller-box">

        <h4>🏪 {vendor}</h4>

        <p><b>Best Selling:</b> {best_food}</p>

        <p><b>Average Rating:</b> {stars} ({best_rating}/5)</p>

        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# RATE FOOD SECTION
# ---------------------------------------------------

st.markdown("## ⭐ Rate The Food")

# ---------------------------------------------------
# VENDOR TABS
# ---------------------------------------------------

vendors = list(meal_data.keys())

tabs = st.tabs(vendors)

for tab, vendor in zip(tabs, vendors):

    with tab:

        st.markdown(f"### 🏪 {vendor}")

        foods = meal_data[vendor]

        cols = st.columns(2)

        for index, food in enumerate(foods):

            key = f"{selected_meal}|{vendor}|{food}"

            total_rating = ratings_data[key]["total_rating"]

            votes = ratings_data[key]["votes"]

            avg_rating = (
                round(total_rating / votes, 1)
                if votes > 0 else 0
            )

            stars = "⭐" * int(round(avg_rating))

            with cols[index % 2]:

                st.markdown(
                    f"""
                    <div class="food-card">

                    <h4>{food}</h4>

                    <p>
                    ⭐ <b>Live Rating:</b>
                    {stars} ({avg_rating}/5)
                    </p>

                    <p>
                    👥 <b>Total Votes:</b> {votes}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                user_rating = st.feedback(
                    "stars",
                    key=f"feedback_{key}"
                )

                if st.button(
                    "Submit Rating",
                    key=f"btn_{key}"
                ):

                    if user_rating is not None:

                        ratings_data[key]["total_rating"] += (
                            user_rating + 1
                        )

                        ratings_data[key]["votes"] += 1

                        save_data(ratings_data)

                        st.success(
                            f"You rated {food} {user_rating + 1}⭐"
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Please select stars before submitting."
                        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Built for Tech Mahindra Canteen Management System"
)
