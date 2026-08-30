/**
 * CYBER-DRISHTI // I4C Predictive Cybercrime Analytics Client Engine
 * Handles GIS Heatmap Rendering, Multi-Hop Vis.js Graph Visualization,
 * Real-time Telemetry, and Law Enforcement Rapid Action Dispatches.
 */

let map = null;
let mapMarkers = [];
let mapCircles = [];
let networkGraph = null;
let allIncidents = [];
let selectedIncidentId = null;
let currentTab = 'map';

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initLeafletMap();
    initVisGraph();
    setupEventListeners();
    refreshAllData();

    // Live clock ticker & countdown refresher every second
    setInterval(updateCountdowns, 1000);
    // Poll for updates every 10 seconds
    setInterval(refreshAllData, 10000);
});

/* ==========================================================================
   Map Initialization (Leaflet with Dark Tactical CartoDB Tiles)
   ========================================================================== */
function initLeafletMap() {
    // Default center on India
    map = L.map('leaflet-map', {
        center: [22.5937, 78.9629],
        zoom: 5,
        zoomControl: true
    });

    // High performance dark tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
}

/* ==========================================================================
   Vis.js Mule Network Graph Initialization
   ========================================================================== */
function initVisGraph() {
    const container = document.getElementById('mule-network-graph');
    const data = { nodes: [], edges: [] };
    const options = {
        nodes: {
            font: { color: '#ffffff', size: 12, face: 'Inter, sans-serif' },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            width: 2,
            shadow: true,
            arrows: { to: { enabled: true, scaleFactor: 1.2 } },
            smooth: { type: 'cubicBezier', forceDirection: 'horizontal' }
        },
        physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
                gravitationalConstant: -50,
                centralGravity: 0.01,
                springLength: 120,
                springConstant: 0.08
            }
        },
        interaction: { hover: true, tooltipDelay: 100 }
    };
    networkGraph = new vis.Network(container, data, options);
}

/* ==========================================================================
   Data Fetching & State Updates
   ========================================================================== */
async function refreshAllData() {
    await Promise.all([
        fetchStats(),
        fetchHotspots(),
        fetchIncidents()
    ]);
}

async function fetchStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        document.getElementById('kpi-imminent').innerText = data.imminent_cashouts_active;
        document.getElementById('kpi-intercepted').innerText = '₹' + (data.total_funds_intercepted_inr / 100000).toFixed(1) + ' L';
        document.getElementById('kpi-mules').innerText = data.mule_nodes_isolated;
        document.getElementById('kpi-leadtime').innerText = data.avg_preemption_lead_time_mins + ' Min';
    } catch (err) {
        console.error('Error fetching stats:', err);
    }
}

async function fetchHotspots() {
    try {
        const res = await fetch('/api/hotspots');
        const data = await res.json();
        renderHotspotsOnMap(data.hotspots);
    } catch (err) {
        console.error('Error fetching hotspots:', err);
    }
}

async function fetchIncidents() {
    try {
        const priority = document.getElementById('filter-priority').value;
        const category = document.getElementById('filter-category').value;
        const url = `/api/incidents?priority=${encodeURIComponent(priority)}&category=${encodeURIComponent(category)}`;
        
        const res = await fetch(url);
        const incidents = await res.json();
        allIncidents = incidents;
        renderIncidentList(incidents);

        // Preserve current selection or auto-select first
        if (selectedIncidentId) {
            const exists = allIncidents.some(i => i.incident_id === selectedIncidentId);
            if (exists) {
                selectIncident(selectedIncidentId, false);
            } else if (incidents.length > 0) {
                selectIncident(incidents[0].incident_id, true);
            }
        } else if (incidents.length > 0) {
            selectIncident(incidents[0].incident_id, true);
        }
    } catch (err) {
        console.error('Error fetching incidents:', err);
    }
}

/* ==========================================================================
   UI Rendering Functions
   ========================================================================== */
function renderHotspotsOnMap(hotspots) {
    if (!map) return;

    // Clear existing markers & circles
    mapMarkers.forEach(m => map.removeLayer(m));
    mapCircles.forEach(c => map.removeLayer(c));
    mapMarkers = [];
    mapCircles = [];

    hotspots.forEach(h => {
        // Pulse Circle
        const circle = L.circle([h.lat, h.lng], {
            color: h.pulse_color,
            fillColor: h.pulse_color,
            fillOpacity: 0.25,
            radius: h.radius_meters,
            weight: 2
        }).addTo(map);
        mapCircles.push(circle);

        // Marker with custom cyber icon
        const customIcon = L.divIcon({
            className: 'custom-atm-marker',
            html: `<div style="background:${h.pulse_color}; width:14px; height:14px; border-radius:50%; border:2px solid #fff; box-shadow:0 0 12px ${h.pulse_color}; cursor:pointer;"></div>`,
            iconSize: [14, 14],
            iconAnchor: [7, 7]
        });

        const marker = L.marker([h.lat, h.lng], { icon: customIcon }).addTo(map);
        marker.bindPopup(`
            <div style="font-family:Inter,sans-serif; font-size:12px; color:#0f172a; padding:4px;">
                <b style="color:#b91c1c;">🚨 PREDICTED WITHDRAWAL HOTSPOT</b><br/>
                <b>${h.atm_name}</b><br/>
                <span>Region: ${h.region}</span><br/>
                <span>Bank: ${h.bank}</span><br/>
                <span>Risk Score: <b>${h.risk_score}%</b></span><br/>
                <span>Active Threats: <b>${h.imminent_threats}</b></span><br/>
                <span>Amount at Risk: <b>₹${h.total_amount_inr.toLocaleString('en-IN')}</b></span>
            </div>
        `);
        mapMarkers.push(marker);
    });
}

function renderIncidentList(incidents) {
    const listContainer = document.getElementById('incident-list-container');
    listContainer.innerHTML = '';

    if (incidents.length === 0) {
        listContainer.innerHTML = '<div style="text-align:center; color:#64748b; padding:20px; font-size:13px;">No complaints match filters</div>';
        return;
    }

    incidents.forEach(inc => {
        const card = document.createElement('div');
        card.className = `incident-card ${inc.incident_id === selectedIncidentId ? 'active' : ''}`;
        card.id = `card-${inc.incident_id}`;
        card.onclick = () => selectIncident(inc.incident_id);

        let badgeClass = 'badge-moderate';
        if (inc.mins_to_cashout <= 35) badgeClass = 'badge-critical';
        else if (inc.mins_to_cashout <= 70) badgeClass = 'badge-high';

        let actionBadges = '';
        if (inc.is_dispatched || inc.is_lien_frozen) {
            actionBadges = '<div class="action-badges-row">';
            if (inc.is_dispatched) {
                actionBadges += '<span class="action-tag tag-dispatched">🚔 Dispatched</span>';
            }
            if (inc.is_lien_frozen) {
                actionBadges += '<span class="action-tag tag-frozen">🔒 Lien Hold</span>';
            }
            actionBadges += '</div>';
        }

        card.innerHTML = `
            <div class="card-top">
                <span class="incident-id">${inc.incident_id}</span>
                <span class="badge ${badgeClass}">${inc.mins_to_cashout <= 35 ? 'IMMINENT' : inc.severity}</span>
            </div>
            <div class="card-category">${inc.category}</div>
            <div class="card-details">
                <span class="amount-tag">₹${inc.amount_inr.toLocaleString('en-IN')}</span>
                <span class="countdown-tag ${inc.mins_to_cashout <= 15 ? 'urgent' : ''}" data-target-time="${inc.predicted_cashout_at}" data-incident-id="${inc.incident_id}">
                    ⏱️ ${inc.mins_to_cashout}m 00s to cash-out
                </span>
            </div>
            ${actionBadges}
        `;
        listContainer.appendChild(card);
    });
}

async function selectIncident(incidentId, flyTo = true) {
    selectedIncidentId = incidentId;

    // Highlight card in list
    document.querySelectorAll('.incident-card').forEach(c => c.classList.remove('active'));
    const targetCard = document.getElementById(`card-${incidentId}`);
    if (targetCard) targetCard.classList.add('active');

    const inc = allIncidents.find(i => i.incident_id === incidentId);
    if (!inc) return;

    // Update Right Panel (Intelligence Dossier & LEA Rapid Action)
    document.getElementById('dossier-id').innerText = inc.incident_id;
    document.getElementById('dossier-ack').innerText = inc.acknowledgement_no;
    document.getElementById('dossier-category').innerText = inc.category;
    document.getElementById('dossier-victim').innerText = `${inc.victim_name} (${inc.victim_bank})`;
    document.getElementById('dossier-amount').innerText = '₹' + inc.amount_inr.toLocaleString('en-IN');
    document.getElementById('dossier-atm-name').innerText = inc.target_atm.name;
    document.getElementById('dossier-atm-coords').innerText = `LAT: ${inc.target_atm.lat.toFixed(4)}, LNG: ${inc.target_atm.lng.toFixed(4)} (Radius: ${inc.target_atm.search_radius_meters}m)`;
    document.getElementById('dossier-confidence').innerText = `${inc.confidence_score}%`;
    document.getElementById('dossier-mins').innerText = `${inc.mins_to_cashout} Mins`;
    document.getElementById('dossier-police-unit').innerText = inc.actionable_intelligence.assigned_police_unit;
    document.getElementById('dossier-action-rec').innerText = inc.actionable_intelligence.suggested_action;

    // Dynamically update action buttons based on this specific incident's state
    const btnDispatch = document.getElementById('btn-dispatch');
    const btnFreeze = document.getElementById('btn-freeze');

    if (btnDispatch) {
        if (inc.is_dispatched) {
            btnDispatch.innerHTML = '<span>✅</span> BEAT PATROL DISPATCHED (CORDON ACTIVE)';
            btnDispatch.style.background = '#059669';
            btnDispatch.style.boxShadow = '0 0 12px rgba(5, 150, 105, 0.4)';
            btnDispatch.style.cursor = 'default';
            btnDispatch.disabled = true;
        } else {
            btnDispatch.innerHTML = '<span>🚨</span> Dispatch Quick Response Beat Patrol';
            btnDispatch.style.background = '';
            btnDispatch.style.boxShadow = '';
            btnDispatch.style.cursor = 'pointer';
            btnDispatch.disabled = false;
        }
    }

    if (btnFreeze) {
        if (inc.is_lien_frozen) {
            btnFreeze.innerHTML = `<span>🔒</span> LIEN FROZEN (₹${inc.amount_inr.toLocaleString('en-IN')})`;
            btnFreeze.style.background = '#0284c7';
            btnFreeze.style.boxShadow = '0 0 12px rgba(2, 132, 199, 0.4)';
            btnFreeze.style.cursor = 'default';
            btnFreeze.disabled = true;
        } else {
            btnFreeze.innerHTML = '<span>⚡</span> Trigger 1930 Automated Lien Hold';
            btnFreeze.style.background = '';
            btnFreeze.style.boxShadow = '';
            btnFreeze.style.cursor = 'pointer';
            btnFreeze.disabled = false;
        }
    }

    // Progress bar for Golden Hour
    const pct = Math.max(10, Math.min(100, (1 - (inc.mins_to_cashout / 90)) * 100));
    document.getElementById('progress-bar-fill').style.width = `${pct}%`;

    // Center map on target ATM if requested
    if (flyTo && map && inc.target_atm.lat && inc.target_atm.lng) {
        map.flyTo([inc.target_atm.lat, inc.target_atm.lng], 13, { duration: 1.2 });
    }

    // Load Mule Graph for this incident
    fetchMuleGraph(incidentId);
}

async function fetchMuleGraph(incidentId) {
    try {
        const res = await fetch(`/api/mule-graph/${incidentId}`);
        const data = await res.json();
        if (networkGraph) {
            networkGraph.setData(data);
        }
    } catch (err) {
        console.error('Error fetching mule graph:', err);
    }
}

/* ==========================================================================
   Interactive Actions (Dispatch, Freeze, Simulate)
   ========================================================================== */
async function triggerSimulation() {
    try {
        const res = await fetch('/api/simulate-live', { method: 'POST' });
        const result = await res.json();
        
        showToast(`🚨 ${result.message}`);
        await refreshAllData();
        if (result.incident) {
            selectIncident(result.incident.incident_id);
        }
    } catch (err) {
        console.error('Simulation error:', err);
    }
}

async function dispatchBeatPolice() {
    if (!selectedIncidentId) return;
    const inc = allIncidents.find(i => i.incident_id === selectedIncidentId);
    if (!inc || inc.is_dispatched) return;

    try {
        const res = await fetch('/api/action/dispatch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                incident_id: inc.incident_id,
                police_unit: inc.actionable_intelligence.assigned_police_unit,
                target_atm: inc.target_atm.name
            })
        });
        const data = await res.json();
        
        // Mutate local state
        inc.is_dispatched = true;
        if (data.incident && data.incident.dispatch_details) {
            inc.dispatch_details = data.incident.dispatch_details;
        }

        showToast(`🚔 Beat Patrol Dispatched to ${inc.target_atm.name} (ETA: ${data.eta_mins || 8} mins)`);
        selectIncident(inc.incident_id);
        renderIncidentList(allIncidents);
    } catch (err) {
        console.error('Dispatch error:', err);
    }
}

async function freezeBankLien() {
    if (!selectedIncidentId) return;
    const inc = allIncidents.find(i => i.incident_id === selectedIncidentId);
    if (!inc || inc.is_lien_frozen) return;

    try {
        const res = await fetch('/api/action/freeze-lien', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                incident_id: inc.incident_id,
                target_bank: inc.target_atm.bank,
                mule_layer: inc.mule_hops_count,
                amount_inr: inc.amount_inr
            })
        });
        const data = await res.json();
        
        // Mutate local state
        inc.is_lien_frozen = true;
        if (data.incident && data.incident.lien_freeze_details) {
            inc.lien_freeze_details = data.incident.lien_freeze_details;
            inc.actionable_intelligence.bank_lien_status = data.incident.actionable_intelligence.bank_lien_status;
        }

        showToast(`⚡ 1930 / CFCFRMS Lien Hold Executed: ₹${inc.amount_inr.toLocaleString('en-IN')} Secured`);
        selectIncident(inc.incident_id);
        renderIncidentList(allIncidents);
    } catch (err) {
        console.error('Lien error:', err);
    }
}

async function openDossierModal() {
    if (!selectedIncidentId) return;
    try {
        const res = await fetch(`/api/dossier/${selectedIncidentId}`);
        const data = await res.json();
        
        document.getElementById('modal-dossier-content').innerText = data.dossier_text;
        document.getElementById('dossier-modal').style.display = 'flex';
    } catch (err) {
        console.error('Error fetching dossier:', err);
    }
}

function closeDossierModal() {
    document.getElementById('dossier-modal').style.display = 'none';
}

function printDossier() {
    const printWindow = window.open('', '_blank');
    const content = document.getElementById('modal-dossier-content').innerText;
    printWindow.document.write(`<pre style="font-family:monospace; padding:20px; font-size:12px;">${content}</pre>`);
    printWindow.document.close();
    printWindow.print();
}

function showToast(message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>🔔</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4500);
}

function switchTab(tabName) {
    currentTab = tabName;
    const mapEl = document.getElementById('leaflet-map');
    const graphEl = document.getElementById('mule-network-graph');
    const tabMapBtn = document.getElementById('tab-map-btn');
    const tabGraphBtn = document.getElementById('tab-graph-btn');

    if (tabName === 'map') {
        mapEl.style.display = 'block';
        graphEl.style.display = 'none';
        tabMapBtn.classList.add('active');
        tabGraphBtn.classList.remove('active');
        if (map) map.invalidateSize();
    } else {
        mapEl.style.display = 'none';
        graphEl.style.display = 'block';
        tabMapBtn.classList.remove('active');
        tabGraphBtn.classList.add('active');
        if (networkGraph) networkGraph.fit();
    }
}

function zoomToRegion(regionName) {
    switchTab('map');
    if (!map) return;

    if (regionName === 'ncr') map.flyTo([28.6139, 77.2090], 10);
    else if (regionName === 'jamtara') map.flyTo([23.9614, 86.8020], 10);
    else if (regionName === 'bengaluru') map.flyTo([12.9716, 77.5946], 11);
    else if (regionName === 'mumbai') map.flyTo([19.0760, 72.8777], 11);
    else map.flyTo([22.5937, 78.9629], 5);
}

function updateCountdowns() {
    const now = Date.now();
    const countdownTags = document.querySelectorAll('.countdown-tag');
    
    countdownTags.forEach(el => {
        const targetTimeStr = el.getAttribute('data-target-time');
        if (!targetTimeStr) return;
        
        const targetTime = new Date(targetTimeStr.replace(' ', 'T')).getTime();
        const diffSecs = Math.floor((targetTime - now) / 1000);
        
        if (diffSecs <= 0) {
            el.innerText = '⚠️ CASHOUT IMMINENT / EXPIRED';
            el.classList.add('urgent');
        } else {
            const mins = Math.floor(diffSecs / 60);
            const secs = diffSecs % 60;
            const formattedSecs = secs < 10 ? '0' + secs : secs;
            el.innerText = `⏱️ ${mins}m ${formattedSecs}s to cash-out`;
            
            if (mins <= 15) {
                el.classList.add('urgent');
            } else {
                el.classList.remove('urgent');
            }
        }
    });

    // Also update selected incident panel countdown and progress bar in real time
    if (selectedIncidentId) {
        const inc = allIncidents.find(i => i.incident_id === selectedIncidentId);
        if (inc && inc.predicted_cashout_at) {
            const targetTime = new Date(inc.predicted_cashout_at.replace(' ', 'T')).getTime();
            const diffSecs = Math.floor((targetTime - now) / 1000);
            const minsEl = document.getElementById('dossier-mins');
            const barFill = document.getElementById('progress-bar-fill');
            
            if (diffSecs <= 0) {
                if (minsEl) minsEl.innerText = '00m 00s (WINDOW ELAPSED)';
                if (barFill) barFill.style.width = '100%';
            } else {
                const mins = Math.floor(diffSecs / 60);
                const secs = diffSecs % 60;
                const formattedSecs = secs < 10 ? '0' + secs : secs;
                if (minsEl) minsEl.innerText = `${mins}m ${formattedSecs}s (Golden Hour)`;
                
                // 90 minutes baseline = 5400 seconds
                const pct = Math.max(10, Math.min(100, (1 - (diffSecs / 5400)) * 100));
                if (barFill) barFill.style.width = `${pct.toFixed(1)}%`;
            }
        }
    }
}

function filterIncidents() {
    const priority = document.getElementById('filter-priority').value.toUpperCase();
    const category = document.getElementById('filter-category').value.toLowerCase();
    const searchInput = document.getElementById('filter-search');
    const searchQuery = searchInput ? searchInput.value.toLowerCase().trim() : '';

    const filtered = allIncidents.filter(inc => {
        // Priority filter
        if (priority !== 'ALL' && !inc.priority.toUpperCase().includes(priority)) {
            return false;
        }
        // Category filter
        if (category !== 'all' && !inc.category.toLowerCase().includes(category)) {
            return false;
        }
        // Search query filter
        if (searchQuery) {
            const targetAtm = inc.target_atm || {};
            const haystack = [
                inc.incident_id,
                inc.acknowledgement_no,
                inc.category,
                inc.victim_name,
                inc.victim_bank,
                targetAtm.name,
                targetAtm.bank,
                inc.region_cluster,
                inc.state,
                ...(inc.mule_chain || []).map(m => `${m.holder_name} ${m.bank_name} ${m.account_num} ${m.ifsc}`)
            ].join(' ').toLowerCase();

            if (!haystack.includes(searchQuery)) {
                return false;
            }
        }
        return true;
    });

    renderIncidentList(filtered);
    
    // Auto-select first in filtered list if current selection is filtered out
    if (filtered.length > 0) {
        const currentVisible = filtered.some(i => i.incident_id === selectedIncidentId);
        if (!currentVisible) {
            selectIncident(filtered[0].incident_id, true);
        }
    }
}

function exportIncidentsCSV() {
    if (!allIncidents || allIncidents.length === 0) {
        showToast('No incident records to export');
        return;
    }

    const headers = [
        'Incident ID',
        'Acknowledgement No',
        'Crime Classification',
        'Severity',
        'Loss Amount (INR)',
        'Victim Name',
        'Victim Bank',
        'Incident Logged At',
        'Predicted Cashout At',
        'Minutes Remaining',
        'Target ATM Kiosk',
        'ATM Operating Bank',
        'Latitude',
        'Longitude',
        'Search Radius (Meters)',
        'Mule Hop Depth',
        'Dispatch Status',
        'Lien Hold Status',
        'Assigned Police Unit'
    ];

    const csvRows = [headers.join(',')];

    allIncidents.forEach(inc => {
        const target = inc.target_atm || {};
        const row = [
            `"${inc.incident_id}"`,
            `"${inc.acknowledgement_no}"`,
            `"${inc.category}"`,
            `"${inc.severity}"`,
            inc.amount_inr,
            `"${inc.victim_name}"`,
            `"${inc.victim_bank}"`,
            `"${inc.reported_at}"`,
            `"${inc.predicted_cashout_at}"`,
            inc.mins_to_cashout,
            `"${target.name || ''}"`,
            `"${target.bank || ''}"`,
            target.lat || 0,
            target.lng || 0,
            target.search_radius_meters || 500,
            inc.mule_hops_count || 2,
            inc.is_dispatched ? '"DISPATCHED"' : '"PENDING"',
            inc.is_lien_frozen ? '"LIEN_FROZEN"' : '"READY"',
            `"${inc.actionable_intelligence?.assigned_police_unit || ''}"`
        ];
        csvRows.push(row.join(','));
    });

    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:T]/g, '_');
    link.setAttribute('href', url);
    link.setAttribute('download', `CYBER_DRISHTI_I4C_INTELLIGENCE_${timestamp}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showToast(`📥 Exported ${allIncidents.length} complaints to official I4C CSV`);
}

function setupEventListeners() {
    const filterPri = document.getElementById('filter-priority');
    const filterCat = document.getElementById('filter-category');
    const filterSrc = document.getElementById('filter-search');

    if (filterPri) filterPri.addEventListener('change', filterIncidents);
    if (filterCat) filterCat.addEventListener('change', filterIncidents);
    if (filterSrc) filterSrc.addEventListener('input', filterIncidents);
}
