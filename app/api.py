"""
Cyber-Drishti: FastAPI REST API & Web Application Server
Exposes high-performance endpoints for real-time cyber intelligence,
GIS hotspot feeds, mule account graph networks, and law enforcement actions.
"""

import os
import hashlib
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.simulation_engine import CyberSimulationEngine
from app.predictive_engine import PredictiveAnalyticsEngine

app = FastAPI(
    title="CYBER-DRISHTI // I4C Predictive Cybercrime Analytics",
    description="Predictive Analytics Framework for Cybercrime Complaints to Forecast Cash Withdrawal Hotspots",
    version="1.0.0"
)

# Initialize simulation and predictive ML modules
sim_engine = CyberSimulationEngine(initial_count=32)
pred_engine = PredictiveAnalyticsEngine()

# Mount static directory for frontend assets
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class DispatchRequest(BaseModel):
    incident_id: str
    police_unit: str
    target_atm: str
    notes: Optional[str] = "Immediate tactical intercept dispatched."

class LienFreezeRequest(BaseModel):
    incident_id: str
    target_bank: str
    mule_layer: int
    amount_inr: int

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Cyber-Drishti Backend Active. Building Frontend...</h1>"

@app.get("/api/stats")
async def get_stats():
    incidents = sim_engine.get_all_incidents()
    hotspots = pred_engine.compute_hotspots(incidents)
    kpis = pred_engine.compute_dashboard_kpis(incidents, hotspots)
    return kpis

@app.get("/api/incidents")
async def list_incidents(
    priority: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50
):
    incidents = sim_engine.get_all_incidents()
    filtered = incidents

    if priority and priority.upper() != "ALL":
        filtered = [inc for inc in filtered if priority.upper() in inc.get("priority", "").upper()]

    if category and category.upper() != "ALL":
        filtered = [inc for inc in filtered if category.lower() in inc.get("category", "").lower()]

    return filtered[:limit]

@app.get("/api/incident/{incident_id}")
async def get_incident_details(incident_id: str):
    inc = sim_engine.get_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc

@app.get("/api/hotspots")
async def get_hotspots():
    incidents = sim_engine.get_all_incidents()
    hotspots = pred_engine.compute_hotspots(incidents)
    return {
        "count": len(hotspots),
        "hotspots": hotspots
    }

@app.get("/api/mule-graph/{incident_id}")
async def get_mule_graph(incident_id: str):
    inc = sim_engine.get_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    graph_data = pred_engine.extract_mule_graph(inc)
    return graph_data

@app.post("/api/simulate-live")
async def trigger_live_incident():
    new_incident = sim_engine.trigger_live_incident()
    return {
        "status": "SUCCESS",
        "message": "🚨 New High-Priority Cyber Fraud Complaint Ingested into 1930 Stream",
        "incident": new_incident
    }

@app.post("/api/action/dispatch")
async def dispatch_police_unit(req: DispatchRequest):
    inc = sim_engine.dispatch_incident(
        incident_id=req.incident_id,
        police_unit=req.police_unit,
        target_atm=req.target_atm,
        notes=req.notes or ""
    )
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return {
        "status": "DISPATCH_CONFIRMED",
        "timestamp": inc["dispatch_details"]["timestamp"],
        "incident_id": req.incident_id,
        "assigned_unit": req.police_unit,
        "target_location": req.target_atm,
        "alert_broadcast_channels": ["Police Tetra Wireless", "CCTNS Mobile Dispatch", "Beat Patrol WhatsApp Alert"],
        "eta_mins": inc["dispatch_details"]["eta_mins"],
        "action_log": f"Quick Response Team mobilized to cordon {req.target_atm}. CCTV recording lock active.",
        "incident": inc
    }

@app.post("/api/action/freeze-lien")
async def freeze_bank_lien(req: LienFreezeRequest):
    inc = sim_engine.freeze_incident_lien(
        incident_id=req.incident_id,
        target_bank=req.target_bank,
        mule_layer=req.mule_layer,
        amount_inr=req.amount_inr
    )
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    return {
        "status": "LIEN_FREEZE_TRANSMITTED",
        "timestamp": inc["lien_freeze_details"]["timestamp"],
        "incident_id": req.incident_id,
        "target_bank": req.target_bank,
        "amount_secured_inr": req.amount_inr,
        "cfcfrms_ref_no": inc["lien_freeze_details"]["cfcfrms_ref_no"],
        "action_log": f"Automated 1930 / MHA emergency lien hold executed against Layer {req.mule_layer} destination account. ATM card disabled.",
        "incident": inc
    }

@app.get("/api/dossier/{incident_id}")
async def get_dossier_text(incident_id: str):
    inc = sim_engine.get_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    target = inc.get("target_atm", {})
    mule_chain = inc.get("mule_chain", [])
    
    dossier = f"""================================================================================
INDIAN CYBER CRIME COORDINATION CENTRE (I4C) - MINISTRY OF HOME AFFAIRS
TACTICAL ACTIONABLE CYBER INTELLIGENCE DOSSIER - PS-26184
================================================================================
INCIDENT ID           : {inc['incident_id']}
ACKNOWLEDGEMENT NO    : {inc['acknowledgement_no']}
CRIME CLASSIFICATION  : {inc['category']}
SEVERITY LEVEL        : {inc['severity']}
TOTAL AMOUNT SPHONED  : INR {inc['amount_inr']:,}
VICTIM NAME & BANK    : {inc['victim_name']} ({inc['victim_bank']})
INCIDENT LOGGED AT    : {inc['reported_at']}

--------------------------------------------------------------------------------
PREDICTIVE WITHDRAWAL INTELLIGENCE (AFT SURVIVAL & ST-DBSCAN FORECAST)
--------------------------------------------------------------------------------
PREDICTED CASHOUT TIME: {inc['predicted_cashout_at']}
ESTIMATED TIME TO ACT : {inc['mins_to_cashout']} MINUTES (GOLDEN HOUR)
AFT HAZARD EXPONENT   : {inc.get('hazard_exponent', 0.85)} (Accelerated Failure Time Model)
FORECAST CONFIDENCE   : {inc['confidence_score']}% (Spatio-Temporal GNN & Velocity Model)
PREDICTED ATM NODE    : {target.get('name')}
ATM OPERATING BANK    : {target.get('bank')}
GEO COORDINATES       : LAT {target.get('lat')}, LNG {target.get('lng')}
SEARCH PERIMETER      : {target.get('search_radius_meters')} METERS RADIUS

--------------------------------------------------------------------------------
MULTI-HOP MONEY MULE TRAIL (FORENSIC DAG BREAKDOWN)
--------------------------------------------------------------------------------
"""
    for node in mule_chain:
        if node['type'] == 'VICTIM':
            dossier += f"[HOP 0 - VICTIM]    {node['holder_name']} | {node['bank_name']} | {node['account_num']} | Sent: INR {node['amount_transferred']:,}\n"
        elif 'MULE' in node['type']:
            dossier += f"[HOP {node['layer']} - MULE]      {node['holder_name']} | {node['bank_name']} | {node['account_num']} | Flag: {node.get('kyc_flag','Suspicious')}\n"
        else:
            dossier += f"[FINAL CASH-OUT]   {node.get('atm_name')} | Dispense Target: INR {node['amount_transferred']:,}\n"

    dossier += f"""
--------------------------------------------------------------------------------
LAW ENFORCEMENT ACTION PROTOCOL
--------------------------------------------------------------------------------
DESIGNATED POLICE UNIT: {inc['actionable_intelligence']['assigned_police_unit']}
RECOMMENDED OPERATION : {inc['actionable_intelligence']['suggested_action']}
BANK LIEN STATUS      : {inc['actionable_intelligence']['bank_lien_status']}
CCTV PRESERVATION     : {inc['actionable_intelligence'].get('cctv_preservation_order', 'TRANSMITTED')}
================================================================================
Generated automatically by CYBER-DRISHTI Predictive Analytics Framework.
Confidential - For Law Enforcement and Banking Nodal Use Only.
"""
    
    # Generate Salted SHA-256 Hash for Evidence Chain of Custody
    salt = "I4C_EVIDENCE_SALT_2026"
    raw_content = f"{dossier}{salt}"
    dossier_hash = hashlib.sha256(raw_content.encode('utf-8')).hexdigest()
    
    dossier += f"CRYPTOGRAPHIC EVIDENCE HASH (SHA-256):\n{dossier_hash}\n================================================================================\n"

    return {"incident_id": incident_id, "dossier_text": dossier}
