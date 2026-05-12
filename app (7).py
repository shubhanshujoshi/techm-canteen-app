
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Tech Mahindra Canteen Live Ratings",
    page_icon="🍽️",
    layout="wide"
)

DATA_FILE = "ratings_data.json"

default_data = {
    "Breakfast": {
        "Vendor A": ["Poha", "Upma", "Tea", "Coffee", "Sandwich"],
        "Vendor B": ["Idli", "Dosa", "Coffee", "Vada"],
        "Vendor C": ["Paratha", "Curd", "Tea"],
        "Vendor D": ["Bread Omelette", "Boiled Eggs", "Tea"],
        "Vendor E": ["Cornflakes", "Milk", "Banana Shake"]
    },
    "Lunch": {
        "Vendor A": ["Dal Rice", "Paneer Butter Masala", "Roti"],
        "Vendor B": ["Biryani", "Raita", "Cold Drink"],
        "Vendor C": ["Rajma Chawal", "Salad", "Papad"],
        "Vendor D": ["Fried Rice", "Manchurian", "Noodles"],
        "Vendor E": ["Chicken Curry", "Jeera Rice", "Roti"]
    },
    "Snacks": {
        "Vendor A": ["Samosa", "Tea", "Coffee"],
        "Vendor B": ["Puff", "Cold Coffee", "Burger"],
        "Vendor C": ["Momos", "Spring Roll", "Tea"],
        "Vendor D": ["French Fries", "Pizza Slice", "Pepsi"],
        "Vendor E": ["Pasta", "Garlic Bread", "Milkshake"]
    },
    "Dinner": {
        "Vendor A": ["Dal Tadka", "Roti", "Rice"],
        "Vendor B": ["Kadhai Paneer", "Naan", "Lassi"],
        "Vendor C": ["Khichdi", "Curd", "Pickle"],
        "Vendor D": ["Hakka Noodles", "Soup", "Manchurian"],
        "Vendor E": ["Butter Chicken", "Rice", "Roti"]
    }
}

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

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    data = initialize_ratings()

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

ratings_data = load_data()

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

st.title("🍽️ Tech Mahindra Smart Canteen")
st.subheader(f"Currently Serving: {current_meal}")

search_query = st.text_input(
    "🔍 Search Food Item",
    placeholder="Search for dosa, biryani, tea..."
)

st.sidebar.title("Filters")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(current_meal)
)

meal_data = default_data[selected_meal]

for vendor, foods in meal_data.items():

    st.markdown("---")
    st.header(f"🏪 {vendor}")

    cols = st.columns(2)

    for index, food in enumerate(foods):

        if search_query:
            if search_query.lower() not in food.lower():
                continue

        key = f"{selected_meal}|{vendor}|{food}"

        total_rating = ratings_data[key]["total_rating"]
        votes = ratings_data[key]["votes"]

        avg_rating = round(total_rating / votes, 1) if votes > 0 else 0

        with cols[index % 2]:

            st.subheader(food)

            st.write(f"⭐ Live Rating: **{avg_rating}/5**")
            st.write(f"👥 Total Votes: {votes}")

            user_rating = st.slider(
                f"Rate {food}",
                min_value=1,
                max_value=5,
                value=5,
                key=f"slider_{key}"
            )

            if st.button(f"Submit Rating for {food}", key=f"btn_{key}"):

                ratings_data[key]["total_rating"] += user_rating
                ratings_data[key]["votes"] += 1

                save_data(ratings_data)

                st.success(
                    f"Thanks! You rated {food} {user_rating}⭐"
                )

                st.rerun()

st.markdown("---")
st.caption("Built for Tech Mahindra Canteen Management System")
