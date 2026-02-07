"""
Canteen Rush AI - Multi-Vendor Marketplace
Final, Production-Ready Ultimate Edition
"""

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pandas as pd
import time

import database as db
import ai_engine

# Initialize database
db.init_db()

# Page configuration
st.set_page_config(
    page_title="Canteen Rush AI",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CONSTANTS & THEME ====================
THEME_CONFIG = {
    "bg_dark": "#0f172a",
    "bg_card": "#1e293b",
    "accent_blue": "#3b82f6",
    "accent_green": "#10b981",
    "accent_amber": "#f59e0b",
    "accent_red": "#ef4444",
    "text_main": "#f1f5f9",
    "text_muted": "#94a3b8"
}

CSS_SYSTEM = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {THEME_CONFIG['bg_dark']}; color: {THEME_CONFIG['text_main']}; }}
    
    .main-header {{
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem; border-radius: 16px; color: #f8fafc; text-align: center;
        margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #334155;
    }}
    
    .card-container {{
        background-color: {THEME_CONFIG['bg_card']}; border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #334155; margin-bottom: 24px; text-align: center; color: {THEME_CONFIG['text_main']};
    }}
    .card-container:hover {{ transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.5); border-color: #475569; }}
    .card-image {{ border-radius: 12px; width: 100%; height: 160px; object-fit: cover; margin-bottom: 18px; filter: brightness(0.9); }}
    
    .badge {{ display: inline-block; padding: 6px 14px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #fff; }}
    .status-ready {{ background-color: {THEME_CONFIG['accent_green']}; box-shadow: 0 0 12px rgba(16, 185, 129, 0.4); }}
    .status-cooking {{ background-color: {THEME_CONFIG['accent_amber']}; box-shadow: 0 0 12px rgba(245, 158, 11, 0.4); }}
    .status-received {{ background-color: {THEME_CONFIG['accent_blue']}; box-shadow: 0 0 12px rgba(59, 130, 246, 0.4); }}
    .status-expired {{ background-color: {THEME_CONFIG['accent_red']}; box-shadow: 0 0 12px rgba(239, 68, 68, 0.4); }}
    
    .karma-badge {{ padding: 8px 18px; border-radius: 10px; font-weight: 700; font-size: 0.9rem; }}
    .karma-green {{ background-color: rgba(16, 185, 129, 0.2); color: {THEME_CONFIG['accent_green']}; border: 1px solid {THEME_CONFIG['accent_green']}; }}
    .karma-yellow {{ background-color: rgba(245, 158, 11, 0.2); color: {THEME_CONFIG['accent_amber']}; border: 1px solid {THEME_CONFIG['accent_amber']}; }}
    .karma-red {{ background-color: rgba(239, 68, 68, 0.2); color: {THEME_CONFIG['accent_red']}; border: 1px solid {THEME_CONFIG['accent_red']}; }}
    
    .urgent-row {{ background-color: rgba(239, 68, 68, 0.1) !important; border-right: 5px solid {THEME_CONFIG['accent_red']} !important; }}
    .vendor-order-row {{ background-color: {THEME_CONFIG['bg_card']}; border-radius: 12px; padding: 15px; border: 1px solid #334155; margin-bottom: 12px; }}
    
    .qr-mock {{ background: #fff; padding: 10px; border-radius: 8px; width: 100px; height: 100px; margin: 10px auto; border: 4px solid {THEME_CONFIG['accent_green']}; }}
    .tooltip {{ color: {THEME_CONFIG['text_muted']}; font-size: 0.8rem; cursor: help; border-bottom: 1px dashed {THEME_CONFIG['text_muted']}; }}
    
    [data-testid="stSidebar"] {{ background-color: #111827; border-right: 1px solid #1f2937; }}
    .stTextInput>div>div>input {{ background-color: {THEME_CONFIG['bg_card']}; color: {THEME_CONFIG['text_main']}; border-color: #334155; }}
    .stExpander {{ background-color: {THEME_CONFIG['bg_card']} !important; border: 1px solid #334155 !important; border-radius: 12px !important; }}
</style>
"""
st.markdown(CSS_SYSTEM, unsafe_allow_html=True)

# ==================== SESSION STATE ====================
def init_session_state():
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "role" not in st.session_state: st.session_state.role = None
    if "user_info" not in st.session_state: st.session_state.user_info = None
    if "selected_vendor" not in st.session_state: st.session_state.selected_vendor = None
    if "last_statuses" not in st.session_state: st.session_state.last_statuses = {}

init_session_state()

# ==================== AUTHENTICATION ====================
def render_auth():
    st.markdown('<div class="main-header"><h1>🍱 Canteen Rush AI</h1><p>Production Edition • Multi-Vendor System</p></div>', unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.tabs(["🎓 Student", "📝 Register", "👨‍🍳 Vendor", "🛡️ Admin"])
    
    with t1:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="card-container"><h3>Student Login</h3>', unsafe_allow_html=True)
            with st.form("student_login", clear_on_submit=True):
                roll = st.text_input("Roll No", placeholder="2024CS001")
                pin = st.text_input("PIN", type="password", max_chars=4)
                if st.form_submit_button("Sign In", use_container_width=True):
                    if db.check_ban_status(roll):
                        st.error("🚫 Account Suspended. Karma < 40.")
                    else:
                        user = db.verify_user(roll, pin)
                        if user:
                            st.session_state.logged_in, st.session_state.role = True, "student"
                            st.session_state.user_info = {"roll": roll, "name": user["name"], "points": user["points"]}
                            st.rerun()
                        else: st.error("Invalid credentials.")
            st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="card-container"><h3>Register Student</h3>', unsafe_allow_html=True)
            with st.form("register"):
                name = st.text_input("Full Name")
                roll = st.text_input("Roll Number")
                pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
                if st.form_submit_button("Create ID", use_container_width=True):
                    if name and roll and len(pin) == 4:
                        if db.register_user(roll, name, pin): st.success("Created! Please Log In.")
                        else: st.error("ID exists.")
                    else: st.warning("Fill all fields correctly.")
            st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="card-container"><h3>Vendor Panel</h3>', unsafe_allow_html=True)
            with st.form("vendor_login"):
                vu = st.text_input("Username")
                vp = st.text_input("Password", type="password")
                if st.form_submit_button("Vendor Sign In", use_container_width=True):
                    v = db.verify_vendor(vu, vp)
                    if v:
                        st.session_state.logged_in, st.session_state.role = True, "vendor"
                        st.session_state.user_info = v
                        st.rerun()
                    else: st.error("Access Denied.")
            st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="card-container"><h3>Admin Access</h3>', unsafe_allow_html=True)
            with st.form("admin_login"):
                au = st.text_input("Admin ID")
                ap = st.text_input("Secret Key", type="password")
                if st.form_submit_button("Authorize", use_container_width=True):
                    if db.verify_admin(au, ap):
                        st.session_state.logged_in, st.session_state.role = True, "admin"
                        st.rerun()
                    else: st.error("Master key incorrect.")
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== INTERFACES ====================

def render_student():
    st_autorefresh(interval=5000, key="sr")
    st.session_state.user_info["points"] = db.get_user_points(st.session_state.user_info["roll"])
    pts = st.session_state.user_info["points"]

    c1, c2 = st.columns([3, 1])
    c1.title(f"👋 {st.session_state.user_info['name']}")
    k_class = "karma-green" if pts > 80 else ("karma-red" if pts < 50 else "karma-yellow")
    c2.markdown(f'<div style="text-align:right"><span class="karma-badge {k_class}">⭐ Karma: {pts}</span></div>', unsafe_allow_html=True)
    if c2.button("Exit"): 
        st.session_state.clear()
        st.rerun()

    active = db.get_user_active_orders(st.session_state.user_info["roll"])
    if active:
        with st.expander("🕒 Tracking", expanded=True):
            for o in active:
                cs, oid = o["status"], o["id"]
                if oid in st.session_state.last_statuses and st.session_state.last_statuses[oid] != cs and cs == "Ready":
                    st.toast(f"✅ {o['token_id']} Ready!", icon="🍱")
                st.session_state.last_statuses[oid] = cs
                val = {"Received": 0, "Cooking": 50, "Ready": 100}.get(cs, 0)
                sc = st.columns([1, 4, 1])
                sc[0].write(o["token_id"])
                
                with sc[1]:
                    st.progress(val/100, f"{o['item_name']} ({o['vendor_name']})")
                    if cs == "Ready":
                        st.markdown('<div class="qr-mock"><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data='+o["token_id"]+'" width="80"></div>', unsafe_allow_html=True)
                        st.caption("Show this at counter")
                
                sc[2].markdown(f'<span class="badge status-{cs.lower()}">{cs}</span>', unsafe_allow_html=True)

    if not st.session_state.selected_vendor:
        st.subheader("🏙️ Select Stall")
        vs = db.get_all_vendors()
        cols = st.columns(3)
        for i, v in enumerate(vs):
            with cols[i%3]:
                st.markdown(f'<div class="card-container"><img src="{v["image_url"]}" class="card-image"><h3>{v["name"]}</h3></div>', unsafe_allow_html=True)
                if st.button(f"Go to {v['name']}", key=f"v_{v['id']}", use_container_width=True):
                    st.session_state.selected_vendor = v
                    st.rerun()
    else:
        v = st.session_state.selected_vendor
        st.subheader(f"🍱 {v['name']}")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            if st.button("⬅️ Change Stall"):
                st.session_state.selected_vendor = None
                st.rerun()
        with c2:
            target_break = st.select_slider(
                "🎯 Targeted Pickup / Break",
                options=["Immediate", "10:30 AM", "12:00 PM", "1:30 PM", "3:00 PM"],
                value="Immediate"
            )
        
        items = db.get_menu(v["id"])
        icols = st.columns(3)
        for i, item in enumerate(items):
            with icols[i%3]:
                p = ai_engine.calculate_wait_time(v["id"], item["avg_prep_time"], target_break)
                st.markdown(f"""
                <div class="card-container">
                    <img src="{item["image_url"]}" class="card-image">
                    <h4>{item["item_name"]}</h4>
                    <p style="color:{THEME_CONFIG["accent_green"]}; font-size:1.2rem; font-weight:bold;">₹{item["price"]}</p>
                    <p class="tooltip" title="Prep: {p['breakdown']['base_prep']}m | Queue: {p['breakdown']['queue_delay']}m | Buffer: {p['breakdown']['buffer']}m">
                        ⏱️ Predicted: {p['minutes']} mins
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Order {item['item_name']}", key=f"oi_{item['id']}", use_container_width=True):
                    tid = db.add_order(st.session_state.user_info["roll"], v["id"], item["item_name"], p["formatted_time"])
                    st.success(f"Token: {tid} | Pickup: {p['formatted_time']}")
                    st.balloons()

def render_vendor():
    st_autorefresh(interval=10000, key="vr")
    v_id = st.session_state.user_info["id"]
    c1, c2 = st.columns([4, 1])
    c1.title(f"👨‍🍳 {st.session_state.user_info['name']}")
    if c2.button("Exit Panel"): 
        st.session_state.clear()
        st.rerun()

    s = ai_engine.get_vendor_stats(v_id)
    mc = st.columns(3)
    mc[0].metric("Queue", s["queue_load"])
    mc[1].metric("Wait", f"{s['avg_wait_minutes']}m")
    mc[2].metric("Rush", "🔥" if s["is_rush_hour"] else "✅")

    with st.sidebar:
        st.header("⚙️ Supply")
        for item in db.get_menu(v_id, False):
            if st.checkbox(item["item_name"], value=(item["is_active"]==1), key=f"i_{item['id']}") != (item["is_active"]==1):
                db.toggle_item_availability(item["id"], not (item["is_active"]==1))
                st.rerun()

    orders = db.get_vendor_orders(v_id)
    for o in orders:
        urgent, ghost = False, False
        try:
            pt = datetime.strptime(o['predicted_pickup_time'], "%I:%M %p")
            nt = datetime.strptime(datetime.now().strftime("%I:%M %p"), "%I:%M %p")
            df = (pt - nt).total_seconds() / 60
            if 0 < df < 5: urgent = True
            
            ot = datetime.strptime(o['order_time'], "%Y-%m-%d %H:%M:%S")
            if o['status'] == "Ready" and (datetime.now() - ot).total_seconds() / 60 > 20: ghost = True
        except: pass
        
        style = "urgent-row" if urgent else ("karma-badge karma-yellow" if ghost else "")
        st.markdown(f'<div class="vendor-order-row {style}">', unsafe_allow_html=True)
        oc = st.columns([1, 1.5, 2, 2.5])
        oc[0].write(o["token_id"])
        
        # Proactive Prep Logic
        try:
            pt = datetime.strptime(o['predicted_pickup_time'], "%I:%M %p")
            nt = datetime.strptime(datetime.now().strftime("%I:%M %p"), "%I:%M %p")
            # If wait matches prep_time, highlight start
            prep_needed = db.get_item_prep_time_by_name(o['item_name'])
            wait_rem = (pt - nt).total_seconds() / 60
            if wait_rem <= prep_needed + 2 and o["status"] == "Received":
                oc[1].warning(f"⏰ Start NOW!")
            else:
                oc[1].write(f"In {int(max(0, wait_rem - prep_needed))}m")
        except:
            oc[1].write(o["item_name"])
            
        oc[2].write(f"👤 {o['student_name']} ({o['predicted_pickup_time']})")
        
        with oc[3]:
            bc = st.columns(4)
            if o["status"]=="Received":
                if bc[0].button("🍳", key=f"c_{o['id']}", help="Start Cooking"): db.update_status(o['id'], "Cooking"); st.rerun()
            if o["status"]=="Cooking":
                if bc[1].button("🔔", key=f"r_{o['id']}", help="Mark Ready"): db.update_status(o['id'], "Ready"); st.rerun()
            if o["status"]=="Ready":
                if bc[2].button("🛡️", key=f"d_{o['id']}", help="Verify & Collect"): db.update_status(o['id'], "Collected"); st.rerun()
            if bc[3].button("💀", key=f"x_{o['id']}", help="Mark No-Show"):
                db.expire_order_with_penalty(o['id'])
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def render_admin():
    st.title("🛡️ System Master View")
    if st.button("Safe Logout"): 
        st.session_state.clear()
        st.rerun()
    
    st.subheader("👥 Global Userbase & Karma")
    with db.get_db() as conn:
        users = pd.read_sql("SELECT roll_no, name, points FROM users", conn)
        st.dataframe(users, use_container_width=True)
    
    st.subheader("📊 Global Order Log")
    with db.get_db() as conn:
        orders = pd.read_sql("SELECT * FROM orders ORDER BY order_time DESC LIMIT 50", conn)
        st.dataframe(orders, use_container_width=True)

# ==================== MAIN ====================
def main():
    try:
        if not st.session_state.logged_in: render_auth()
        elif st.session_state.role == "student": render_student()
        elif st.session_state.role == "vendor": render_vendor()
        elif st.session_state.role == "admin": render_admin()
    except Exception as e:
        st.error(f"🔥 Core Error: {str(e)}")
        if st.button("Hard Reset"): st.session_state.clear(); st.rerun()

if __name__ == "__main__":
    main()
