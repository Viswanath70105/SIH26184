"""
Cyber-Drishti: Indian Cybercrime Complaint & Mule Account Simulation Engine
Simulates realistic NCRP (1930 Helpline) cyber financial fraud incidents, multi-layer mule account transfers,
and ATM/CSP cash withdrawal patterns across key cyber fraud hubs and metropolitan clusters in India.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from app.predictive_engine import estimate_aft_cashout_window

# Indian Cybercrime Hubs & Metro Incident Centers
REGIONS = [
    {
        "cluster_name": "Delhi-NCR & Mewat Corridor",
        "state": "Delhi / Haryana / Rajasthan",
        "lat": 28.6139,
        "lng": 77.2090,
        "atm_hotspots": [
            {"name": "SBI ATM - Gurugram Cyber Hub", "lat": 28.4952, "lng": 77.0891, "bank": "State Bank of India", "risk_index": 0.94},
            {"name": "HDFC ATM - Nuh Main Market", "lat": 28.1062, "lng": 76.9965, "bank": "HDFC Bank", "risk_index": 0.98},
            {"name": "PNB CSP Kiosk - Bharatpur Border", "lat": 27.2152, "lng": 77.4930, "bank": "Punjab National Bank", "risk_index": 0.96},
            {"name": "Axis Bank ATM - Noida Sector 62", "lat": 28.6270, "lng": 77.3725, "bank": "Axis Bank", "risk_index": 0.89},
            {"name": "ICICI ATM - South Extension Delhi", "lat": 28.5729, "lng": 77.2215, "bank": "ICICI Bank", "risk_index": 0.82}
        ]
    },
    {
        "cluster_name": "Jamtara - Deoghar - Giridih Belt",
        "state": "Jharkhand",
        "lat": 23.9614,
        "lng": 86.8020,
        "atm_hotspots": [
            {"name": "Bank of India ATM - Jamtara Station Rd", "lat": 23.9580, "lng": 86.8001, "bank": "Bank of India", "risk_index": 0.99},
            {"name": "SBI CSP Kiosk - Karmatar Cyber Belt", "lat": 24.0850, "lng": 86.7230, "bank": "State Bank of India", "risk_index": 0.97},
            {"name": "Canara Bank ATM - Deoghar Tower Chowk", "lat": 24.4826, "lng": 86.7000, "bank": "Canara Bank", "risk_index": 0.91}
        ]
    },
    {
        "cluster_name": "Bengaluru Tech Corridor",
        "state": "Karnataka",
        "lat": 12.9716,
        "lng": 77.5946,
        "atm_hotspots": [
            {"name": "Kotak ATM - Marathahalli Junction", "lat": 12.9569, "lng": 77.7011, "bank": "Kotak Mahindra", "risk_index": 0.88},
            {"name": "SBI ATM - Electronic City Phase 1", "lat": 12.8399, "lng": 77.6770, "bank": "State Bank of India", "risk_index": 0.85},
            {"name": "HDFC ATM - Indiranagar 100ft Rd", "lat": 12.9784, "lng": 77.6408, "bank": "HDFC Bank", "risk_index": 0.79}
        ]
    },
    {
        "cluster_name": "Mumbai - Thane - Navi Mumbai Belt",
        "state": "Maharashtra",
        "lat": 19.0760,
        "lng": 72.8777,
        "atm_hotspots": [
            {"name": "Union Bank ATM - Mira Road East", "lat": 19.2813, "lng": 72.8561, "bank": "Union Bank", "risk_index": 0.93},
            {"name": "ICICI ATM - Andheri West Station", "lat": 19.1197, "lng": 72.8464, "bank": "ICICI Bank", "risk_index": 0.87},
            {"name": "HDFC ATM - Vashi Sector 17", "lat": 19.0771, "lng": 72.9986, "bank": "HDFC Bank", "risk_index": 0.84}
        ]
    },
    {
        "cluster_name": "Ahmedabad - Surat Financial Corridor",
        "state": "Gujarat",
        "lat": 23.0225,
        "lng": 72.5714,
        "atm_hotspots": [
            {"name": "Bank of Baroda ATM - Ashram Road", "lat": 23.0338, "lng": 72.5683, "bank": "Bank of Baroda", "risk_index": 0.86},
            {"name": "SBI ATM - Ring Road Surat", "lat": 21.1959, "lng": 72.8302, "bank": "State Bank of India", "risk_index": 0.91}
        ]
    },
    {
        "cluster_name": "Hyderabad Cyberabad Belt",
        "state": "Telangana",
        "lat": 17.3850,
        "lng": 78.4867,
        "atm_hotspots": [
            {"name": "SBI ATM - Madhapur Cyber Towers", "lat": 17.4504, "lng": 78.3808, "bank": "State Bank of India", "risk_index": 0.89},
            {"name": "Axis Bank ATM - Secunderabad Station", "lat": 17.4399, "lng": 78.4983, "bank": "Axis Bank", "risk_index": 0.83}
        ]
    },
    {
        "cluster_name": "Kolkata - Salt Lake - Asansol Hub",
        "state": "West Bengal",
        "lat": 22.5726,
        "lng": 88.3639,
        "atm_hotspots": [
            {"name": "PNB ATM - Sector V Salt Lake", "lat": 22.5804, "lng": 88.4378, "bank": "Punjab National Bank", "risk_index": 0.87},
            {"name": "SBI ATM - Howrah Station South Gate", "lat": 22.5833, "lng": 88.3426, "bank": "State Bank of India", "risk_index": 0.92}
        ]
    }
]

MODUS_OPERANDI_TYPES = [
    {
        "type": "Digital Arrest (CBI / Police Impersonation)",
        "severity": "CRITICAL",
        "avg_amount_range": (150000, 1200000),
        "typical_layers": 3,
        "speed_factor": 1.4,
        "desc": "Victim coerced via video call claiming parcel contains narcotics; forced to transfer funds to 'Supreme Court verification escrow'."
    },
    {
        "type": "Part-Time Task & Telegram Rating Scam",
        "severity": "HIGH",
        "avg_amount_range": (30000, 250000),
        "typical_layers": 2,
        "speed_factor": 1.2,
        "desc": "Victim promised high commissions for rating Google maps / YouTube videos, then prompted to deposit VIP funds."
    },
    {
        "type": "Fake Stock Trading / Institutional IPO Scam",
        "severity": "CRITICAL",
        "avg_amount_range": (200000, 2500000),
        "typical_layers": 4,
        "speed_factor": 1.1,
        "desc": "Bogus trading portal showing artificial 400% profits; victim unable to withdraw without paying 'custom tax'."
    },
    {
        "type": "FedEx / Courier Customs Blackmail",
        "severity": "HIGH",
        "avg_amount_range": (80000, 450000),
        "typical_layers": 2,
        "speed_factor": 1.3,
        "desc": "Fraudster claims parcel addressed to victim seized with illegal passports and narcotics; demands instant clearance fee."
    },
    {
        "type": "Instant APK Loan App Extortion",
        "severity": "MEDIUM",
        "avg_amount_range": (15000, 95000),
        "typical_layers": 2,
        "speed_factor": 1.0,
        "desc": "Malicious loan app accesses contacts and gallery, morphs images, and extorts money into rotating UPI accounts."
    },
    {
        "type": "Aadhaar Enabled Payment (AePS) Biometric Clone",
        "severity": "HIGH",
        "avg_amount_range": (10000, 60000),
        "typical_layers": 1,
        "speed_factor": 1.6,
        "desc": "Cloned silicone thumbprints used at local CSP kiosks for immediate cash drain from victim bank accounts."
    }
]

INDIAN_BANKS = [
    {"name": "State Bank of India", "code": "SBIN"},
    {"name": "HDFC Bank", "code": "HDFC"},
    {"name": "ICICI Bank", "code": "ICIC"},
    {"name": "Punjab National Bank", "code": "PUNB"},
    {"name": "Bank of Baroda", "code": "BARB"},
    {"name": "Axis Bank", "code": "UTIB"},
    {"name": "Canara Bank", "code": "CNRB"},
    {"name": "Kotak Mahindra Bank", "code": "KKBK"},
    {"name": "Airtel Payments Bank", "code": "AIRP"},
    {"name": "Paytm Payments Bank", "code": "PYTM"}
]

FIRST_NAMES = ["Amit", "Rajesh", "Pooja", "Vikram", "Sneha", "Rahul", "Priya", "Ankit", "Deepak", "Rohan", "Sunita", "Manoj", "Kavita", "Suresh", "Divya", "Arjun", "Neha", "Varun", "Meera"]
LAST_NAMES = ["Sharma", "Verma", "Singh", "Patel", "Gupta", "Yadav", "Kumar", "Reddy", "Nair", "Das", "Joshi", "Choudhury", "Mishra", "Mehta", "Iyer", "Kulkarni"]

def generate_random_account() -> str:
    return str(random.randint(10000000000, 99999999999))

def generate_random_ifsc(bank_code: str) -> str:
    return f"{bank_code}0{random.randint(100000, 999999)}"

def generate_mule_chain(victim_amount: int, num_layers: int, target_atm: Dict[str, Any], is_smurfing: bool = False) -> List[Dict[str, Any]]:
    """
    Simulates realistic multi-hop money flow across layered mule accounts to destination ATM/CSP.
    Supports 1-to-N branching (Smurfing / Structuring DAGs) for sophisticated scam syndicates.
    """
    nodes = []
    
    # Node 0: Victim Node
    victim_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    victim_bank = random.choice(INDIAN_BANKS)
    nodes.append({
        "node_id": 0,
        "parent_id": None,
        "layer": 0,
        "type": "VICTIM",
        "holder_name": victim_name,
        "bank_name": victim_bank["name"],
        "account_num": f"XXXX-XXXX-{generate_random_account()[-4:]}",
        "ifsc": generate_random_ifsc(victim_bank["code"]),
        "amount_transferred": victim_amount,
        "txn_id": f"UPI/TXN/{random.randint(100000000000, 999999999999)}",
        "time_offset_mins": 0,
        "mule_risk_score": 0.05,
        "kyc_status": "VERIFIED_CITIZEN"
    })
    
    current_node_id = 1
    cumulative_time = random.randint(4, 10)
    
    if is_smurfing and victim_amount >= 150000:
        # Generate 2-way Branching Layer 1 (Structuring / Smurfing Pattern)
        split_ratio = random.uniform(0.48, 0.52)
        amount_branch_a = int(victim_amount * split_ratio)
        amount_branch_b = int(victim_amount * (1.0 - split_ratio) * 0.98)
        
        bank_a = random.choice(INDIAN_BANKS)
        bank_b = random.choice([b for b in INDIAN_BANKS if b != bank_a])
        
        node_a_id = current_node_id
        nodes.append({
            "node_id": node_a_id,
            "parent_id": 0,
            "layer": 1,
            "type": "MULE_L1 (Branch A)",
            "holder_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "bank_name": bank_a["name"],
            "account_num": f"XXXX-XXXX-{generate_random_account()[-4:]}",
            "ifsc": generate_random_ifsc(bank_a["code"]),
            "amount_transferred": amount_branch_a,
            "txn_id": f"IMPS/{random.randint(100000000000, 999999999999)}",
            "time_offset_mins": cumulative_time,
            "mule_risk_score": 0.88,
            "kyc_status": "SUSPICIOUS_MULE",
            "kyc_flag": "Rapid Split Structuring (< 3 Mins)"
        })
        current_node_id += 1
        
        node_b_id = current_node_id
        nodes.append({
            "node_id": node_b_id,
            "parent_id": 0,
            "layer": 1,
            "type": "MULE_L1 (Branch B)",
            "holder_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "bank_name": bank_b["name"],
            "account_num": f"XXXX-XXXX-{generate_random_account()[-4:]}",
            "ifsc": generate_random_ifsc(bank_b["code"]),
            "amount_transferred": amount_branch_b,
            "txn_id": f"IMPS/{random.randint(100000000000, 999999999999)}",
            "time_offset_mins": cumulative_time + random.randint(1, 3),
            "mule_risk_score": 0.86,
            "kyc_status": "SUSPICIOUS_MULE",
            "kyc_flag": "Dormant Jan-Dhan Mule Reactivated"
        })
        current_node_id += 1
        
        # Layer 2 Aggregator Node
        cumulative_time += random.randint(6, 14)
        agg_bank = random.choice(INDIAN_BANKS)
        agg_amount = int((amount_branch_a + amount_branch_b) * 0.96)
        agg_node_id = current_node_id
        
        nodes.append({
            "node_id": agg_node_id,
            "parent_id": node_a_id,  # Connects from branch A
            "layer": 2,
            "type": "MULE_L2 (Aggregator)",
            "holder_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "bank_name": agg_bank["name"],
            "account_num": f"XXXX-XXXX-{generate_random_account()[-4:]}",
            "ifsc": generate_random_ifsc(agg_bank["code"]),
            "amount_transferred": agg_amount,
            "txn_id": f"NEFT/{random.randint(100000000000, 999999999999)}",
            "time_offset_mins": cumulative_time,
            "mule_risk_score": 0.94,
            "kyc_status": "HIGH_RISK_AGGREGATOR",
            "kyc_flag": "Shell Corporate Current Account"
        })
        current_node_id += 1
        
        # Final Target Cash-Out ATM
        nodes.append({
            "node_id": current_node_id,
            "parent_id": agg_node_id,
            "layer": 3,
            "type": "CASH_WITHDRAWAL_TARGET",
            "holder_name": "ATM / CSP Cash Dispenser",
            "bank_name": target_atm["bank"],
            "atm_name": target_atm["name"],
            "lat": target_atm["lat"] + random.uniform(-0.002, 0.002),
            "lng": target_atm["lng"] + random.uniform(-0.002, 0.002),
            "amount_transferred": agg_amount,
            "time_offset_mins": cumulative_time + random.randint(8, 20),
            "mule_risk_score": target_atm["risk_index"],
            "status": "PREDICTED_IMMINENT"
        })
    else:
        # Standard Multi-Hop Linear Mule Chain
        remaining_amount = victim_amount
        prev_node_id = 0
        
        for layer_idx in range(1, num_layers + 1):
            mule_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)} (Mule L{layer_idx})"
            mule_bank = random.choice(INDIAN_BANKS)
            split_amount = int(remaining_amount * random.uniform(0.93, 0.98))
            
            kyc_flags = random.choice([
                "Dormant Account Reactivated Recently",
                "Aadhaar Address in High-Risk Jamtara/Mewat Pin Code",
                "Rapid IN-OUT Balance Velocity within 2 Mins",
                "Mismatched Device Geolocation / Multi-IP Hopping",
                "Shell Enterprise Current Account Opened via Rent-a-KYC"
            ])
            
            nodes.append({
                "node_id": current_node_id,
                "parent_id": prev_node_id,
                "layer": layer_idx,
                "type": f"MULE_L{layer_idx}",
                "holder_name": mule_name,
                "bank_name": mule_bank["name"],
                "account_num": f"XXXX-XXXX-{generate_random_account()[-4:]}",
                "ifsc": generate_random_ifsc(mule_bank["code"]),
                "amount_transferred": split_amount,
                "txn_id": f"IMPS/{random.randint(100000000000, 999999999999)}",
                "time_offset_mins": cumulative_time,
                "mule_risk_score": round(0.78 + (layer_idx * 0.06), 2),
                "kyc_status": "SUSPICIOUS_MULE",
                "kyc_flag": kyc_flags
            })
            prev_node_id = current_node_id
            current_node_id += 1
            remaining_amount = split_amount
            cumulative_time += random.randint(6, 16)
            
        # Final Target Node: Cash-Out ATM
        nodes.append({
            "node_id": current_node_id,
            "parent_id": prev_node_id,
            "layer": num_layers + 1,
            "type": "CASH_WITHDRAWAL_TARGET",
            "holder_name": "ATM / CSP Cash Dispenser",
            "bank_name": target_atm["bank"],
            "atm_name": target_atm["name"],
            "lat": target_atm["lat"] + random.uniform(-0.002, 0.002),
            "lng": target_atm["lng"] + random.uniform(-0.002, 0.002),
            "amount_transferred": remaining_amount,
            "time_offset_mins": cumulative_time + random.randint(8, 22),
            "mule_risk_score": target_atm["risk_index"],
            "status": "PREDICTED_IMMINENT"
        })
        
    return nodes

def generate_incident(incident_id_num: int, is_live: bool = False) -> Dict[str, Any]:
    """Generates a comprehensive simulated cybercrime complaint docket with mathematical predictive metrics."""
    region = random.choice(REGIONS)
    target_atm = random.choice(region["atm_hotspots"])
    modus = random.choice(MODUS_OPERANDI_TYPES)
    
    amount = random.randint(modus["avg_amount_range"][0], modus["avg_amount_range"][1])
    amount = round(amount / 1000) * 1000
    
    is_smurfing = random.random() < 0.45 or modus["severity"] == "CRITICAL"
    mule_chain = generate_mule_chain(amount, modus["typical_layers"], target_atm, is_smurfing=is_smurfing)
    
    now = datetime.now()
    if is_live:
        reported_time = now - timedelta(minutes=random.randint(2, 12))
    else:
        reported_time = now - timedelta(minutes=random.randint(20, 360))
        
    incident_id = f"NCRP-2026-I4C-{incident_id_num:05d}"
    
    # Mathematical AFT Survival Model Calculation
    hop_depth = len([n for n in mule_chain if "MULE" in n.get("type", "")])
    last_hop_time = mule_chain[-1].get("time_offset_mins", 25)
    dormancy_weight = 0.85 if "Dormant" in str(mule_chain) else 0.45
    
    aft_metrics = estimate_aft_cashout_window(
        hop_depth=hop_depth,
        amount=amount,
        transfer_time_delta_mins=last_hop_time,
        dormancy_score=dormancy_weight,
        hub_risk_index=target_atm["risk_index"]
    )
    
    mins_remaining = aft_metrics["mins_to_cashout"]
    confidence = aft_metrics["confidence_score"]
    predicted_cashout_time = now + timedelta(minutes=mins_remaining)
    
    # Threat Priority Level
    if mins_remaining <= 35:
        priority = "CRITICAL (IMMINENT CASH-OUT)"
    elif mins_remaining <= 75:
        priority = "HIGH (ACTIVE MULE HOPS)"
    else:
        priority = "MODERATE (TRACE STAGE)"
        
    police_stations = [
        f"Cyber Crime Police Station, {region['state']}",
        f"Special Cyber Cell, Sector {random.randint(1, 40)}",
        f"Crime Branch Cyber Division - Beat Patrol {random.randint(101, 199)}"
    ]
    
    return {
        "incident_id": incident_id,
        "acknowledgement_no": f"ACK-1930-{random.randint(1000000, 9999999)}",
        "category": modus["type"],
        "severity": modus["severity"],
        "description": modus["desc"],
        "amount_inr": amount,
        "region_cluster": region["cluster_name"],
        "state": region["state"],
        "victim_name": mule_chain[0]["holder_name"],
        "victim_bank": mule_chain[0]["bank_name"],
        "reported_at": reported_time.strftime("%Y-%m-%d %H:%M:%S"),
        "predicted_cashout_at": predicted_cashout_time.strftime("%Y-%m-%d %H:%M:%S"),
        "mins_to_cashout": mins_remaining,
        "priority": priority,
        "confidence_score": confidence,
        "hazard_exponent": aft_metrics["hazard_exponent"],
        "is_dispatched": False,
        "is_lien_frozen": False,
        "dispatch_details": None,
        "lien_freeze_details": None,
        "target_atm": {
            "name": target_atm["name"],
            "bank": target_atm["bank"],
            "lat": target_atm["lat"],
            "lng": target_atm["lng"],
            "risk_index": target_atm["risk_index"],
            "search_radius_meters": random.choice([300, 500, 750, 1000])
        },
        "mule_hops_count": hop_depth,
        "mule_chain": mule_chain,
        "actionable_intelligence": {
            "assigned_police_unit": random.choice(police_stations),
            "suggested_action": f"Alert Beat Patrol within {random.choice([300, 500])}m of {target_atm['name']}; Trigger instant 1930 lien freeze on Layer {hop_depth} mule account.",
            "bank_lien_status": "READY FOR LIEN HOLD",
            "cctv_preservation_order": "TRANSMITTED TO BRANCH NODAL OFFICER"
        }
    }

class CyberSimulationEngine:
    def __init__(self, initial_count: int = 25):
        self.incidents: List[Dict[str, Any]] = []
        self.incident_counter = 9100
        self._seed_data(initial_count)
        
    def _seed_data(self, count: int):
        for _ in range(count):
            self.incident_counter += 1
            is_live = random.random() < 0.40
            self.incidents.append(generate_incident(self.incident_counter, is_live=is_live))
            
        self.incidents.sort(key=lambda x: x["mins_to_cashout"])
        
    def get_all_incidents(self) -> List[Dict[str, Any]]:
        return self.incidents
        
    def get_incident_by_id(self, incident_id: str) -> Dict[str, Any]:
        for inc in self.incidents:
            if inc["incident_id"] == incident_id:
                return inc
        return None

    def trigger_live_incident(self) -> Dict[str, Any]:
        self.incident_counter += 1
        new_inc = generate_incident(self.incident_counter, is_live=True)
        self.incidents.insert(0, new_inc)
        return new_inc

    def dispatch_incident(self, incident_id: str, police_unit: str, target_atm: str, notes: str = "") -> Optional[Dict[str, Any]]:
        inc = self.get_incident_by_id(incident_id)
        if not inc:
            return None
        
        inc["is_dispatched"] = True
        inc["dispatch_details"] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "assigned_unit": police_unit,
            "target_location": target_atm,
            "eta_mins": random.randint(6, 12),
            "status": "CORDON_ACTIVE",
            "notes": notes or "Immediate quick response beat patrol mobilized."
        }
        return inc

    def freeze_incident_lien(self, incident_id: str, target_bank: str, mule_layer: int, amount_inr: int) -> Optional[Dict[str, Any]]:
        inc = self.get_incident_by_id(incident_id)
        if not inc:
            return None
            
        inc["is_lien_frozen"] = True
        ref_no = f"CFCFRMS-1930-{incident_id[-5:]}-{random.randint(100, 999)}"
        inc["lien_freeze_details"] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_bank": target_bank,
            "mule_layer": mule_layer,
            "amount_secured_inr": amount_inr,
            "cfcfrms_ref_no": ref_no,
            "status": "FUNDS_LOCKED"
        }
        inc["actionable_intelligence"]["bank_lien_status"] = f"FROZEN (REF: {ref_no})"
        return inc
