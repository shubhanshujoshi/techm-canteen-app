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

/* Background */

.stApp {
    background-color: #f5f5f5;
}

/* Main Title */

.main-title {
    background: linear-gradient(90deg, #E20031, #ff4d6d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-weight: 800;
    margin-top: 10px;
}

/* Subtitle */

.sub-title {
    color: #555555;
    font-size: 20px;
    margin-top: -10px;
}

/* Food Cards */

.food-card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    border-top: 5px solid #E20031;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Top Rated */

.top-rated-box {
    background-color: white;
    padding: 18px;
    border-radius: 15px;
    border-left: 8px solid #E20031;
    margin-bottom: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Best Seller */

.best-seller-box {
    background-color: white;
    padding: 18px;
    border-radius: 15px;
    border-left: 8px solid #ff9800;
    margin-bottom: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Tabs */

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 700;
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
            "Vada",
            "Pongal"
        ],

        "Vendor C": [
            "Paratha",
            "Curd",
            "Tea",
            "Aloo Puri",
            "Lassi"
        ],

        "Vendor D": [
            "Bread Omelette",
            "Boiled Eggs",
            "Tea",
            "Maggi",
            "Milk"
        ],

        "Vendor E": [
            "Cornflakes",
            "Milk",
            "Banana Shake",
            "Oats",
            "Fruit Bowl"
        ]
    },

    "Lunch": {

        "Vendor A": [
            "Dal Rice",
            "Paneer Butter Masala",
            "Roti",
            "Veg Pulao",
            "Salad"
        ],

        "Vendor B": [
            "Biryani",
            "Raita",
            "Cold Drink",
            "Chicken Curry",
            "Naan"
        ],

        "Vendor C": [
            "Rajma Chawal",
            "Salad",
            "Papad",
            "Mix Veg",
            "Jeera Rice"
        ],

        "Vendor D": [
            "Fried Rice",
            "Manchurian",
            "Noodles",
            "Spring Roll",
            "Soup"
        ],

        "Vendor E": [
            "Butter Chicken",
            "Jeera Rice",
            "Roti",
            "Dal Makhani",
            "Paneer Tikka"
        ]
    },

    "Snacks": {

        "Vendor A": [
            "Samosa",
            "Tea",
            "Coffee",
            "Burger",
            "French Fries"
        ],

        "Vendor B": [
            "Puff",
            "Cold Coffee",
            "Burger",
            "Pizza Slice",
            "Momos"
        ],

        "Vendor C": [
            "Momos",
            "Spring Roll",
            "Tea",
            "Sandwich",
            "Cold Drink"
        ],

        "Vendor D": [
            "French Fries",
            "Pizza Slice",
            "Pepsi",
            "Pasta",
            "Garlic Bread"
        ],

        "Vendor E": [
            "Pasta",
            "Garlic Bread",
            "Milkshake",
            "Brownie",
            "Nachos"
        ]
    },

    "Dinner": {

        "Vendor A": [
            "Dal Tadka",
            "Roti",
            "Rice",
            "Kheer",
            "Paneer Curry"
        ],

        "Vendor B": [
            "Kadhai Paneer",
            "Naan",
            "Lassi",
            "Butter Chicken",
            "Soup"
        ],

        "Vendor C": [
            "Khichdi",
            "Curd",
            "Pickle",
            "Veg Curry",
            "Rice"
        ],

        "Vendor D": [
            "Hakka Noodles",
            "Soup",
            "Manchurian",
            "Fried Rice",
            "Spring Roll"
        ],

        "Vendor E": [
            "Butter Chicken",
            "Rice",
            "Roti",
            "Dal Fry",
            "Ice Cream"
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

current_meal = get_current_meal()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

col1, col2 = st.columns([1, 8])

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
    placeholder="Search food items..."
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
            "Rating": avg_rating,
            "Votes": votes
        })

top_dishes = sorted(
    top_dishes,
    key=lambda x: (x["Rating"], x["Votes"]),
    reverse=True
)

for idx, dish in enumerate(top_dishes[:5], start=1):

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

        <h3>🏪 {vendor}</h3>

        <p><b>Best Selling:</b> {best_food}</p>

        <p><b>Rating:</b> {stars} ({best_rating}/5)</p>

        <p><b>Total Orders/Ratings:</b> {best_votes}</p>

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

        filtered_foods = []

        for food in foods:

            if search_query:

                if search_query.lower() not in food.lower():
                    continue

            filtered_foods.append(food)

        cols = st.columns(2)

        for index, food in enumerate(filtered_foods):

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

                    <h3>{food}</h3>

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
