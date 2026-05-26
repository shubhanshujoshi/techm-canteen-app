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
    font-family: 'Aptos', sans-serif;
}

.sub-title {
    color: #555555;
    font-size: 16px;
    font-family: 'Aptos', sans-serif;
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
    font-family: 'Aptos', sans-serif;
}

.stButton > button:hover {
    background-color: #b71c26;
}

/* HORIZONTAL SCROLL WRAPPER */
.scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 18px;
    padding: 10px 4px 18px 4px;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: #D9232D #f0f0f0;
}

.scroll-container::-webkit-scrollbar {
    height: 6px;
}

.scroll-container::-webkit-scrollbar-thumb {
    background: #D9232D;
    border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-track {
    background: #f0f0f0;
    border-radius: 10px;
}

/* CARDS */
.food-card,
.top-card,
.best-card,
.admin-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 18px;
    border-left: 6px solid #D9232D;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    font-family: 'Aptos', sans-serif;
}

/* TOP RATED CARD (fixed width for horizontal scroll) */
.top-card {
    min-width: 200px;
    max-width: 200px;
    flex-shrink: 0;
    scroll-snap-align: start;
    margin-bottom: 0;
}

/* BEST SELLING CARD (fixed width for horizontal scroll) */
.best-card {
    min-width: 200px;
    max-width: 200px;
    flex-shrink: 0;
    scroll-snap-align: start;
    margin-bottom: 0;
}

/* ADMIN CARD */
.admin-card {
    min-width: 180px;
    max-width: 220px;
    flex-shrink: 0;
    scroll-snap-align: start;
    margin-bottom: 0;
}

/* SENTIMENT BADGE */
.badge-positive {
    display: inline-block;
    background: #e6f9ee;
    color: #1a7a40;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
    border: 1px solid #1a7a40;
}

.badge-negative {
    display: inline-block;
    background: #fde8e8;
    color: #D9232D;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
    border: 1px solid #D9232D;
}

.badge-neutral {
    display: inline-block;
    background: #fff9e6;
    color: #996600;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
    border: 1px solid #996600;
}

/* TABS */
.stTabs [data-baseweb="tab"] {
    color: #D9232D;
    font-weight: 600;
    font-family: 'Aptos', sans-serif;
}

.stTabs [aria-selected="true"] {
    background-color: #D9232D !important;
    color: white !important;
    border-radius: 10px;
}

/* FEEDBACK */
[data-testid="stFeedback"] button {
    transform: scale(1.5);
    margin-right: 10px;
}

/* FOOTER */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }

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
                    "star_counts": [0, 0, 0, 0, 0]   # index 0=1star … 4=5star
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
                if "star_counts" not in fresh_data[key]:
                    fresh_data[key]["star_counts"] = [0, 0, 0, 0, 0]
    except Exception:
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

positive_words = [
    "good", "great", "excellent", "amazing", "awesome",
    "tasty", "love", "nice", "best", "fresh", "fantastic",
    "delicious", "yummy", "superb", "perfect", "enjoyed",
    "wonderful", "brilliant", "outstanding", "satisfying"
]

negative_words = [
    "bad", "worst", "cold", "stale", "awful", "hate",
    "poor", "dirty", "disgusting", "late", "waste",
    "terrible", "horrible", "pathetic", "rotten", "bland",
    "overpriced", "undercooked", "overcooked", "salty", "spicy"
]


def analyze_sentiment(feedbacks):
    if not feedbacks:
        return "neutral", "🟡 Neutral"

    pos = 0
    neg = 0

    for feedback in feedbacks:
        fb = feedback.lower()
        for w in positive_words:
            if w in fb:
                pos += 1
        for w in negative_words:
            if w in fb:
                neg += 1

    if pos > neg:
        return "positive", "🟢 Positive"
    elif neg > pos:
        return "negative", "🔴 Negative"
    else:
        return "neutral", "🟡 Neutral"


def sentiment_badge(label_text):
    if "Positive" in label_text:
        return f'<span class="badge-positive">{label_text}</span>'
    elif "Negative" in label_text:
        return f'<span class="badge-negative">{label_text}</span>'
    else:
        return f'<span class="badge-neutral">{label_text}</span>'


# ---------------------------------------------------
# SATISFACTION % (4 & 5 star votes)
# ---------------------------------------------------

def satisfaction_percent(vendor, meal, data):
    total_votes = 0
    satisfied_votes = 0
    for food in default_data[meal][vendor]:
        key = f"{meal}|{vendor}|{food}"
        sc = data[key].get("star_counts", [0, 0, 0, 0, 0])
        satisfied_votes += sc[3] + sc[4]   # 4-star + 5-star
        total_votes += data[key]["votes"]
    if total_votes == 0:
        return 0
    return round((satisfied_votes / total_votes) * 100, 1)


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

show_admin = st.sidebar.button("👁️ Admin View")

if st.sidebar.button("🔄 Reset All Ratings"):
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

col1, col2 = st.columns([1, 7])

with col1:
    st.image("logo.png", width=80)

with col2:
    st.markdown(
        '<div class="main-title">Tech Mahindra Smart Canteen</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="sub-title">Intelligent Food Experience & Feedback Platform'
        f'<br>Currently Serving: <b>{selected_meal}</b></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# TOP 5 HIGHEST RATED  (horizontal scroll)
# ---------------------------------------------------

st.markdown("## 🏆 Top 5 Highest Rated Dishes")

top_dishes = []

for vendor, foods in meal_data.items():
    for food in foods:
        key = f"{selected_meal}|{vendor}|{food}"
        votes = ratings_data[key]["votes"]
        avg = ratings_data[key]["total_rating"] / votes if votes > 0 else 0
        _, sentiment_label = analyze_sentiment(ratings_data[key]["feedbacks"])
        top_dishes.append({
            "Food": food,
            "Vendor": vendor,
            "Rating": round(avg, 1),
            "Votes": votes,
            "Sentiment": sentiment_label
        })

top_dishes = sorted(top_dishes, key=lambda x: x["Rating"], reverse=True)[:5]

cards_html = '<div class="scroll-container">'
for idx, dish in enumerate(top_dishes):
    stars = "★" * int(round(dish["Rating"])) + "☆" * (5 - int(round(dish["Rating"])))
    badge = sentiment_badge(dish["Sentiment"])
    cards_html += f"""
    <div class="top-card">
        <h3 style="font-size:16px; margin:0 0 6px 0; color:#D9232D;">#{idx+1} {dish['Food']}</h3>
        <p style="margin:4px 0; font-size:13px; color:#555;"><b>{dish['Vendor']}</b></p>
        <p style="font-size:20px; color:#D9232D; margin:6px 0;">{stars}</p>
        <p style="margin:4px 0;"><b>{dish['Rating']}/5</b> &nbsp;·&nbsp; {dish['Votes']} orders</p>
        <p style="margin:6px 0;">{badge}</p>
    </div>
    """
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# RATE FOOD SECTION
# ---------------------------------------------------

st.markdown("## ⭐ Rate Food Item")

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
        avg = ratings_data[key]["total_rating"] / votes if votes > 0 else 0
        _, sent_label = analyze_sentiment(ratings_data[key]["feedbacks"])
        badge_html = sentiment_badge(sent_label)

        st.markdown(
            f"""
            <div class="food-card">
                <h3>{selected_food}</h3>
                <p><b>Vendor:</b> {vendor}</p>
                <p><b>Rating:</b> {round(avg,1)}/5 &nbsp;|&nbsp; <b>Total Orders:</b> {votes}</p>
                <p><b>Sentiment:</b> {badge_html}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_rating = st.feedback("stars", key=f"feedback_{key}")

        user_text = st.text_area(
            "Optional Feedback",
            placeholder="Write your feedback here...",
            key=f"text_{key}"
        )

        if st.button(f"Submit Rating – {selected_food}", key=f"btn_{key}"):
            if user_rating is not None:
                star_value = user_rating + 1   # 0-indexed → 1-5
                ratings_data[key]["total_rating"] += star_value
                ratings_data[key]["votes"] += 1
                ratings_data[key]["star_counts"][user_rating] += 1

                if user_text.strip():
                    ratings_data[key]["feedbacks"].append(user_text.strip())

                save_data(ratings_data)
                st.success("Feedback Submitted Successfully ✅")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please select a star rating before submitting.")

st.markdown("---")

# ---------------------------------------------------
# BEST SELLING DISH OF EACH VENDOR  (horizontal scroll)
# ---------------------------------------------------

st.markdown("## 🥇 Best Selling Dish Of Each Vendor")

best_cards_html = '<div class="scroll-container">'

for vendor in meal_data.keys():
    best_food = None
    best_votes = -1
    best_rating = 0

    for food in meal_data[vendor]:
        key = f"{selected_meal}|{vendor}|{food}"
        votes = ratings_data[key]["votes"]
        avg = ratings_data[key]["total_rating"] / votes if votes > 0 else 0
        if votes > best_votes:
            best_votes = votes
            best_food = food
            best_rating = round(avg, 1)

    stars = "★" * int(round(best_rating)) + "☆" * (5 - int(round(best_rating)))

    best_cards_html += f"""
    <div class="best-card">
        <h4 style="color:#D9232D; margin:0 0 8px 0;">{vendor}</h4>
        <p style="font-weight:700; font-size:15px; margin:4px 0;">{best_food}</p>
        <p style="font-size:18px; color:#D9232D; margin:4px 0;">{stars}</p>
        <p style="margin:4px 0;">Rating: <b>{best_rating}/5</b></p>
        <p style="margin:4px 0;">Orders: <b>{best_votes}</b></p>
    </div>
    """

best_cards_html += '</div>'
st.markdown(best_cards_html, unsafe_allow_html=True)

# ---------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------

if show_admin:

    st.markdown("---")
    st.markdown("## 🛠️ Admin Dashboard")

    vendor_orders = {}
    avg_vendor_rating = {}
    satisfaction_pct = {}
    sentiment_map = {}

    for vendor, foods in meal_data.items():
        total_orders = 0
        total_rating_sum = 0
        all_feedbacks = []

        for food in foods:
            key = f"{selected_meal}|{vendor}|{food}"
            v = ratings_data[key]["votes"]
            total_orders += v
            total_rating_sum += ratings_data[key]["total_rating"]
            all_feedbacks.extend(ratings_data[key].get("feedbacks", []))

        vendor_orders[vendor] = total_orders

        avg_vendor_rating[vendor] = (
            round(total_rating_sum / total_orders, 1)
            if total_orders > 0 else 0
        )

        satisfaction_pct[vendor] = satisfaction_percent(vendor, selected_meal, ratings_data)

        _, sent_label = analyze_sentiment(all_feedbacks)
        sentiment_map[vendor] = sent_label

    # ---- Vendor Performance Cards (horizontal scroll) ----
    st.markdown("### Vendor Performance")

    admin_cards_html = '<div class="scroll-container">'
    for vendor in vendor_orders:
        badge = sentiment_badge(sentiment_map[vendor])
        stars = "★" * int(round(avg_vendor_rating[vendor])) + "☆" * (5 - int(round(avg_vendor_rating[vendor])))
        sat = satisfaction_pct[vendor]
        sat_color = "#1a7a40" if sat >= 70 else ("#D9232D" if sat < 40 else "#996600")

        admin_cards_html += f"""
        <div class="admin-card">
            <h4 style="color:#D9232D; margin:0 0 10px 0;">{vendor}</h4>
            <p style="margin:4px 0;"><b>Avg Rating</b></p>
            <p style="font-size:18px; color:#D9232D; margin:2px 0;">{stars}</p>
            <p style="margin:2px 0; font-size:13px;">{avg_vendor_rating[vendor]}/5</p>
            <hr style="border:none; border-top:1px solid #eee; margin:8px 0;">
            <p style="margin:4px 0;"><b>Satisfaction</b></p>
            <p style="color:{sat_color}; font-size:22px; font-weight:700; margin:2px 0;">{sat}%</p>
            <p style="font-size:11px; color:#888; margin:0;">Based on 4★ & 5★ reviews</p>
            <hr style="border:none; border-top:1px solid #eee; margin:8px 0;">
            <p style="margin:4px 0;"><b>Total Orders:</b> {vendor_orders[vendor]}</p>
            <p style="margin:4px 0;"><b>Sentiment:</b> {badge}</p>
        </div>
        """
    admin_cards_html += '</div>'
    st.markdown(admin_cards_html, unsafe_allow_html=True)

    # ---- Orders Line Chart ----
    st.markdown("### 📈 Total Orders Served – Vendor Comparison")

    chart_df = pd.DataFrame({
        "Vendor": list(vendor_orders.keys()),
        "Total Orders": list(vendor_orders.values())
    }).set_index("Vendor")

    st.line_chart(chart_df)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("Built for Tech Mahindra Smart Canteen Management System")
