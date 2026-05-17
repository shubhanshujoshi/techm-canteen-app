import streamlit as st
from datetime import datetime
import json
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Tech Mahindra Smart Canteen",
    page_icon="🍽️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.stApp {
    background-color: #f5f5f5;
}

/* DARK MODE */

@media (prefers-color-scheme: dark) {

    .stApp {
        background-color: #111111 !important;
    }

    p, h1, h2, h3, h4, h5, h6, label, div {
        color: white !important;
    }
}

/* TITLE */

.main-title {
    background: linear-gradient(90deg, #E20031, #ff4d6d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 34px;
    font-weight: 700;
}

.sub-title {
    font-size: 16px;
    color: #666;
}

/* BUTTONS */

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

/* BIGGER STARS */

[data-testid="stFeedback"] button {
    transform: scale(1.8);
    margin-right: 12px;
}

/* MOBILE */

@media (max-width: 768px) {

    .main-title {
        font-size: 24px;
    }

}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA FILES
# ---------------------------------------------------

DATA_FILE = "ratings_data.json"
FEEDBACK_FILE = "food_feedback.json"

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

auto_meal = get_current_meal()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Meal Filters")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(auto_meal)
)

meal_data = default_data[selected_meal]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

col1, col2 = st.columns([1, 7])

with col1:
    st.markdown("## 🍽️")

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
            Currently Serving: <b>{selected_meal}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# TOP 5 DISHES
# ---------------------------------------------------

st.markdown("## Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        total_rating = ratings_data[key]["total_rating"]
        votes = ratings_data[key]["votes"]

        avg = round(total_rating / votes, 1) if votes > 0 else 0

        top_dishes.append({
            "food": food,
            "vendor": vendor,
            "rating": avg
        })

top_dishes = sorted(
    top_dishes,
    key=lambda x: x["rating"],
    reverse=True
)[:5]

top_html = """
<div style="
display:flex;
overflow-x:auto;
gap:16px;
padding-bottom:12px;
">
"""

for idx, dish in enumerate(top_dishes):

    stars = "⭐" * int(round(dish["rating"]))

    top_html += f"""
    <div style="
        min-width:250px;
        background:white;
        border-radius:18px;
        padding:20px;
        border-top:5px solid #E20031;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        flex-shrink:0;
    ">

        <h3>{idx+1}. {dish['food']}</h3>

        <p><b>{dish['vendor']}</b></p>

        <h2>{stars}</h2>

        <p>{dish['rating']}/5</p>

    </div>
    """

top_html += "</div>"

st.markdown(top_html, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# FEEDBACK SECTION
# ---------------------------------------------------

st.markdown("## Food Feedback")

vendors = list(meal_data.keys())

tabs = st.tabs(vendors)

for tab, vendor in zip(tabs, vendors):

    with tab:

        foods = meal_data[vendor]

        selected_food = st.selectbox(
            f"Select Food - {vendor}",
            foods,
            key=f"feedback_food_{vendor}"
        )

        feedback_text = st.text_area(
            "Write Your Feedback",
            placeholder="Taste, quality, hygiene, service etc.",
            key=f"text_{vendor}"
        )

        if st.button(
            f"Submit Feedback - {vendor}",
            key=f"feedback_btn_{vendor}"
        ):

            feedback_data = []

            if os.path.exists(FEEDBACK_FILE):

                with open(FEEDBACK_FILE, "r") as f:
                    feedback_data = json.load(f)

            feedback_data.append({
                "meal": selected_meal,
                "vendor": vendor,
                "food": selected_food,
                "feedback": feedback_text,
                "time": str(datetime.now())
            })

            with open(FEEDBACK_FILE, "w") as f:
                json.dump(feedback_data, f)

            st.success("Feedback Submitted Successfully")

st.markdown("---")

# ---------------------------------------------------
# BEST SELLERS
# ---------------------------------------------------

st.markdown("## Best Selling Food Item Of Each Vendor")

best_sellers = []

for vendor, foods in meal_data.items():

    best_food = None
    best_votes = -1
    best_rating = 0

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        votes = ratings_data[key]["votes"]
        total_rating = ratings_data[key]["total_rating"]

        avg = round(total_rating / votes, 1) if votes > 0 else 0

        if votes > best_votes:

            best_votes = votes
            best_food = food
            best_rating = avg

    best_sellers.append({
        "vendor": vendor,
        "food": best_food,
        "rating": best_rating,
        "votes": best_votes
    })

seller_html = """
<div style="
display:flex;
overflow-x:auto;
gap:16px;
padding-bottom:12px;
">
"""

for item in best_sellers:

    stars = "⭐" * int(round(item["rating"]))

    seller_html += f"""
    <div style="
        min-width:250px;
        background:white;
        border-radius:18px;
        padding:20px;
        border-top:5px solid #E20031;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        flex-shrink:0;
    ">

        <h3>{item['vendor']}</h3>

        <p><b>{item['food']}</b></p>

        <h2>{stars}</h2>

        <p>{item['rating']}/5</p>

        <p>{item['votes']} Votes</p>

    </div>
    """

seller_html += "</div>"

st.markdown(seller_html, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# RATE FOOD
# ---------------------------------------------------

st.markdown("## Rate Food")

tabs = st.tabs(vendors)

for tab, vendor in zip(tabs, vendors):

    with tab:

        foods = meal_data[vendor]

        selected_food = st.selectbox(
            f"Choose Food - {vendor}",
            foods,
            key=f"rate_{vendor}"
        )

        key = f"{selected_meal}|{vendor}|{selected_food}"

        total_rating = ratings_data[key]["total_rating"]
        votes = ratings_data[key]["votes"]

        avg = round(total_rating / votes, 1) if votes > 0 else 0

        stars = "⭐" * int(round(avg))

        st.markdown(
            f"""
            <div style="
                background:white;
                padding:20px;
                border-radius:18px;
                border-top:5px solid #E20031;
                box-shadow:0 4px 12px rgba(0,0,0,0.08);
                text-align:center;
                margin-top:15px;
                margin-bottom:20px;
            ">

                <h3>{selected_food}</h3>

                <h2>{stars}</h2>

                <p><b>{avg}/5 Rating</b></p>

                <p>{votes} Votes</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        user_rating = st.feedback(
            "stars",
            key=f"rating_{key}"
        )

        if st.button(
            f"Submit Rating - {selected_food}",
            key=f"btn_{key}"
        ):

            if user_rating is not None:

                ratings_data[key]["total_rating"] += user_rating + 1

                ratings_data[key]["votes"] += 1

                save_data(ratings_data)

                st.success(
                    f"Successfully Rated {selected_food}"
                )

                st.rerun()

            else:

                st.warning("Please select stars first.")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Built for Tech Mahindra Smart Canteen Management System"
)
