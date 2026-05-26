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
    page_icon="🍽️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.cdnfonts.com/css/aptos');

html, body, [class*="css"] {
    font-family: 'Aptos', sans-serif !important;
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
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #b71c26;
}

/* CARDS */

.food-card, .admin-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 18px;
    border-left: 6px solid #D9232D;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

/* HORIZONTAL SCROLL CONTAINER (SWIPE LEFT FEATURE) */

.scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding: 10px 5px 20px 5px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: #D9232D #f0f0f0;
}

.scroll-container::-webkit-scrollbar {
    height: 8px;
}

.scroll-container::-webkit-scrollbar-track {
    background: #f0f0f0;
    border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-thumb {
    background-color: #D9232D;
    border-radius: 10px;
}

.scroll-card {
    min-width: 280px;
    flex: 0 0 auto;
    background: white;
    padding: 20px;
    border-radius: 18px;
    border-left: 6px solid #D9232D;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

.scroll-card h3, .scroll-card h4 {
    margin-top: 0;
    color: #111;
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

/* METRICS */
[data-testid="stMetricValue"] {
    color: #D9232D;
}

/* FEEDBACK */

[data-testid="stFeedback"] button {
    transform: scale(1.5);
    margin-right: 10px;
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
                    "high_ratings": 0, # Tracks 4 and 5 star ratings
                    "feedbacks": []
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
                if "high_ratings" not in fresh_data[key]:
                    fresh_data[key]["high_ratings"] = 0
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
        return "🟡 Neutral"

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
        return "🟢 Positive"
    elif negative_count > positive_count:
        return "🔴 Negative"
    else:
        return "🟡 Neutral"

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
# SIDEBAR CONTROLS
# ---------------------------------------------------

st.sidebar.title("Controls")

# Use a toggle for Admin view so it stays open
show_admin = st.sidebar.toggle("📊 Show Admin View")

# Reset Button (Clears JSON and Session State Inputs)
if st.sidebar.button("⚠️ Reset All Data & Inputs"):
    ratings_data = initialize_ratings()
    save_data(ratings_data)
    
    # Clear session state so UI inputs actually clear
    for key in st.session_state.keys():
        if key.startswith('feedback_') or key.startswith('text_') or key.endswith('_food'):
            del st.session_state[key]
            
    st.sidebar.success("All data and inputs reset successfully!")
    st.rerun()

st.sidebar.markdown("---")

selected_meal = st.sidebar.selectbox(
    "Select Meal Time",
    ["Breakfast", "Lunch", "Snacks", "Dinner"],
    index=["Breakfast", "Lunch", "Snacks", "Dinner"].index(auto_meal)
)

meal_data = default_data[selected_meal]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

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

# ---------------------------------------------------
# TOP 5 HIGHEST RATED (HORIZONTAL SCROLL)
# ---------------------------------------------------

st.markdown("## Top 5 Highest Rated Dishes")

top_dishes = []
for vendor, foods in meal_data.items():
    for food in foods:
        key = f"{selected_meal}|{vendor}|{food}"
        votes = ratings_data[key]["votes"]
        avg = (ratings_data[key]["total_rating"] / votes) if votes > 0 else 0
        top_dishes.append({
            "Food": food,
            "Vendor": vendor,
            "Rating": round(avg, 1)
        })

top_dishes = sorted(top_dishes, key=lambda x: x["Rating"], reverse=True)[:5]

scroll_html = '<div class="scroll-container">'
for idx, dish in enumerate(top_dishes):
    stars = "★" * int(round(dish["Rating"]))
    scroll_html += f"""<div class="scroll-card">
<h3>{idx+1}. {dish['Food']}</h3>
<p><b>{dish['Vendor']}</b></p>
<p style="font-size:22px; color:#D9232D; margin: 0;">{stars}</p>
<p style="margin-top: 5px;"><b>{dish['Rating']} / 5</b></p>
</div>"""
scroll_html += '</div>'

st.markdown(scroll_html, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# RATE FOOD SECTION
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
        avg = (ratings_data[key]["total_rating"] / votes) if votes > 0 else 0
        
        food_sentiment = analyze_sentiment(ratings_data[key].get("feedbacks", []))

        st.markdown(
            f"""
            <div class="food-card">
            <h3>{selected_food}</h3>
            <p><b>Vendor:</b> {vendor}</p>
            <p><b>Current Rating:</b> {round(avg,1)} / 5</p>
            <p><b>Total Orders:</b> {votes}</p>
            <p><b>Customer Sentiment:</b> {food_sentiment}</p>
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
            placeholder="Write your feedback here...",
            key=f"text_{key}"
        )

        if st.button(f"Submit Rating - {selected_food}", key=f"btn_{key}"):
            if user_rating is not None:
                actual_rating = user_rating + 1
                ratings_data[key]["total_rating"] += actual_rating
                ratings_data[key]["votes"] += 1
                
                if actual_rating >= 4:
                    ratings_data[key]["high_ratings"] += 1

                if user_text.strip() != "":
                    ratings_data[key]["feedbacks"].append(user_text)

                save_data(ratings_data)
                st.success("Feedback Submitted Successfully ✅")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please select a star rating.")

st.markdown("---")

# ---------------------------------------------------
# BEST SELLING DISHES (HORIZONTAL SCROLL)
# ---------------------------------------------------

st.markdown("## Best Selling Dish Of Each Vendor")

best_scroll_html = '<div class="scroll-container">'
for vendor in meal_data.keys():
    best_food = None
    best_votes = -1
    best_rating = 0

    for food in meal_data[vendor]:
        key = f"{selected_meal}|{vendor}|{food}"
        votes = ratings_data[key]["votes"]
        avg = (ratings_data[key]["total_rating"] / votes) if votes > 0 else 0

        if votes > best_votes:
            best_votes = votes
            best_food = food
            best_rating = round(avg, 1)
            
    best_scroll_html += f"""<div class="scroll-card">
<h4>{vendor}</h4>
<p style="font-size:18px; font-weight: 600; color: #D9232D;">{best_food}</p>
<p>Rating: <b>{best_rating} / 5</b></p>
<p>Total Orders: <b>{best_votes}</b></p>
</div>"""
best_scroll_html += '</div>'

st.markdown(best_scroll_html, unsafe_allow_html=True)

# ---------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------

if show_admin:
    st.markdown("---")
    st.markdown("## Admin Dashboard")

    vendor_orders = {}
    vendor_avg_ratings = {}
    vendor_satisfaction = {}
    total_system_orders = 0

    # Calculate Data
    for vendor, foods in meal_data.items():
        total_orders = 0
        total_rating_score = 0
        total_high_ratings = 0

        for food in foods:
            key = f"{selected_meal}|{vendor}|{food}"
            votes = ratings_data[key]["votes"]
            
            total_orders += votes
            total_rating_score += ratings_data[key]["total_rating"]
            total_high_ratings += ratings_data[key]["high_ratings"]

        avg_rating = (total_rating_score / total_orders) if total_orders > 0 else 0
        vendor_avg_ratings[vendor] = round(avg_rating, 2)
        
        satisfaction = (total_high_ratings / total_orders * 100) if total_orders > 0 else 0
        vendor_satisfaction[vendor] = round(satisfaction, 1)
        
        vendor_orders[vendor] = total_orders
        total_system_orders += total_orders

    # Mock calculations for wastage metrics based on orders (can be replaced with real backend logic later)
    # Assumes base stock of 50 per vendor over actual orders, and preventative measures saving 15%
    simulated_wastage_kg = max(0, ((len(vendors) * 50) - total_system_orders) * 0.2) 
    simulated_prevented_kg = total_system_orders * 0.15 

    # Top Level Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Orders Received", value=total_system_orders)
    m2.metric(label="Total Food Wastage (This Month)", value=f"{simulated_wastage_kg:.1f} kg", delta="-5% vs Last Month", delta_color="inverse")
    m3.metric(label="Food Wastage Prevented (This Month)", value=f"{simulated_prevented_kg:.1f} kg", delta="+12% Efficiency")

    st.markdown("---")

    st.markdown("### Total Orders Served by Vendor (Line Chart)")
    chart_data = pd.DataFrame({
        "Orders Served": list(vendor_orders.values())
    }, index=list(vendor_orders.keys()))
    st.line_chart(chart_data, color="#D9232D")

    st.markdown("### Vendor Performance Breakdown")
    admin_cols = st.columns(len(vendor_orders))
    for idx, vendor in enumerate(vendor_orders):
        with admin_cols[idx]:
            st.markdown(
                f"""
                <div class="admin-card">
                    <h4>{vendor}</h4>
                    <p><b>Avg Rating:</b> {vendor_avg_ratings[vendor]} / 5</p>
                    <p><b>Satisfaction:</b> {vendor_satisfaction[vendor]}%</p>
                    <p><b>Total Orders:</b> {vendor_orders[vendor]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("Built for Tech Mahindra Smart Canteen Management System")
