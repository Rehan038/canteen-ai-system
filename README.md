Test Credentials

user log in 
username: 12345
password:1234

vendor login

username: coffee
password :123

admin 

username : admin
password : admin123


# 🍔 Canteen Rush AI

### *Zero Wait. Zero Waste. Synchronized Campus Dining.*

**Canteen Rush AI** is an intelligent queue management and demand forecasting system designed to eliminate physical waiting lines in high-density university campuses. By converting physical queues into asynchronous digital demand, we ensure students pick up their food exactly when it's ready—no earlier, no later.

---

## 🚀 Key Features

### 1. 🧠 AI Coordination Engine (The Brain)

* **Dynamic Time Prediction:** Calculates precise pickup times using a heuristic algorithm: `(Queue Length * Avg Prep Time) + Item Complexity + Walking Buffer`.
* **Rush Hour Detection:** Automatically detects high traffic (`>20 active orders`) and applies a congestion multiplier (`1.5x`) to manage expectations.
* **Smart Sorting:** Prioritizes kitchen orders by **"Urgency"** (Time to Promised Pickup) rather than just First-Come-First-Serve.

### 2. 📱 Student Interface (Pre-emptive Demand)

* **Time-Travel Ordering:** Students place orders during class. The app predicts: *"If you order now, pickup is at 12:45 PM."*
* **Frictionless Identity:** Secure **PIN-based login** (Name + ID + 4-digit PIN) for fast access without complex sign-ups.
* **Multi-Vendor Marketplace:** Browse menus from different campus vendors (Grill Master, Fresh Brew, etc.) in a unified interface.
* **Live Tracking:** Real-time status bar: `Received` → `Cooking` → `Ready` → `Collected`.

### 3. 👨‍🍳 Vendor Dashboard (Synchronization)

* **Live Kitchen Display System (KDS):** Auto-refreshing dashboard shows incoming orders instantly.
* **Visual Urgency:** Rows turn **RED** if pickup is < 5 minutes away.
* **Inventory Control:** One-click toggle to "86" (hide) items that are out of stock.
* **Ghost Protocol:** Automatically flags orders as "Expired" if not picked up in 20 minutes to clear counter space.

### 4. ⚖️ Karma & Security System

* **Reliability Score:** Every user starts with **100 Points**.
* **No-Show Penalty:** If an order expires, the user loses **10 Points**.
* **Automatic Ban:** If points drop below **40**, the user is **blocked from logging in**, ensuring system efficiency.

---

## 🛠️ Tech Stack

* **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Database:** SQLite (Lightweight, file-based persistence)
* **Real-Time Updates:** `streamlit-autorefresh`
* **Data Processing:** Pandas

---

## 📸 Screenshots

*(Add your screenshots here after running the app)*

| Student Ordering Flow | Vendor Dashboard |
| --- | --- |
|  |  |

---

## ⚡ Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/canteen-rush-ai.git
cd canteen-rush-ai

```


2. **Install Dependencies**
```bash
pip install -r requirements.txt

```


3. **Run the Application**
```bash
streamlit run app.py

```


4. **Access the App**
* Open your browser at `http://localhost:8501`



---

## 📂 Project Structure

```text
📂 canteen-rush-ai
├── app.py              # Main Application (UI & Logic)
├── database.py         # Database Schema & Helper Functions
├── ai_engine.py        # Prediction Algorithm & Business Logic
├── canteen.db          # SQLite Database (Auto-generated)
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation

```

---

## 🌍 SDG Alignment

**Goal 12: Responsible Consumption and Production**
By shifting from "Reactive Cooking" (cooking in bulk hoping for sales) to "Proactive Preparation" (cooking only confirmed orders), Canteen Rush AI significantly reduces food waste and optimizes resource usage.

---

## 🔮 Future Roadmap

* [ ] **UPI Integration:** Enable real payments to completely remove cash handling.
* [ ] **Hardware Integration:** Connect with physical thermal printers in the kitchen.
* [ ] **Nutritional AI:** Recommend meals based on student health goals.

---

### 👥 Team

* **Developers:** Rehan , chris and anamika

*Built for revelations 2026 Hackathon.*
