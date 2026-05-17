import streamlit as st
from datetime import datetime
import json
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Tech Mahindra Smart Canteen",
    page_icon="logo.png",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* =====================================================
LIGHT MODE
===================================================== */

.stApp {
    background-color: #f5f5f5;
    color: #111111;
}

/* TITLE */

.main-title {
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(90deg, #E20031, #ff4d6d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    color: #555555;
    font-size: 16px;
}

/* CARD */

.card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    border-top: 5px solid #E20031;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    min-width: 240px;
    flex-shrink: 0;
    color: #111111;
}

/* FEEDBACK CARD */

.feedback-card {
    background: white;
    border-left: 5px solid #E20031;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 14px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
}

/* SCROLL */

.scroll-row {
    display: flex;
    overflow-x: auto;
    gap: 16px;
    padding-bottom: 10px;
    scroll-behavior: smooth;
}

.scroll-row::-webkit-scrollbar {
    height: 8px;
}

.scroll-row::-webkit-scrollbar-thumb {
    background: #E20031;
    border-radius: 10px;
}

/* BUTTON */

.stButton > button {
    background-color: #E20031;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #b80028;
    color: white;
}

/* BIG STARS */

[data-testid="stFeedback"] button {
    transform: scale(1.7);
    margin-right: 10px;
}

/* =====================================================
DARK MODE
===================================================== */

@media (prefers-color-scheme: dark) {

    .stApp {
        background-color: #111111 !important;
        color: white !important;
    }

    html, body, p, h1, h2, h3, h4, h5, h6,
    label, span, div {
        color: white !important;
    }

    .sub-title {
        color: #cccccc !important;
    }

    .card {
        background: #1e1e1e !important;
        color: white !important;
        box-shadow: 0px 4px 12px rgba(255,255,255,0.05);
    }

    .feedback-card {
        background: #1e1e1e !important;
        color: white !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e1e1e !important;
        color: white !important;
    }

    .stTextArea textarea {
        background-color: #1e1e1e !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
}

/* =====================================================
MOBILE
===================================================== */

@media (max-width: 768px) {

    .main-title {
        font-size: 26px;
    }

    .card {
        min-width: 85%;
    }

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FILES
# =====================================================

DATA_FILE = "ratings_data.json"
FEEDBACK_FILE = "food_feedback.json"

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
                    "votes": 0
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

    with open(DATA_FILE, "r") as f:
        existing_data = json.load(f)

    for key in existing_data:

        if key in fresh_data:
            fresh_data[key] = existing_data[key]

    return fresh_data

# =====================================================
# SAVE DATA
# =====================================================

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

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

st.sidebar.title("Meal Filters")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(auto_meal)
)

# RESET BUTTON

if st.sidebar.button("Reset All Ratings"):

    ratings_data = initialize_ratings()

    save_data(ratings_data)

    st.sidebar.success("All ratings have been reset successfully")

    st.rerun()

meal_data = default_data[selected_meal]

# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([1, 8])

with col1:
    st.image("logo.png", width=70)

with col2:

    st.markdown("""
<div class="main-title">
Tech Mahindra Smart Canteen
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="sub-title">
Currently Serving: <b>{selected_meal}</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# TOP 5
# =====================================================

st.markdown("## Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        votes = ratings_data[key]["votes"]
        total = ratings_data[key]["total_rating"]

        avg = round(total / votes, 1) if votes > 0 else 0

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

html = '<div class="scroll-row">'

for dish in top_dishes:

    stars = "⭐" * int(round(dish["rating"]))

    html += f'''
<div class="card">
<h3>{dish["food"]}</h3>
<p><b>{dish["vendor"]}</b></p>
<h2>{stars}</h2>
<p>{dish["rating"]}/5</p>
</div>
'''

html += '</div>'

st.markdown(html, unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# FEEDBACK SECTION
# =====================================================

st.markdown("## Food Feedback")

vendors = list(meal_data.keys())

tabs = st.tabs(vendors)

for tab, vendor in zip(tabs, vendors):

    with tab:

        foods = meal_data[vendor]

        selected_food = st.selectbox(
            f"Select Food - {vendor}",
            foods,
            key=f"feedback_{vendor}"
        )

        feedback_text = st.text_area(
            "Write Your Feedback",
            placeholder="Taste, hygiene, quality etc.",
            key=f"text_{vendor}"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                f"Submit Feedback - {vendor}",
                key=f"btn_feedback_{vendor}"
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

        with col2:

            show_feedback = st.button(
                f" Recent Feedbacks - {vendor}",
                key=f"recent_feedback_{vendor}"
            )

        if show_feedback:

            if os.path.exists(FEEDBACK_FILE):

                with open(FEEDBACK_FILE, "r") as f:
                    feedback_data = json.load(f)

                vendor_feedbacks = [
                    x for x in reversed(feedback_data)
                    if x["vendor"] == vendor
                ]

                if vendor_feedbacks:

                    st.markdown("### Recent Customer Feedbacks")

                    for item in vendor_feedbacks[:5]:

                        st.markdown(f"""
<div class="feedback-card">

<h4>{item["food"]}</h4>

<p><b>Vendor:</b> {item["vendor"]}</p>

<p>{item["feedback"]}</p>

<p style="font-size:12px; opacity:0.7;">
{item["time"][:19]}
</p>

</div>
""", unsafe_allow_html=True)

                else:

                    st.info("No feedback available yet.")

st.markdown("---")

# =====================================================
# BEST SELLERS
# =====================================================

st.markdown("## Best Selling Food Item Of Each Vendor")

best_sellers = []

for vendor, foods in meal_data.items():

    best_food = None
    best_votes = -1
    best_rating = 0

    for food in foods:

        key = f"{selected_meal}|{vendor}|{food}"

        votes = ratings_data[key]["votes"]
        total = ratings_data[key]["total_rating"]

        avg = round(total / votes, 1) if votes > 0 else 0

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

html = '<div class="scroll-row">'

for item in best_sellers:

    stars = "⭐" * int(round(item["rating"]))

    html += f'''
<div class="card">
<h3>{item["vendor"]}</h3>
<p><b>{item["food"]}</b></p>
<h2>{stars}</h2>
<p>{item["rating"]}/5</p>
<p>{item["votes"]} Votes</p>
</div>
'''

html += '</div>'

st.markdown(html, unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# RATE FOOD
# =====================================================

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

        votes = ratings_data[key]["votes"]
        total = ratings_data[key]["total_rating"]

        avg = round(total / votes, 1) if votes > 0 else 0

        stars = "⭐" * int(round(avg))

        st.markdown(f'''
<div class="card">
<h3>{selected_food}</h3>
<h2>{stars}</h2>
<p><b>{avg}/5 Rating</b></p>
<p>{votes} Votes</p>
</div>
''', unsafe_allow_html=True)

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

                st.warning(
                    "Please select stars first."
                )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Built for Tech Mahindra Smart Canteen Management System"
)
