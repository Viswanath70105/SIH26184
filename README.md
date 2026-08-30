# 🛡️ [Project] // I4C-MHA Predictive Cybercrime Analytics System
### Smart India Hackathon (SIH 2026) | Problem Statement ID: 26184
> **Organization:** Ministry of Home Affairs (MHA)  
> **Department:** Indian Cyber Crime Coordination Centre (I4C), CIS Division  
> **Theme:** Blockchain & Cybersecurity | **Category:** Software  

---

## ⚡ Quickstart (1-Command Run)

To run the full interactive prototype and open the dashboard in your browser:

```bash
python3 run.py
```
Or run directly with uvicorn:
```bash
python3 -m uvicorn app.api:app --reload --port 8000
```
Then open your web browser at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🌟 Key Features of the Prototype

1. **AI/ML Predictive Cash-Out Hotspot Forecaster:**
   - Spatio-temporal risk modeling (ST-DBSCAN inspired) predicting high-probability ATM/CSP withdrawal clusters and estimated cash-out windows (minutes remaining).
2. **Interactive Tactical GIS Heatmap:**
   - Leaflet.js-powered dark tactical map showing live ATM pins, dynamic radar pulse rings, and quick zoom navigation across Indian cyber hubs (Delhi-NCR/Mewat, Jamtara, Bengaluru, Mumbai).
3. **Multi-Hop Mule Network Graph (Vis.js):**
   - Interactive force-directed graph exposing transaction flows: Victim $\rightarrow$ Layer 1 Mule $\rightarrow$ Layer 2 Mule $\rightarrow$ Target ATM node with KYC risk flags.
4. **Law Enforcement Action Center (Rapid Response):**
   - **`[🚨 Dispatch Beat Patrol]`**: Simulates instant dispatch to field units near target ATM coordinates.
   - **`[⚡ Trigger 1930 Bank Lien Freeze]`**: Simulates automated CFCFRMS freeze to lock funds in mule accounts before cash withdrawal.
   - **`[📄 View Official I4C FIR Docket]`**: Generates a formatted, printable tactical intelligence brief.
5. **Live 1930 Simulation Engine (`[⚡ Ingest Live Incident]`):**
   - Simulates authentic Indian cyber complaints (Digital Arrest, Telegram Task Scam, Fake Stock IPO, FedEx Courier Fraud, Loan App Extortion, AePS Biometric Clone) in real-time.

---

## 📁 Repository Structure

```
SIH2026/
├── app/
│   ├── __init__.py
│   ├── api.py                 # FastAPI REST API endpoints & server
│   ├── simulation_engine.py   # Indian Cybercrime & Mule Chain Generator
│   ├── predictive_engine.py   # ST-DBSCAN, ML Risk Scoring & Graph logic
│   └── static/
│       ├── index.html         # Glassmorphic tactical dashboard
│       ├── styles.css         # Modern dark-mode styling tokens
│       └── app.js             # Leaflet GIS, Vis.js graph & real-time client logic
├── run.py                     # Single-command startup script
├── PRESENTATION_GUIDE.md      # Ready-to-copy Slide-by-Slide PPT content for teammates
└── README.md                  # Project documentation
```

---

## 🎯 How to Demonstrate in the Hackathon

1. **Start the app:** Run `python3 run.py` and display the dashboard on screen.
2. **Show the Live Stream:** Point out the incoming 1930 complaints with the **"Golden Hour" cashout countdown** on the left panel.
3. **Explore Hotspots on Map:** Switch between hotspot regions (Delhi-NCR, Jamtara, Bengaluru) and click on red pulse rings to reveal the predicted ATM and risk confidence.
4. **Reveal the Mule Money Trail:** Click on the **"🕸️ Multi-Hop Mule Money Trail"** tab to show the force-directed graph revealing how money travels through layered mule accounts.
5. **Simulate a Live Incident:** Click **"⚡ Ingest Live Incident (Simulate)"** at the top right to demonstrate real-time AI ingestion and alert generation.
6. **Take Action:** Click **"Dispatch Beat Patrol"** and **"Trigger 1930 Bank Lien Freeze"**, then open the **"Official I4C FIR Docket"** to show a complete end-to-end operational workflow.

---

## 📚 PPT & Presentation Content
Refer to **[`PRESENTATION_GUIDE.md`](./PRESENTATION_GUIDE.md)** for the slide-by-slide text, architectural diagrams, mathematical formulations, and answers to expected jury questions.
