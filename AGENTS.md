# 🤖 AGENTS.md // Master Context & Instructions for AI Reviewers & Developers

> **Target Audience:** Any AI Assistant (Antigravity, Cursor, Claude Code, Grok, ChatGPT, etc.) reviewing, testing, or upgrading this prototype.
> **Project Name:** **CYBER-DRISHTI** (AI-Powered Predictive Cash-Out Analytics & Preemption Framework)
> **Competition:** Smart India Hackathon (SIH 2026) | **Problem Statement ID:** 26184
> **Client / Organization:** Ministry of Home Affairs (MHA) / Indian Cyber Crime Coordination Centre (I4C), CIS Division

---

## 🎯 1. Executive Summary & Problem Context

The National Cybercrime Reporting Portal (NCRP / 1930 Helpline) receives **8,000+ daily financial fraud complaints**. 
Fraudsters launder stolen money across 3 to 5 layers of "mule accounts" and withdraw physical cash at remote ATMs/CSP kiosks within **45 to 90 minutes** of credit. 

* **The Core Crisis:** Traditional cyber policing is **purely reactive** (investigations occur days/weeks after the cash has already left the digital banking perimeter).
* **The Solution (CYBER-DRISHTI):** Shifts policing to **proactive cash-out preemption** by predicting:
  1. **WHERE:** Target ATM/CSP cluster (latitude, longitude, 300m–1km search radius).
  2. **WHEN:** Dynamic time window ($<35\text{ mins}$) before physical withdrawal occurs ("Golden Hour").
  3. **ACTION:** Automated 1-click dispatch to nearest field beat patrol + automated CFCFRMS (1930) bank lien hold.

---

## 🏗️ 2. Current Architecture & Codebase Map

```
SIH2026/
├── app/
│   ├── __init__.py
│   ├── simulation_engine.py   # Indian Cybercrime & Multi-Hop Mule Chain Generator
│   ├── predictive_engine.py   # Spatio-Temporal DBSCAN, ML Risk Scoring & Graph Traversal
│   ├── api.py                 # FastAPI REST API Endpoints & Server
│   └── static/
│       ├── index.html         # High-contrast tactical glassmorphic dashboard
│       ├── styles.css         # Custom Vanilla CSS Design System (Tailwind-free)
│       └── app.js             # Leaflet GIS mapping, Vis.js graph & live telemetry
├── run.py                     # Single-command startup entrypoint (http://127.0.0.1:8000)
├── PRESENTATION_GUIDE.md      # Official SIH 6-Slide Presentation Deck
├── JURY_QA_MASTER_VAULT.md    # Exhaustive Technical & Legal Q&A Defense Guide
├── README.md                  # Project Quickstart & Documentation
└── AGENTS.md                  # This file
```

---

## 🔬 3. Core Mathematical & Algorithmic Models (Already Implemented)

Any AI modifying or extending the algorithms must understand and preserve these core models:

### 1. Spatio-Temporal Clustering Metric ($D_{ST}$)
Combines Haversine spatial distance with complaint time decay:
$$D_{ST}(p_i, p_j) = \sqrt{\alpha \cdot \left(\frac{d_{Haversine}(p_i, p_j)}{\epsilon_1}\right)^2 + \beta \cdot \left(\frac{|t_i - t_j|}{\epsilon_2}\right)^2}$$

### 2. Time-to-Withdrawal Survival Function ($\hat{T}_{cashout}$)
Closed-form Accelerated Failure Time (AFT) estimator for remaining minutes in the Golden Hour:
$$\hat{T}_{cashout} = T_0 \cdot \exp\left(-\left[\beta_1 \cdot \text{HopDepth} + \beta_2 \cdot \ln\left(\frac{\text{Amount}}{\Delta t_{transfer}}\right) + \beta_3 \cdot \text{DormancyScore} + \beta_4 \cdot \text{HubIndex}\right]\right)$$

### 3. Graph Fan-Out Entropy (Detecting Smurfing / Multi-Split Mule Layers)
$$H_{out}(u) = -\sum_{v \in \mathcal{N}_{out}(u)} p(u \to v) \log_2 p(u \to v)$$

---

## ⚡ 4. REST API Reference (`app/api.py`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main tactical dashboard HTML (`index.html`) |
| `GET` | `/api/stats` | High-level aggregated KPIs (Funds secured, imminent threats, isolated mules) |
| `GET` | `/api/incidents` | Filterable list of active cyber complaints (by priority & category) |
| `GET` | `/api/incident/{id}` | Deep-dive telemetry for a single complaint |
| `GET` | `/api/hotspots` | Computed GeoJSON hotspot clusters with pulse radii & risk levels |
| `GET` | `/api/mule-graph/{id}` | Vis.js node & edge graph dataset for multi-hop money flow |
| `POST` | `/api/simulate-live` | Generates an authentic incoming 1930 cyber fraud complaint |
| `POST` | `/api/action/dispatch` | Simulates real-time dispatch of beat police to predicted coordinates |
| `POST` | `/api/action/freeze-lien`| Simulates instant automated 1930 / CFCFRMS bank account hold |
| `GET` | `/api/dossier/{id}` | Auto-generates formatted, printable I4C intelligence brief |

---

## 📋 5. Strict Constraints & Guidelines for AI Agents

When reviewing or improving this project, **all AI assistants MUST adhere to the following rules**:

1. **Keep it Lightweight & Zero-Build (No Heavy Frameworks):**
   * **Do NOT** convert the frontend to React, Next.js, Angular, or Vue. 
   * Maintain the ultra-fast, zero-dependency **Vanilla HTML5 + CSS + JavaScript** structure. It must run instantly without `npm install` or build steps.
2. **Do NOT Break Working Functionality:**
   * The prototype currently runs flawlessly at `python3 run.py`. Any new features or refactorings must preserve existing endpoints and UI interactions.
3. **Simplicity & Usability First:**
   * The UI is designed for I4C command center operators and police investigators. Keep it clean, intuitive, high-contrast (tactical dark theme), and easy to navigate.
4. **Data Privacy & DPDP Act 2023 Compliance:**
   * Never output unmasked personal identifiable information (PII). All account numbers must use tokenization (`XXXX-XXXX-1234`).
5. **Beginner-Friendly Code Documentation:**
   * The student team consists of **1st-year Computer Science students**. Any newly added code, algorithms, or queries must be cleanly documented and explained in simple terms.
6. **Persistence Strategy for Prototype:**
   * Currently, the system uses the in-memory simulation engine (`simulation_engine.py`). If adding persistence, use **SQLite** or simple JSON storage to avoid requiring complex database setups for judges.

---

## 🚀 6. Recommended High-Impact Areas for Review & Upgrade

If an AI is asked to review and suggest upgrades for this prototype, prioritize these high-value areas:

1. **Enhanced Data Simulation:** Add more diverse Indian cyber scam categories (e.g. SIM Swap, WhatsApp OTP hijack, fake utility bill scams).
2. **Interactive Export Capabilities:** Add 1-click **Export to CSV / PDF** for incident reports and suspect mule lists.
3. **Audio / Visual Alert Effects:** Enhance tactical sound effects (e.g. subtle radar pulse beep on live simulation) with an easy mute toggle.
4. **Offline Mode / Local Cache:** Ensure map tiles and mock data cache gracefully if offline.
5. **Automated Unit Tests:** Add lightweight `pytest` scripts for the ML clustering and API endpoints.

---

*This document was created for the SIH 2026 CYBER-DRISHTI project. Update this file as the project evolves into subsequent phases.*
