import hashlib
from pathlib import Path
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from backend.models import ScenarioAnalysis, CaptureMetadata
from backend.data.scenarios import SCENARIO_RESULTS

# Dynamic Capture Registry
CAPTURE_REGISTRY = {}
DATASET_RAW = Path("dataset/ipsec/raw")

def calculate_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def build_registry():
    files = {
        "01-strong-gcm256.pcap": "S01",
        "02-weak-cbc128.pcap": "S02",
        "03-transport-gcm.pcap": "S03",
        "04-cbc256-dh4096.pcap": "S04",
        "05-no-pfs.pcap": "S05",
        "06-weak-ikev1.pcap": "S06",
        "ikev2_s2s_ipsec_vpn_aes_gcm.pcapng": "EX01"
    }
    
    registry = {}
    
    if DATASET_RAW.exists():
        for filename, scenario_id in files.items():
            path = DATASET_RAW / filename
            if path.exists():
                sha256 = calculate_sha256(path)
                
                if scenario_id == "EX01":
                    source = "wireshark-sample-capture"
                    ctype = "external-validation"
                else:
                    source = "strongswan-testbed"
                    ctype = "controlled"
                    
                meta = SCENARIO_RESULTS.get(scenario_id)
                pkts = meta.packet_count if meta else None
                dur = meta.duration_sec if meta else None
                
                registry[sha256] = {
                    "scenario_id": scenario_id,
                    "filename": filename,
                    "sha256": sha256,
                    "source": source,
                    "capture_type": ctype,
                    "packet_count": pkts,
                    "duration_seconds": dur
                }
    return registry

CAPTURE_REGISTRY = build_registry()

app = FastAPI(title="IPSec Protocol Analyzer API", version="0.1.0")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scenarios", response_model=List[CaptureMetadata])
def list_scenarios():
    """
    Returns the metadata for all available predefined captures.
    """
    return [scenario.capture for scenario in SCENARIO_RESULTS.values()]

@app.get("/api/analyze/{scenario_id}", response_model=ScenarioAnalysis)
def get_scenario_analysis(scenario_id: str):
    """
    Returns the full structured analysis data for a given scenario ID.
    """
    scenario_id = scenario_id.upper()
    if scenario_id not in SCENARIO_RESULTS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return SCENARIO_RESULTS[scenario_id]

@app.post("/api/upload", response_model=ScenarioAnalysis)
async def upload_pcap(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
        
    contents = await file.read()
    h = hashlib.sha256()
    h.update(contents)
    file_hash = h.hexdigest()
    
    registry_entry = CAPTURE_REGISTRY.get(file_hash)
    if not registry_entry:
        raise HTTPException(
            status_code=400, 
            detail="The uploaded PCAP is not part of the validated capture library. Please upload a known sample."
        )
        
    scenario_id = registry_entry["scenario_id"]
    return SCENARIO_RESULTS[scenario_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
