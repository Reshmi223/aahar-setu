import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- SUPABASE CLOUD DATABASE CONFIGURATION WITH YOUR EXACT KEYS ---
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_PeDf0zC_6j8CjonEa1LB2Q_j3FQmvHy"

# Initialize Supabase Client Connection
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# --- DATABASE CORE OPERATIONS ---
def get_all_listings():
    try:
        response = supabase.table("food_listings").select("*").order("id").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Database Error: {e}")
        return []

def add_donation(donor, food_name, quantity, location, contact, cooked_time):
    new_item = {
        "donor": donor,
        "food": food_name,
        "quantity": int(quantity),
        "location": location,
        "contact": contact,
        "cooked_time": cooked_time.strftime("%Y-%m-%d %H:%M"),
        "status": "Available",
        "claimed_by": ""
    }
    supabase.table("food_listings").insert(new_item).execute()

def update_expiry_and_get_listings():
    listings = get_all_listings()
    current_time = datetime.now()
    
    for item in listings:
        if item["status"] == "Available":
            cooked_dt = datetime.strptime(item["cooked_time"], "%Y-%m-%d %H:%M")
            hours_passed = (current_time - cooked_dt).total_seconds() / 3600
            if hours_passed > 6:
                supabase.table("food_listings").update({"status": "Expired"}).eq("id", item["id"]).execute()
                
    return get_all_listings()

def claim_food(item_id, ngo_name):
    try:
        supabase.table("food_listings").update({"status": "Claimed", "claimed_by": ngo_name}).eq("id", item_id).execute()
        return True
    except:
        return False

# --- STREAMLIT WEB UI INTERFACE ---
st.set_page_config(page_title="Aahar Setu - Cloud DB", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu (Cloud-Powered Food Rescue)")
st.markdown("Connecting Surplus Food with Local NGOs. *Powered by Real-Time Supabase Postgre SQL Cloud DB.*")
st.divider()

all_items = update_expiry_and_get_listings()
tab1, tab2, tab3 = st.tabs(["🎁 Donate Food", "🔎 Available Food (NGO View)", "📋 Dashboard & Logs"])

with tab1:
    st.header("Register Extra Food Details")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Name")
            food_name = st.text_input("Food Menu Details")
            quantity = st.number_input("Serves How Many People?", min_value=1, step=1)
        with col2:
            location = st.text_area("Pickup Address")
            contact = st.text_input("Contact Mobile Number")
            cooked_time = st.slider("When was it cooked?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Submit Donation")
        if submit_btn:
            if donor and food_name and location and contact:
                add_donation(donor, food_name, quantity, location, contact, cooked_time)
                st.success("🎉 Success! Data pushed to Supabase Cloud Database.")
                st.rerun()
            else:
                st.error("⚠️ Fill out all mandatory fields.")

with tab2:
    st.header("Active Food Listings")
    available_items = [i for i in all_items if i["status"] == "Available"]
    
    if not available_items:
        st.info("No active food listings available in cloud right now.")
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
                                st.success("Food Reserved in Cloud!")
                                st.rerun()

with tab3:
    st.header("Network Statistics")
    total_listings = len(all_items)
    claimed_count = len([i for i in all_items if i["status"] == "Claimed"])
    expired_count = len([i for i in all_items if i["status"] == "Expired"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Cloud Listings", total_listings)
    m2.metric("Successful Rescues", claimed_count)
    m3.metric("Safety Timeouts", expired_count)
    
    st.divider()
    st.dataframe(all_items, use_container_width=True)
