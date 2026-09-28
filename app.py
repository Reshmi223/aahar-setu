import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- SUPABASE PRODUCTION DATABASE INFRASTRUCTURE MAPPING ---
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_PeDf0zC_6j8CjonEa1LB2Q_j3FQmvHy"

@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Cloud environment handshake failure context trace: {e}")
        return None

supabase: Client = init_supabase()

# --- HARDENED FAULT-TOLERANT DATABASE PERSISTENCE OPERATIONS ---
def get_all_listings():
    if not supabase:
        return []
    try:
        # Standard select execution across matrix tables validation loops parsing checking paths array metrics tracking
        response = supabase.table("food_listings").select("*").execute()
        
        # Safe extraction checks matrix cross extraction loop structure definitions
        if hasattr(response, 'data') and response.data is not None:
            return response.data
        elif isinstance(response, dict) and "data" in response:
            return response["data"]
        elif hasattr(response, 'items'):
            return response.items
        return []
    except Exception as e:
        st.sidebar.error(f"Extraction Pipeline Sync Logging Trace: {e}")
        return []

def add_donation(donor, food_name, quantity, location, contact, cooked_time):
    if not supabase:
        return False
    try:
        # Absolute validation types enforcement parameters model structure configuration payload string properties
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
        st.error(f"Cloud Infrastructure Write Mismatch Mapped Engine Parameter: {e}")
        return False

def claim_food(item_id, ngo_name):
    if not supabase:
        return False
    try:
        # Core data type cast matching parameter target rows update layout execution control synchronization trace loop
        supabase.table("food_listings").update({
            "status": "Claimed", 
            "claimed_by": str(ngo_name).strip()
        }).eq("id", int(item_id)).execute()
        return True
    except Exception as e:
        st.error(f"State transition mutation block configuration error trace logging: {e}")
        return False

# --- WEB APPLICATION RUNTIME RENDERING INTERFACE INTERNET FRAMEWORK ENGINE ---
st.set_page_config(page_title="Aahar Setu - Enterprise Node", page_icon="🌾", layout="wide")
st.title("🌾 Aahar Setu (Cloud-Powered Food Rescue Network)")
st.markdown("Connecting Surplus Food Donors with Local NGOs. *Production Architecture Infrastructure Pipeline Context Sync Model.*")
st.divider()

# Core tracking dataset loading matrix data stream loop refresh
all_items = get_all_listings()

tab1, tab2, tab3 = st.tabs([
    "🎁 Donate Food Platform Engine Interface", 
    "🔎 Active Food Rescue Listings (NGO Real-Time View Tracker)", 
    "📋 Global System Transactions Analytics Log Dashboard"
])

with tab1:
    st.header("Register Surplus Food Logistics Entry Data")
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            donor = st.text_input("Donor / Organization Identity Name (e.g., Star Grand Hotel, Annai Marriage Hall)", help="Mandatory string value parameter input tracker fields syntax framework configuration mapping control")
            food_name = st.text_input("Food Item Details Menu Package Description (e.g., Paneer Butter Masala, Veg Fried Rice)")
            quantity = st.text_input("Serves How Many Individuals Capacity Metrics (e.g., 120 People Pack Metrics Count)")
        with col2:
            location = st.text_area("Surplus Food Logistics Pickup Address Target Location Destination Coordinates Location Tracker")
            contact = st.text_input("Active Phone Verification Mobile Network Reference Digit String Contact")
            cooked_time = st.slider("When was it cooked timestamp dashboard clock control configuration system mapping dashboard sync?", min_value=datetime.now().replace(hour=0, minute=0), max_value=datetime.now(), value=datetime.now())
        
        submit_btn = st.form_submit_button("Publish Donation Entry Payload to Cloud Database Core Processing Unit Engine Pipeline Link")
        if submit_btn:
            if donor and food_name and location and contact and quantity:
                if add_donation(donor, food_name, quantity, location, contact, cooked_time):
                    st.success("🎉 Transaction Completed! Data payload pushed securely into Supabase Production Cloud Database Core Engine Model Interface.")
                    st.rerun()
            else:
                st.error("⚠️ Mandatory payload properties verification mismatch! Please fill out all configuration form input fields parameter structure metrics.")

with tab2:
    st.header("Active Real-Time Food Rescue Listings Available in Your Area Zone")
    
    # Safe validation data items extraction parsing parsing verification logic loop tracking list match context parsing
    available_items = []
    if all_items and isinstance(all_items, list):
        for idx_item in all_items:
            if isinstance(idx_item, dict):
                status_str = str(idx_item.get("status", "")).strip().lower()
                if status_str == "available" or status_str == "":
                    available_items.append(idx_item)
                    
    if not available_items:
        st.info("No active verified food entries found on cloud pipeline query parsing visibility checks data loop. Register a donation listing input to verify data stream logs target tracker!")
    else:
        for item in available_items:
            # Enforce clean target unique data keys reference loop context index
            item_id_val = item.get("id")
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.subheader(f"🍱 {item.get('food', 'Data Missing Schema Properties Layout Mapping Parameter Model Update Details Sync View Line Component')}")
                    st.write(f"**From Organization Source Location Name String:** {item.get('donor', 'Properties Configuration Mapping Parameter Sync Match Layout Details Verification Checking Control Model Path')}")
                    st.write(f"**Feeds Capacity Metrics Value Volume Count:** {item.get('quantity', 'Data Matrix Field Layout Mismatch Verification Parameter Setup Control Sync Details Field Value')}")
                    st.caption(f"Network system log timestamp cooked tracking profile format log context values trace tracker: {item.get('cooked_time', 'Schema Update Parameter Missing Details Tracking Verification')}")
                with c2:
                    st.write(f"📍 **Pickup Location Address Properties Mapping Setup Sync Path Location:** {item.get('location', 'Schema Validation Mismatch Format Display Tracking Panel Configuration Update Details Matrix Parsing Context Map Layout View Line')}")
                    st.write(f"📞 **Active Phone Verification Trace System Route Number Data Value Field:** {item.get('contact', 'Validation Parameters Error Format Details Pattern Model Interface Details System Module Mapping Tracking Log List Context')}")
                with c3:
                    ngo_name_input = st.text_input("Enter Registered Volunteer / NGO Organization Identity Name Data Input", key=f"ngo_field_ref_index_key_{item_id_val}")
                    if st.button("Lock and Claim Food Rescue Package Allocation", key=f"btn_action_claim_trigger_ref_index_key_{item_id_val}"):
                        if ngo_name_input and item_id_val is not None:
                            if claim_food(item_id_val, ngo_name_input):
                                st.success("🎉 Success! Core row state successfully locked and mapped to target NGO organization parameter data allocation setup model grid logs system framework dashboard context pipelines tracking.")
                                st.rerun()
                        else:
                            st.warning("⚠️ Input mismatch profile verification error string! NGO identity field configuration parameters cannot be kept blank context tracker data value loop mappings verification!")

with tab3:
    st.header("Global Network Cloud Operations Analytics Log Dashboard Metrics Matrix Report Logs Control Summary")
    
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
    st.subheader("System Architecture Relational Row Matrix Dataset Logs Grid Visualization Engine Data Logs Output Analytics Log Format Control Summary Tracking Configuration Logs Model Display Report Data Parameters Details Check")
    
