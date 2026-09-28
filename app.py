import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- SUPABASE CLOUD DATABASE CONFIGURATION WITH DYNAMIC QUERIES ---
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_PeDf0zC_6j8CjonEa1LB2Q_j3FQmvHy"

@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        return None

supabase: Client = init_supabase()

def get_all_listings():
    if not supabase:
        return []
    try:
        response = supabase.table("food_listings").select("*").execute()
        if hasattr(response, 'data') and response.data is not None:
            return response.data
        return []
    except Exception as e:
        return []

def add_donation(donor, food_name, quantity, location, contact, cooked_time):
    if not supabase:
        return False
    try:
        new_item = {
            "donor": str(donor),
            "food": str(food_name),
            "quantity": str(quantity),
            "location": str(location),
            "contact": str(contact),
            "cooked_time": cooked_time.strftime("%Y-%m-%d %H:%M"),
            "status": "Available",
            "claimed_by": ""
        }
        supabase.table("food_listings").insert(new_item).execute()
        return True
    except Exception as e:
        return False

def claim_food(item_id, ngo_name):
    if not supabase:
        return False
    try:
        supabase.table("food_listings").update({"status": "Claimed", "claimed_by": str(ngo_name)}).eq("id", int(item_id)).execute()
        return True
    except Exception as e:
        return False

# --- STREAMLIT UI DESIGN PLATFORM ---
st.set_page_config(page_title="Aahar Setu - Core Engine", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu (Cloud-Powered Food Rescue Network)")
st.markdown("Connecting Surplus Food Donors with Local NGOs. *Stable Production Architecture.*")
st.divider()

all_items = get_all_listings()
tab1, tab2, tab3 = st.tabs(["🎁 Donate Food Platform", "🔎 Available Food (NGO View Tracker)", "📋 System Transaction Logs"])

with tab1:
    st.header("Register Surplus Food Entry Details")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Name")
            food_name = st.text_input("Food Item Details Menu")
            quantity = st.text_input("Serves How Many People? (e.g., 50 peruku)")
        with col2:
            location = st.text_area("Pickup Address Location")
            contact = st.text_input("Contact Mobile Phone Number")
            cooked_time = st.slider("When was it cooked timestamp?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Publish Donation Entry")
        if submit_btn:
            if donor and food_name and location and contact:
                if add_donation(donor, food_name, quantity, location, contact, cooked_time):
                    st.success("🎉 Transaction Completed! Data pushed securely into Supabase Production Cloud Database.")
                    st.rerun()
            else:
                st.error("⚠️ Please fill out all configuration form input fields.")

with tab2:
    st.header("Active Real-Time Food Rescue Listings")
    available_items = [i for i in all_items if isinstance(i, dict) and str(i.get("status")).strip().lower() == "available"]
                
    if not available_items:
        st.info("No active verified food entries found on cloud database right now.")
    else:
        for item in available_items:
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.subheader(f"🍱 {item.get('food', 'N/A')}")
                    st.write(f"**From Organization Source:** {item.get('donor', 'N/A')}")
                    st.write(f"**Feeds Capacity:** {item.get('quantity', 'N/A')} individuals")
                    st.caption(f"Cooked on: {item.get('cooked_time', 'N/A')}")
                with c2:
                    st.write(f"📍 **Pickup Location Address:** {item.get('location', 'N/A')}")
                    st.write(f"📞 **Active Phone Number Field:** {item.get('contact', 'N/A')}")
                with c3:
                    ngo_name_input = st.text_input("Enter Registered Volunteer / NGO Organization Name", key=f"ngo_field_{item.get('id', 0)}")
                    if st.button("Lock and Claim Food Rescue Package Allocation", key=f"btn_action_claim_trigger_{item.get('id', 0)}"):
                        if ngo_name_input:
                            if claim_food(item.get('id'), ngo_name_input):
                                st.success("🎉 Success! Row state successfully locked to target NGO.")
                                st.rerun()
                        else:
                            st.warning("⚠️ NGO identity field cannot be kept blank.")

with tab3:
    st.header("Global Network Cloud Operations Analytics Log")
    total_listings = len(all_items)
    claimed_count = len([i for i in all_items if isinstance(i, dict) and str(i.get("status")).strip().lower() == "claimed"])
    expired_count = len([i for i in all_items if isinstance(i, dict) and str(i.get("status")).strip().lower() == "expired"])
                    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Consolidated Cloud Transactions Listings", total_listings)
    m2.metric("Successful Active Food Rescues Allocation States", claimed_count)
    m3.metric("Safety Timeout Control State Blocks (Expired)", expired_count)
    
    st.divider()
    st.subheader("System Architecture Relational Row Matrix Dataset Logs Grid")
    if all_items:
        st.dataframe(all_items, use_container_width=True)
    else:
        st.info("System database analytics matrix datalog interface report dashboard is completely empty right now.")
