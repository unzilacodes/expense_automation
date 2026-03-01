import streamlit as st
import pandas as pd
import os
import json
import pdfplumber
from datetime import datetime
from streamlit.components.v1 import html

#  configuration
st.set_page_config("Smart Invoice System", layout="wide")
DATA_DIR = "data"
CATEGORY_FILE = "categories.json"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# session
if "user" not in st.session_state:
    st.session_state.user = None
if "page_flow" not in st.session_state:
    st.session_state.page_flow = 0

#  categorization
def load_categories():
    if os.path.exists(CATEGORY_FILE):
        with open(CATEGORY_FILE, "r") as f:
            return json.load(f)
    return {
        "Electronics": ["laptop","computer","usb","mouse","keyboard","monitor","printer","charger","camera","speaker","hp","dell","elitebook","ipad","tablet","macbook","headphones","ssd","hdd","ram","router"],
        "Food": ["food","pizza","coffee","biryani","meal","snack","lunch","dinner","restaurant","drink","burger","cake","tea","sandwich","juice"],
        "Office": ["pen","paper","notebook","file","folder","stapler","stationery","envelope","clip","marker","printer ink","calendar","diary","binder"],
        "Travel": ["taxi","bus","hotel","uber","flight","train","cab","airbnb","careem","fare","car","ticket","fuel","trip","boarding pass"],
        "Utilities": ["electric","water","gas","internet","electricity","phone","utility","bill","subscription","wifi","cable","energy"],
        "Medical": ["hospital","medicine","doctor","pharmacy","xray","clinic","test","blood","surgery","dental","eye","prescription","treatment"],
        "Marketing": ["advertisement","promotion","banner","poster","campaign","social media","flyer","branding","seo","content","ads"],
        "Education": ["book","course","tuition","exam","stationery","school","college","university","notes","training"],
        "Entertainment": ["movie","cinema","music","concert","game","netflix","ticket","theatre","show","event"],
        "Miscellaneous": ["gift","donation","subscription","charity","others","misc"]
    }

def save_categories(data):
    with open(CATEGORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

CATEGORY_RULES = load_categories()

def categorize(item):
    combined = str(item).lower()
    for cat, words in CATEGORY_RULES.items():
        for w in words:
            if w in combined:
                return cat
    return "Others"

# login setup (username + purpose)
def login():
    st.markdown("<h1 style='color:#00ffcc;text-align:center'>💼 WELCOME TO SMART INVOICEXPERT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:18px;color:#ffffff'>Automate your invoices and track expenses in one smart place!</p>", unsafe_allow_html=True)
    
    # Username input
    name = st.text_input("Enter your name to start", "")
    # Purpose input
    purpose = st.text_input("Purpose of use (optional)", "")
    
    if st.button("Start"):
        if name.strip() == "":
            st.warning("Please enter a valid name")
        else:
            st.session_state.user = name.lower().strip()
            st.session_state.purpose = purpose.strip() if purpose else "Not specified"
            st.session_state.page_flow = 0
            st.rerun()

#  database
def user_file(user):
    return os.path.join(DATA_DIR, f"{user}.csv")

def load_history(user):
    path = user_file(user)
    if not os.path.exists(path):
        return pd.DataFrame(columns=["Vendor","Date","Item","Quantity","Price","Category"])
    return pd.read_csv(path)

def save_history(user, df):
    df.to_csv(user_file(user), index=False)

#  INVOICE PARSING 
def parse_pdf(file):
    df_all = pd.DataFrame()
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if len(table) < 2:
                    continue
                temp_df = pd.DataFrame(table[1:], columns=table[0])
                temp_df.columns = [str(c).strip().lower() for c in temp_df.columns]
                rename_map = {}
                if 'item name' in temp_df.columns:
                    rename_map['item name'] = 'item'
                if 'item' in temp_df.columns:
                    rename_map['item'] = 'item'
                if 'price' in temp_df.columns:
                    rename_map['price'] = 'price'
                elif 'price(pkr)' in temp_df.columns:
                    rename_map['price(pkr)'] = 'price'
                if 'vendor' in temp_df.columns:
                    rename_map['vendor'] = 'vendor'
                if 'date' in temp_df.columns:
                    rename_map['date'] = 'date'
                if 'quantity' in temp_df.columns:
                    rename_map['quantity'] = 'quantity'
                temp_df = temp_df.rename(columns=rename_map)
                required_cols = ['vendor','date','item','quantity','price']
                temp_df = temp_df[[c for c in required_cols if c in temp_df.columns]]
                if 'price' in temp_df.columns:
                    temp_df['price'] = temp_df['price'].astype(float)
                if 'item' in temp_df.columns:
                    temp_df['category'] = temp_df['item'].apply(categorize)
                df_all = pd.concat([df_all, temp_df], ignore_index=True)
    return df_all

#  UI DESIGN
st.markdown("""
<style>
body {background: radial-gradient(circle at top, #0a0a0a 0%, #121212 100%); color: #f0f0f0; font-family: 'Montserrat', 'Roboto', sans-serif;}
h1,h2,h3,h4 {color: #00fff0; text-shadow: 0 0 5px #00fff0, 0 0 10px #00fff0, 0 0 20px #ff00ff;}
p,span,label {color: #ffffff;}
button, .stButton>button {background: linear-gradient(45deg,#ff00ff,#00ffff); color: #ffffff; border-radius: 15px; border:none; padding:12px 25px; font-weight:bold; font-size:16px; box-shadow:0 0 10px #ff00ff, 0 0 20px #00ffff; transition:0.4s;}
button:hover, .stButton>button:hover{box-shadow:0 0 20px #ff00ff,0 0 30px #00ffff, 0 0 40px #ff00ff; transform: scale(1.08);}
.stDataFrameWrapper {border-radius: 10px; box-shadow: 0 0 20px #00ffff; padding:5px;}
[data-testid="stSidebar"] {background: linear-gradient(to bottom, #0d0d0d, #1a1a1a); border-right: 2px solid #00fff0;}
[data-testid="stSidebar"] .stRadio>label {display:block; position:relative; padding:10px 15px; margin-bottom:10px; border-radius:10px; border:2px solid #00fff0; transition: all 0.3s ease; cursor:pointer;}
[data-testid="stSidebar"] .stRadio>label:hover {box-shadow:0 0 10px #00fff0,0 0 20px #00ffff,0 0 30px #ff00ff; transform: scale(1.05); background-color: rgba(0,255,255,0.05);}
[data-testid="stSidebar"] .stRadio>label:has(input:checked) {background-color: rgba(0,255,255,0.2); box-shadow:0 0 15px #00fff0,0 0 30px #00ffff,0 0 45px #ff00ff; border-color: #00ffff; font-weight:bold; color:#00ffff !important;}
.stFileUploader>div>div {border: 2px dashed #00fff0; border-radius: 10px; padding: 20px; text-align:center; color: #00fff0; font-weight:bold;}
input[type="text"] {background-color:#121212; color:#00fff0; border:1px solid #00fff0; border-radius:10px; padding:8px 12px;}
</style>
""", unsafe_allow_html=True)

# Floating neon dots
html("""
<canvas id="dotsCanvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:-1;"></canvas>
<script>
const canvas=document.getElementById('dotsCanvas'); canvas.width=window.innerWidth; canvas.height=window.innerHeight; const ctx=canvas.getContext('2d');
let dots=[]; for(let i=0;i<120;i++){dots.push({x:Math.random()*canvas.width, y:Math.random()*canvas.height, r:Math.random()*3+1, dx:(Math.random()-0.5)*0.5, dy:(Math.random()-0.5)*0.5, color:`rgba(${Math.floor(Math.random()*255)},${Math.floor(Math.random()*255)},255,0.7)`});}
function animate(){ctx.clearRect(0,0,canvas.width,canvas.height); dots.forEach(d=>{ctx.beginPath(); ctx.arc(d.x,d.y,d.r,0,Math.PI*2); ctx.fillStyle=d.color; ctx.fill(); d.x+=d.dx; d.y+=d.dy; if(d.x<0||d.x>canvas.width)d.dx*=-1; if(d.y<0||d.y>canvas.height)d.dy*=-1;}); requestAnimationFrame(animate);}
animate();
</script>
""", height=0)

# WEB APP 
def app():
    user = st.session_state.user
    st.markdown(f"<h1 style='color:#00ffcc'>💼 Smart Invoice System</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4>User: {st.session_state.user}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5>Purpose of Use: {st.session_state.purpose}</h5>", unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state.user=None
        st.session_state.page_flow = 0
        st.rerun()

    # Modern navigation labels
    pages = ["📤 Upload Invoice", "📊 Monthly Insights", "📂 Expense History", "🎉 Thank You"]
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to page", pages)
    
    if choice == "📤 Upload Invoice":
        st.subheader("Upload Invoice (PDF Table Only)")
        file = st.file_uploader("Upload PDF", type=["pdf"])
        if file:
            st.success("File Uploaded")
            items_df = parse_pdf(file)
            if items_df.empty:
                st.error("No valid table found in PDF!")
                return

            vendor = items_df['vendor'].iloc[0]
            total = items_df['price'].sum()
            date = pd.to_datetime(items_df['date'].iloc[0], dayfirst=True)

            st.markdown(f"""
            <div style="display:flex; gap:20px; margin-bottom:20px;">
                <div style='border:2px solid #00fff0; padding:15px 25px; border-radius:15px; text-align:center; box-shadow: 0 0 10px #00fff0,0 0 20px #00ffff; min-width:180px;'>
                    <h4 style='color:#00fff0;'>Vendor</h4><p style='font-size:18px; font-weight:bold;'>{vendor}</p>
                </div>
                <div style='border:2px solid #ff00ff; padding:15px 25px; border-radius:15px; text-align:center; box-shadow: 0 0 10px #ff00ff,0 0 20px #ff00ff; min-width:180px;'>
                    <h4 style='color:#ff00ff;'>Total Amount</h4><p style='font-size:18px; font-weight:bold;'>{total}</p>
                </div>
                <div style='border:2px solid #00ff00; padding:15px 25px; border-radius:15px; text-align:center; box-shadow: 0 0 10px #00ff00,0 0 20px #00ff00; min-width:180px;'>
                    <h4 style='color:#00ff00;'>Date</h4><p style='font-size:18px; font-weight:bold;'>{date.strftime('%d/%m/%Y')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("Listed Items with Category")
            st.dataframe(items_df[['item','category','price']])
            st.download_button("Download Listed Items CSV", items_df.to_csv(index=False), f"{user}_listed_items.csv")

            # Save history
            history = load_history(user)
            history = pd.concat([history, items_df[['vendor','date','item','quantity','price','category']]], ignore_index=True)
            save_history(user, history)

    elif choice == "📊 Monthly Insights":
        st.subheader("Monthly Report")
        history = load_history(user)
        if not history.empty:
            history['date'] = pd.to_datetime(history['date'], errors='coerce')
            monthly = history.groupby(history['date'].dt.to_period('M'))['price'].sum().reset_index()
            monthly = monthly.sort_values('date')
            chart_data = monthly.copy()
            chart_data['date'] = chart_data['date'].astype(str)
            st.bar_chart(chart_data.set_index('date')['price'])
            st.markdown("<p style='text-align:center;color:#ffffff'>X-axis: Month | Y-axis: Total Amount</p>", unsafe_allow_html=True)
        else:
            st.info("No data yet to show monthly report.")

        st.subheader("Teach System New Keyword")
        learn_word = st.text_input("Enter Keyword")
        learn_cat = st.selectbox("Assign Category", list(CATEGORY_RULES.keys()))
        if st.button("Save Keyword"):
            word = learn_word.lower().strip()
            if word!="" and word not in CATEGORY_RULES[learn_cat]:
                CATEGORY_RULES[learn_cat].append(word)
                save_categories(CATEGORY_RULES)
                st.success(f"'{word}' added to {learn_cat}")
                st.rerun()

    elif choice == "📂 Expense History":
        st.subheader("Extracted Data History")
        history = load_history(user)
        if not history.empty:
            st.dataframe(history)
            st.download_button("Download CSV", history.to_csv(index=False), f"{user}_expenses.csv")
        else:
            st.info("No history data available.")

    elif choice == "🎉 Thank You":
        st.markdown("<h2 style='color:#00fff0;text-align:center'>Thank You for Using Smart Invoice System</h2>", unsafe_allow_html=True)
        st.balloons()

#  FLOW 
if st.session_state.user is None:
    login()
else:
    app()

