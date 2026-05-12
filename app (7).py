import streamlit as st
from datetime import datetime
import json
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Tech Mahindra Smart Canteen",
    page_icon="🔺",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS - TECH MAHINDRA THEME
# ---------------------------------------------------

st.markdown("""
<style>

/* Main Background */

.stApp {
    background-color: #f8f8f8;
}

/* Header */

.main-title {
    color: #D71920;
    font-size: 42px;
    font-weight: 800;
    text-align: center;
}

.sub-title {
    color: #555555;
    text-align: center;
    font-size: 20px;
    margin-bottom: 30px;
}

/* Top Rated Section */

.top-rated-box {
    background-color: white;
    padding: 18px;
    border-radius: 15px;
    border-left: 8px solid #D71920;
    margin-bottom: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

/* Food Cards */

.food-card {
    background-color: white;
    padding: 18px;
    border-radius: 18px;
    border-top: 6px solid #D71920;
    margin-bottom: 20px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

/* Vendor Tabs */

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
    color: #D71920;
}

.stTabs [aria-selected="true"] {
    background-color: #D71920 !important;
    color: white !important;
    border-radius: 10px;
}

/* Buttons */

.stButton>button {
    background-color: #D71920;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #a51218;
    color: white;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

/* Search Box */

.stTextInput>div>div>input {
    border: 2px solid #D71920;
    border-radius: 10px;
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

        "Vendor A": [
            "Poha",
            "Upma",
            "Tea",
            "Coffee",
            "Sandwich"
        ],

        "Vendor B": [
            "Idli",
            "Dosa",
            "Coffee",
            "Vada"
        ],

        "Vendor C": [
            "Paratha",
            "Curd",
            "Tea"
        ],

        "Vendor D": [
            "Bread Omelette",
            "Boiled Eggs",
            "Tea"
        ],

        "Vendor E": [
            "Cornflakes",
            "Milk",
            "Banana Shake"
        ]
    },

    "Lunch": {

        "Vendor A": [
            "Dal Rice",
            "Paneer Butter Masala",
            "Roti"
        ],

        "Vendor B": [
            "Biryani",
            "Raita",
            "Cold Drink"
        ],

        "Vendor C": [
            "Rajma Chawal",
            "Salad",
            "Papad"
        ],

        "Vendor D": [
            "Fried Rice",
            "Manchurian",
            "Noodles"
        ],

        "Vendor E": [
            "Chicken Curry",
            "Jeera Rice",
            "Roti"
        ]
    },

    "Snacks": {

        "Vendor A": [
            "Samosa",
            "Tea",
            "Coffee"
        ],

        "Vendor B": [
            "Puff",
            "Cold Coffee",
            "Burger"
        ],

        "Vendor C": [
            "Momos",
            "Spring Roll",
            "Tea"
        ],

        "Vendor D": [
            "French Fries",
            "Pizza Slice",
            "Pepsi"
        ],

        "Vendor E": [
            "Pasta",
            "Garlic Bread",
            "Milkshake"
        ]
    },

    "Dinner": {

        "Vendor A": [
            "Dal Tadka",
            "Roti",
            "Rice"
        ],

        "Vendor B": [
            "Kadhai Paneer",
            "Naan",
            "Lassi"
        ],

        "Vendor C": [
            "Khichdi",
            "Curd",
            "Pickle"
        ],

        "Vendor D": [
            "Hakka Noodles",
            "Soup",
            "Manchurian"
        ],

        "Vendor E": [
            "Butter Chicken",
            "Rice",
            "Roti"
        ]
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

    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "r") as f:
            return json.load(f)

    data = initialize_ratings()

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    return data

# ---------------------------------------------------
# SAVE DATA
# ---------------------------------------------------

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

ratings_data = load_data()

# ---------------------------------------------------
# CURRENT MEAL LOGIC
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

current_meal = get_current_meal()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="main-title">🔺 Tech Mahindra Smart Canteen</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="sub-title">Currently Serving: {current_meal}</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

search_query = st.text_input(
    "🔍 Search Food Item",
    placeholder="Search dosa, biryani, tea..."
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🍽 Meal Filters")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(current_meal)
)

meal_data = default_data[selected_meal]

# ---------------------------------------------------
# TOP RATED SECTION
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
            "Rating": avg_rating,
            "Votes": votes
        })

top_dishes = sorted(
    top_dishes,
    key=lambda x: (x["Rating"], x["Votes"]),
    reverse=True
)

top_5 = top_dishes[:5]

for idx, dish in enumerate(top_5, start=1):

    stars = "⭐" * int(round(dish["Rating"]))

    st.markdown(
        f"""
        <div class="top-rated-box">

        <h3>#{idx} 🍽️ {dish['Food']}</h3>

        <p><b>Vendor:</b> {dish['Vendor']}</p>

        <p><b>Rating:</b> {stars} ({dish['Rating']}/5)</p>

        <p><b>Total Votes:</b> {dish['Votes']}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# VENDOR TABS
# ---------------------------------------------------

vendors = list(meal_data.keys())

tabs = st.tabs(vendors)

for tab, vendor in zip(tabs, vendors):

    with tab:

        st.markdown(f"## 🏪 {vendor}")

        foods = meal_data[vendor]

        cols = st.columns(2)

        for index, food in enumerate(foods):

            if search_query:

                if search_query.lower() not in food.lower():
                    continue

            key = f"{selected_meal}|{vendor}|{food}"

            total_rating = ratings_data[key]["total_rating"]

            votes = ratings_data[key]["votes"]

            avg_rating = (
                round(total_rating / votes, 1)
                if votes > 0 else 0
            )

            display_stars = "⭐" * int(round(avg_rating))

            with cols[index % 2]:

                st.markdown(
                    '<div class="food-card">',
                    unsafe_allow_html=True
                )

                st.subheader(food)

                st.write(
                    f"⭐ Live Rating: {display_stars} ({avg_rating}/5)"
                )

                st.write(f"👥 Total Votes: {votes}")

                # SINGLE STAR BAR

                user_rating = st.feedback(
                    "stars",
                    key=f"feedback_{key}"
                )

                # SUBMIT BUTTON

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

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Built for Tech Mahindra Canteen Management System"
)
