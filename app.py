import streamlit as st
import json
import os
from datetime import datetime

DB_FILE = "food_rescue_db.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)

def get_all_listings():
    init_db()
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_listings(listings):
    with open(DB_FILE, 'w') as f:
        json.dump(listings, f, indent=4)

def add_donation(donor, food_name, quantity, location, contact, cooked_time):
    listings = get_all_listings()
    new_item = {
        "id": len(listings) + 1,
        "donor": donor,
        "food": food_name,
        "quantity": int(quantity),
        "location": location,
        "contact": contact,
        "cooked_time": cooked_time.strftime("%Y-%m-%d %H:%M"),
        "status": "Available",
        "claimed_by": ""
    }
    listings.append(new_item)
    save_listings(listings)

def update_expiry_and_get_listings():
    listings = get_all_listings()
    updated = False
    current_time = datetime.now()
    
    for item in listings:
        if item["status"] == "Available":
            cooked_dt = datetime.strptime(item["cooked_time"], "%Y-%m-%d %H:%M")
            hours_passed = (current_time - cooked_dt).total_seconds() / 3600
            if hours_passed > 6:
                item["status"] = "Expired"
                updated = True
                
    if updated:
        save_listings(listings)
    return listings

def claim_food(item_id, ngo_name):
    listings = get_all_listings()
    for item in listings:
        if item["id"] == item_id and item["status"] == "Available":
            item["status"] = "Claimed"
            item["claimed_by"] = ngo_name
            save_listings(listings)
            return True
    return False

st.set_page_config(page_title="Aahar Setu - Food Rescue", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu (Food Rescue Network)")
st.markdown("Connecting Extra Food Donors with Local NGOs to End Hunger. *Safe. Transparent. Impactful.*")
st.divider()

all_items = update_expiry_and_get_listings()
tab1, tab2, tab3 = st.tabs(["🎁 Donate Food", "🔎 Available Food (NGO View)", "📋 Dashboard & Logs"])

with tab1:
    st.header("Register Extra Food Details")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Name (e.g., Star Hotel, Annai Mandapam)")
            food_name = st.text_input("Food Menu (e.g., Veg Biryani, Rice & Sambar)")
            quantity = st.number_input("Serves How Many People? (Count)", min_value=1, step=1)
        with col2:
            location = st.text_area("Pickup Address")
            contact = st.text_input("Contact Mobile Number")
            cooked_time = st.slider("When was it cooked?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Submit Donation Listing")
        if submit_btn:
            if donor and food_name and location and contact:
                add_donation(donor, food_name, quantity, location, contact, cooked_time)
                st.success("🎉 Success! Your donation entry is live on the NGO dashboard.")
                st.rerun()
            else:
                st.error("⚠️ Please fill out all mandatory fields before submitting.")

with tab2:
    st.header("Active Food Listings in Your Area")
    available_items = [i for i in all_items if i["status"] == "Available"]
    
    if not available_items:
        st.info("No active food listings available right now. Check back soon!")
    else:
        for item in available_items:
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.subheader(f"🍱 {item['food']}")
                    st.write(f"**From:** {item['donor']} | **Feeds:** {item['quantity']} people")
                    st.caption(f"Cooked on: {item['cooked_time']}")
                with c2:
                    st.write(f"📍 **Address:** {item['location']}")
                    st.write(f"📞 **Contact:** {item['contact']}")
                with c3:
                    ngo_name = st.text_input("Enter NGO Name", key=f"ngo_{item['id']}")
                    if st.button("Claim Food", key=f"btn_{item['id']}"):
                        if ngo_name:
                            if claim_food(item["id"], ngo_name):
                                st.success(f"Reserved for {ngo_name}!")
                                st.rerun()
                        else:
                            st.warning("Enter NGO name first")

with tab3:
    st.header("Network Statistics")
    total_listings = len(all_items)
    claimed_count = len([i for i in all_items if i["status"] == "Claimed"])
    expired_count = len([i for i in all_items if i["status"] == "Expired"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Food Listings", total_listings)
    m2.metric("Successful Rescues (Claimed)", claimed_count)
    m3.metric("Safety Timeouts (Expired)", expired_count)
    
    st.divider()
    st.subheader("All Transaction History Log")
    st.dataframe(all_items, use_container_width=True)
