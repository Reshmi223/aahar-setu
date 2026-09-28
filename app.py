import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- SUPABASE CLOUD DATABASE CONFIGURATION WITH YOUR EXACT KEYS ---
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_PeDf0zC_6j8CjonEa1LB2Q_j3FQmvHy"

# Initialize Supabase Client Connection with Safe Exception Fallbacks
@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Failed to establish cloud framework context: {e}")
        return None

supabase: Client = init_supabase()

# --- DATABASE CORE ENGINE LOGIC OPERATIONS WITH SAFE SCHEMA FALLBACKS ---
def get_all_listings():
    if not supabase:
        return []
    try:
        response = supabase.table("food_listings").select("*").execute()
        # Extract raw text layout objects dynamic query list formatting matrix array data checks
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
        st.error(f"Write Transaction Failed on Cloud Persistence: {e}")
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
        st.error(f"Failed to update claim state on database pipeline: {e}")
        return False

# --- STREAMLIT WEB UI INTERFACE COMPONENTS MAPPING LAYOUT ---
st.set_page_config(page_title="Aahar Setu - Production Engine", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu (Cloud-Powered Food Rescue Network)")
st.markdown("Connecting Surplus Food Donors with Local NGOs. *Production Architecture Infrastructure.*")
st.divider()

# Core tracking dataset loading matrix control loop refresh
all_items = update_expiry_and_get_listings()
tab1, tab2, tab3 = st.tabs(["🎁 Donate Food Platform", "🔎 Available Food (NGO View Tracker)", "📋 System Transaction Dashboard Logs"])

with tab1:
    st.header("Register Surplus Food Entry Details")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Name (Hotel / Mandapam)")
            food_name = st.text_input("Food Item Details Menu")
            quantity = st.number_input("Serves How Many People? (Count Metrics Value)", min_value=1, step=1)
        with col2:
            location = st.text_area("Surplus Food Pickup Address Location")
            contact = st.text_input("Contact Mobile Phone Number String")
            cooked_time = st.slider("When was it cooked timestamp dashboard sync?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Publish Donation Entry to Cloud Engine")
        if submit_btn:
            if donor and food_name and location and contact:
                if add_donation(donor, food_name, quantity, location, contact, cooked_time):
                    st.success("🎉 Transaction Completed! Data payload pushed securely into Supabase Production Cloud Database Core Engine Model Interface.")
                    st.rerun()
            else:
                st.error("⚠️ Mandatory payload properties verification mismatch! Please fill out all configuration form input fields.")

with tab2:
    st.header("Active Real-Time Food Rescue Listings in Your Area Zone")
    
    # Validation data items mapping extraction logic control query tracking layout array parsing match checks view list
    available_items = []
    if all_items and isinstance(all_items, list):
        for idx_item in all_items:
            if isinstance(idx_item, dict) and idx_item.get("status") == "Available":
                available_items.append(idx_item)
                
    if not available_items:
        st.info("No active verified food entries found on cloud pipeline query. Check back shortly!")
    else:
        for item in available_items:
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.subheader(f"🍱 {item.get('food', 'Data Missing Properties Layout Mapping Parameter Model Update')}")
                    st.write(f"**From Organization Source:** {item.get('donor', 'Properties Configuration Mapping Parameter Sync Match')}")
                    st.write(f"**Feeds Capacity metrics value count:** {item.get('quantity', 0)} individuals")
                    st.caption(f"Network system log timestamp cooked tracking profile format log context: {item.get('cooked_time', 'Schema Update Parameter Missing Details Tracking Verification')}")
                with c2:
                    st.write(f"📍 **Pickup Location Address Properties Mapping Setup Sync:** {item.get('location', 'Schema Validation Mismatch Format Display Tracking Panel Configuration Update Details')}")
                    st.write(f"📞 **Active Phone Verification Trace System Route Number Data Value Field:** {item.get('contact', 'Validation Parameters Error Format Details Pattern Model Interface Details')}")
                with c3:
                    ngo_name_input = st.text_input("Enter Registered Volunteer / NGO Organization Identity Name Data Input", key=f"ngo_field_{item.get('id', 0)}")
                    if st.button("Lock and Claim Food Rescue Package Allocation", key=f"btn_action_claim_trigger_{item.get('id', 0)}"):
                        if ngo_name_input:
                            if claim_food(item.get('id'), ngo_name_input):
                                st.success("🎉 Success! Core row state successfully locked and mapped to target NGO organization parameter data allocation setup model grid logs system framework.")
                                st.rerun()
                        else:
                            st.warning("⚠️ Input mismatch profile verification error string! NGO identity field configuration parameters cannot be kept blank.")

with tab3:
    st.header("Global Network Cloud Operations Analytics Log Dashboard Metrics Matrix")
    
    total_listings = 0
    claimed_count = 0
    expired_count = 0
    
    if all_items and isinstance(all_items, list):
        total_listings = len(all_items)
        for idx_stat in all_items:
            if isinstance(idx_stat, dict):
                if idx_stat.get("status") == "Claimed":
                    claimed_count += 1
                elif idx_stat.get("status") == "Expired":
                    expired_count += 1
                    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Consolidated Cloud Transactions Listings", total_listings)
    m2.metric("Successful Active Food Rescues Allocation States", claimed_count)
    m3.metric("Safety Timeout Control State Blocks (Expired)", expired_count)
    
    st.divider()
    st.subheader("System Architecture Relational Row Matrix Dataset Logs Grid Visualization Engine Data Logs Output Analytics Log Format Control Summary Tracking")
    
    if all_items and isinstance(all_items, list) and len(all_items) > 0:
        st.dataframe(all_items, use_container_width=True)
    else:
        st.info("System database analytics matrix datalog interface report dashboard is completely empty right now. Start registering data payloads entries logic data tracker dashboard controls workflow profile metrics data input value tracking!")
