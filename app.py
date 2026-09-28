import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- AUTOMATIC INTEGRATION WITH YOUR EXACT DATABASE URL & KEY ---
SUPABASE_URL = "https://nqvjrapatfdvvjfxogkl.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_PeDf0zC_6j8CjonEa1LB2Q_j3FQmvHy"
@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        return None

supabase: Client = init_supabase()

# --- DATABASE CORE PERSISTENCE OPERATIONS ---
def get_all_listings():
    if not supabase:
        return []
    try:
        response = supabase.table("food_listings").select("*").execute()
        if hasattr(response, 'data') and response.data is not None:
            return response.data
        elif isinstance(response, dict) and "data" in response:
            return response["data"]
        return []
    except Exception as e:
        return []

def add_donation(donor, food_name, quantity, location, contact, cooked_time):
    if not supabase:
        return False
    try:
        new_item = {
            "donor": str(donor).strip(),
            "food": str(food_name).strip(),
            "quantity": str(quantity).strip(), 
            "location": str(location).strip(),
            "contact": str(contact).strip(),
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
        supabase.table("food_listings").update({
            "status": "Claimed", 
            "claimed_by": str(ngo_name).strip()
        }).eq("id", int(item_id)).execute()
        return True
    except Exception as e:
        return False

# --- WEB APPLICATION RENDERING INTERFACE ---
st.set_page_config(page_title="Aahar Setu - Enterprise Node", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu")
st.markdown("Rescue Extra Food. Feed Local Communities. Connecting Donors and NGOs Instantly to Prevent Food Waste.")
st.divider()

all_items = get_all_listings()

tab1, tab2, tab3 = st.tabs([
    "🎁 Donate Food Platform ", 
    "🔎 Active Food Rescue Listings (NGO Real-Time View Tracker)", 
    "📋 Transactions Analytics Log Dashboard"
])

with tab1:
    st.header("Donate Extra Food Details Form")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Name")
            food_name = st.text_input("Food Item Details Menu Package Description")
            quantity = st.text_input("Serves How Many Individuals Capacity Metrics")
        with col2:
            location = st.text_area("Pickup Address")
            contact = st.text_input("Active Phone Verification Mobile Network Number")
            cooked_time = st.slider("When was it cooked timestamp?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Publish Donation Entry Payload")
        if submit_btn:
            if donor and food_name and location and contact and quantity:
                if add_donation(donor, food_name, quantity, location, contact, cooked_time):
                    st.success("🎉 Transaction Completed! Data payload pushed securely into Supabase Production Cloud Database.")
                    st.rerun()
            else:
                st.error("⚠️ Mandatory fields missing! Please fill out all form input fields.")

with tab2:
    st.header("Active Real-Time Food Rescue Listings Available in Your Area Zone")
    
    available_items = []
    if all_items and isinstance(all_items, list):
        for idx_item in all_items:
            if isinstance(idx_item, dict):
                status_str = str(idx_item.get("status", "")).strip().lower()
                if status_str == "available" or status_str == "":
                    available_items.append(idx_item)
                    
    if not available_items:
        st.info("No active verified food entries found on cloud pipeline. Register a donation listing input to verify data stream logs!")
    else:
        for item in available_items:
            item_id_val = item.get("id")
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.subheader(f"🍱 {item.get('food', 'N/A')}")
                    st.write(f"**From Organization Source Location:** {item.get('donor', 'N/A')}")
                    st.write(f"**Feeds Capacity Metrics Value:** {item.get('quantity', 'N/A')} individuals")
                    st.caption(f"Network system log timestamp: {item.get('cooked_time', 'N/A')}")
                with c2:
                    st.write(f"📍 **Pickup Location Address:** {item.get('location', 'N/A')}")
                    st.write(f"📞 **Active Phone Verification Number:** {item.get('contact', 'N/A')}")
                with c3:
                    ngo_name_input = st.text_input("Enter Volunteer / NGO Identity Name", key=f"ngo_field_ref_index_key_{item_id_val}")
                    if st.button("Lock and Claim Food Rescue Package Allocation", key=f"btn_action_claim_trigger_ref_index_key_{item_id_val}"):
                        if ngo_name_input and item_id_val is not None:
                            if claim_food(item_id_val, ngo_name_input):
                                st.success("🎉 Success! Core row state successfully locked and mapped to target NGO.")
                                st.rerun()
                        else:
                            st.warning("⚠️ NGO identity field cannot be kept blank.")

with tab3:
    st.header("Global Network Cloud Operations Analytics Log Dashboard")
    
    total_listings = 0
    claimed_count = 0
    expired_count = 0
    
    if all_items and isinstance(all_items, list):
        total_listings = len(all_items)
        for idx_stat in all_items:
            if isinstance(idx_stat, dict):
                status_stat_str = str(idx_stat.get("status", "")).strip().lower()
                if status_stat_str == "claimed":
                    claimed_count += 1
                elif status_stat_str == "expired":
                    expired_count += 1
                    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Consolidated Cloud Transactions Listings", total_listings)
    m2.metric("Successful Active Food Rescues Allocation States", claimed_count)
    m3.metric("Safety Timeout Control State Blocks (Expired)", expired_count)
    
    st.divider()
    st.subheader("System Architecture Relational Row Matrix Dataset Logs Grid")
    
    if all_items and isinstance(all_items, list) and len(all_items) > 0:
        st.dataframe(all_items, use_container_width=True)
    else:
        st.info("System database dashboard is completely empty right now.")
