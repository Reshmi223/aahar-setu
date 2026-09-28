import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- SUPABASE CLOUD DATABASE CONFIGURATION WITH YOUR EXACT FULL URL ---
SUPABASE_URL = "https://nqvjrapatfdvvjfxogkl.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_PeDf0zC_6j8CjonEa1LB2Q_j3FQmvHy"

# Initialize Supabase Client Connection Safely
@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        return None

supabase: Client = init_supabase()

# --- DATABASE CORE OPERATIONS ---
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
            "donor": str(donor),
            "food": str(food_name),
            "quantity": int(quantity),
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

def update_expiry_and_get_listings():
    listings = get_all_listings()
    if not listings:
        return []
    current_time = datetime.now()
    
    for item in listings:
        if isinstance(item, dict) and item.get("status") == "Available" and item.get("cooked_time"):
            try:
                cooked_dt = datetime.strptime(item["cooked_time"], "%Y-%m-%d %H:%M")
                hours_passed = (current_time - cooked_dt).total_seconds() / 3600
                if hours_passed > 6:
                    supabase.table("food_listings").update({"status": "Expired"}).eq("id", item["id"]).execute()
            except:
                pass
                
    return get_all_listings()

def claim_food(item_id, ngo_name):
    if not supabase:
        return False
    try:
        supabase.table("food_listings").update({"status": "Claimed", "claimed_by": str(ngo_name)}).eq("id", int(item_id)).execute()
        return True
    except Exception as e:
        return False

# --- STREAMLIT WEB UI INTERFACE ---
st.set_page_config(page_title="Aahar Setu - Production Engine", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu (Cloud-Powered Food Rescue Network)")
st.markdown("Connecting Surplus Food Donors with Local NGOs. *Stable High-Level Infrastructure.*")
st.divider()

all_items = update_expiry_and_get_listings()
tab1, tab2, tab3 = st.tabs(["🎁 Donate Food Platform", "🔎 Available Food (NGO View)", "📋 Dashboard Logs"])

with tab1:
    st.header("Register Surplus Food Details")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Name")
            food_name = st.text_input("Food Item Details")
            quantity = st.number_input("Serves How Many People?", min_value=1, step=1)
        with col2:
            location = st.text_area("Surplus Food Pickup Address")
            contact = st.text_input("Contact Phone Number")
            cooked_time = st.slider("When was it cooked?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Publish Donation Entry")
        if submit_btn:
            if donor and food_name and location and contact:
                if add_donation(donor, food_name, quantity, location, contact, cooked_time):
                    st.success("🎉 Success! Data pushed securely into Supabase Cloud Database.")
                    st.rerun()
            else:
                st.error("⚠️ Please fill out all mandatory fields.")

with tab2:
    st.header("Active Food Rescue Listings")
    available_items = [i for i in all_items if isinstance(i, dict) and i.get("status") == "Available"]
                
    if not available_items:
        st.info("No active verified food entries found right now. Check back shortly!")
    else:
        for item in available_items:
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.subheader(f"🍱 {item.get('food', 'N/A')}")
                    st.write(f"**From:** {item.get('donor', 'N/A')} | **Feeds:** {item.get('quantity', 0)} people")
                    st.caption(f"Cooked on: {item.get('cooked_time', 'N/A')}")
                with c2:
                    st.write(f"📍 **Address:** {item.get('location', 'N/A')}")
                    st.write(f"📞 **Contact:** {item.get('contact', 'N/A')}")
                with c3:
                    ngo_name_input = st.text_input("Enter NGO Name", key=f"ngo_field_{item.get('id', 0)}")
                    if st.button("Lock and Claim Food", key=f"btn_claim_{item.get('id', 0)}"):
                        if ngo_name_input:
                            if claim_food(item.get('id'), ngo_name_input):
                                st.success("🎉 Success! Food claimed successfully.")
                                st.rerun()
                        else:
                            st.warning("⚠️ NGO name cannot be blank.")

with tab3:
    st.header("Global Network Cloud Operations Analytics")
    total_listings = len(all_items)
    claimed_count = len([i for i in all_items if isinstance(i, dict) and i.get("status") == "Claimed"])
    expired_count = len([i for i in all_items if isinstance(i, dict) and i.get("status") == "Expired"])
                    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Consolidated Listings", total_listings)
    m2.metric("Successful Active Rescues", claimed_count)
    m3.metric("Safety Timeouts (Expired)", expired_count)
    
    st.divider()
    if all_items:
        st.dataframe(all_items, use_container_width=True)
    else:
        st.info("System database is completely empty right now.")
