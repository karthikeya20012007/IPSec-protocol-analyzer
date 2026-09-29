import json
import subprocess
import hashlib
from pathlib import Path
import sys

DATASET_DIR = Path("dataset/ipsec")
RAW_DIR = DATASET_DIR / "raw"
META_DIR = DATASET_DIR / "metadata"

def get_pcap_info(pcap_path):
    # Use tshark to extract packet count, duration, ip versions, Ike/ESP presence
    try:
        # Check if file exists and is valid
        if not pcap_path.exists() or pcap_path.stat().st_size == 0:
            return {"error": "File does not exist or is empty"}

        # Use capinfos for basic stats
        capinfos_out = subprocess.check_output(f"capinfos -Tm {pcap_path}", shell=True, text=True)
        # capinfos -Tm outputs comma separated values
        lines = capinfos_out.strip().split("\n")
        if len(lines) < 2:
            return {"error": "capinfos failed to parse"}
            
        headers = lines[0].split(',')
        values = lines[1].split(',')
        stats = dict(zip(headers, values))
        
        packet_count = int(stats.get("Number of packets", 0))
        duration = float(stats.get("Capture duration", 0))
        
        if packet_count == 0:
            return {"error": "0 packets"}
            
        # Use tshark to detect protocols
        tshark_out = subprocess.check_output(
            f"tshark -r {pcap_path} -T fields -e ip.version -e ipv6.version -e isakmp.version -e esp.spi -e udp.port",
            shell=True, text=True
        )
        
        ipv4 = "4" in tshark_out
        ipv6 = "6" in tshark_out
        ike = "1.0" in tshark_out or "2.0" in tshark_out
        ike_v1 = "1.0" in tshark_out
        ike_v2 = "2.0" in tshark_out
        esp = "esp" in tshark_out.lower() or tshark_out.count("\t\t") > 0  # weak check, but spi exists if ESP
        
        # Better ESP check
        esp_check = subprocess.check_output(f"tshark -r {pcap_path} -Y esp -c 1 2>/dev/null", shell=True, text=True)
        esp = len(esp_check.strip()) > 0

        # SHA-256
        sha256 = hashlib.sha256(pcap_path.read_bytes()).hexdigest()
        
        return {
            "filename": pcap_path.name,
            "sha256": sha256,
            "source": "strongswan_testbed",
            "capture_type": "IPsec",
            "packet_count": packet_count,
            "duration_seconds": round(duration, 2),
            "ip_version": "IPv6" if ipv6 else "IPv4",
            "ike_detected": ike,
            "ike_version": "IKEv1" if ike_v1 else ("IKEv2" if ike_v2 else "Unknown"),
            "esp_detected": esp,
            "validation_status": "PASS"
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    if not RAW_DIR.exists():
        print("Raw directory not found.")
        sys.exit(1)
        
    pcaps = list(RAW_DIR.glob("*.pcap"))
    if not pcaps:
        print("No PCAPs found.")
        sys.exit(1)
        
    registry = []
    
    print(f"{'Filename':<25} {'Packets':<10} {'Duration':<10} {'IKE':<10} {'ESP':<5} {'Status'}")
    print("-" * 75)
    
    all_pass = True
    
    for pcap in sorted(pcaps):
        info = get_pcap_info(pcap)
        if "error" in info:
            print(f"{pcap.name:<25} ERROR: {info['error']}")
            all_pass = False
        else:
            print(f"{info['filename']:<25} {info['packet_count']:<10} {info['duration_seconds']:<10.2f} {info['ike_version']:<10} {str(info['esp_detected']):<5} {info['validation_status']}")
            
            # Additional configuration_profile matching
            config_profile = info["filename"].replace(".pcap", "")
            
            # Simple mode heuristic (we know from generation)
            mode = "Transport" if "transport" in info["filename"] else "Tunnel"
            
            info["mode"] = mode
            info["configuration_profile"] = config_profile
            
            registry.append(info)
            
    if all_pass:
        print("\nAll PCAPs validated successfully.")
        META_DIR.mkdir(parents=True, exist_ok=True)
        with open(META_DIR / "captures.json", "w") as f:
            json.dump(registry, f, indent=2)
        print(f"Registry written to {META_DIR / 'captures.json'}")
    else:
        print("\nValidation failed for some PCAPs. Registry not updated.")
        sys.exit(1)

if __name__ == "__main__":
    main()
