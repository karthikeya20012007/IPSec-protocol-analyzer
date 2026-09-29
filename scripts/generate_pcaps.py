import os
import subprocess
import time
from pathlib import Path

SCENARIOS = {
    "01-strong-gcm256": {
        "version": 2,
        "proposals": "aes256gcm16-prfsha256-modp2048",
        "esp_proposals": "aes256gcm16-modp2048",
        "mode": "tunnel",
        "traffic": "ping"
    },
    "02-weak-cbc128": {
        "version": 2,
        "proposals": "aes128-sha1-modp1024",
        "esp_proposals": "aes128-sha1-modp1024",
        "mode": "tunnel",
        "traffic": "ping"
    },
    "03-transport-gcm": {
        "version": 2,
        "proposals": "aes128gcm16-prfsha256-modp2048",
        "esp_proposals": "aes128gcm16",
        "mode": "transport",
        "traffic": "ping-direct"
    },
    "04-cbc256-dh4096": {
        "version": 2,
        "proposals": "aes256-sha256-modp4096",
        "esp_proposals": "aes256-sha256-modp4096",
        "mode": "tunnel",
        "traffic": "ping"
    },
    "05-no-pfs": {
        "version": 2,
        "proposals": "aes256gcm16-prfsha256-modp2048",
        "esp_proposals": "aes256gcm16",
        "mode": "tunnel",
        "traffic": "ping"
    },
    "06-weak-ikev1": {
        "version": 1,
        "proposals": "3des-md5-modp1024",
        "esp_proposals": "3des-md5",
        "mode": "tunnel",
        "traffic": "ping"
    }
}

CONF_DIR = Path("conf")
DATASET_DIR = Path("dataset/ipsec")
RAW_DIR = DATASET_DIR / "raw"
META_DIR = DATASET_DIR / "metadata"

def write_swanctl_conf(gw, scenario_id, config):
    local_ip = "192.168.1.1" if gw == "gateway-a" else "192.168.1.2"
    remote_ip = "192.168.1.2" if gw == "gateway-a" else "192.168.1.1"
    
    local_ts = "10.0.1.0/24" if gw == "gateway-a" else "10.0.2.0/24"
    remote_ts = "10.0.2.0/24" if gw == "gateway-a" else "10.0.1.0/24"
    
    if config["mode"] == "transport":
        local_ts = "dynamic"
        remote_ts = "dynamic"

    conf = f"""
connections {{
    gw-gw {{
        local_addrs  = {local_ip}
        remote_addrs = {remote_ip}
        version = {config['version']}
        proposals = {config['proposals']}

        local {{
            auth = psk
            id = {gw}
        }}
        remote {{
            auth = psk
            id = {"gateway-b" if gw == "gateway-a" else "gateway-a"}
        }}

        children {{
            net-net {{
                local_ts  = {local_ts}
                remote_ts = {remote_ts}
                esp_proposals = {config['esp_proposals']}
                mode = {config['mode']}
                start_action = trap
            }}
        }}
    }}
}}

secrets {{
    ike-psk {{
        id-a = gateway-a
        id-b = gateway-b
        secret = "super_secret_psk_123"
    }}
}}
"""
    with open(CONF_DIR / gw / "swanctl.conf", "w") as f:
        f.write(conf)

def run(cmd):
    print(f"[*] {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def generate_scenario(scenario_id, config):
    print(f"\n==============================================")
    print(f"Generating {scenario_id}...")
    print(f"==============================================")
    
    write_swanctl_conf("gateway-a", scenario_id, config)
    write_swanctl_conf("gateway-b", scenario_id, config)
    
    try:
        run("./scripts/setup_testbed.sh")
    except Exception as e:
        print(f"[!] Error setting up testbed for {scenario_id}: {e}")
        return False
    
    pcap_path = RAW_DIR / f"{scenario_id}.pcap"
    if pcap_path.exists():
        pcap_path.unlink()
    
    # Start tcpdump
    print(f"[*] Starting tcpdump...")
    tcpdump = subprocess.Popen(
        f"ip netns exec gateway-a tcpdump -i veth_a_b -w {pcap_path} -U",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True # Process group
    )
    
    time.sleep(2)
    
    # Generate traffic
    try:
        if config["traffic"] == "ping":
            run("ip netns exec client ping -c 10 -i 0.2 10.0.2.2")
        elif config["traffic"] == "ping-direct":
            run("ip netns exec gateway-a ping -c 10 -i 0.2 192.168.1.2")
    except subprocess.CalledProcessError:
        print(f"[!] Traffic generation failed for {scenario_id}!")
        
    time.sleep(2)
    
    print("[*] Stopping tcpdump...")
    # Send SIGINT to the process group
    try:
        os.killpg(os.getpgid(tcpdump.pid), 2) # SIGINT
    except Exception as e:
        print(f"[*] Failed to send SIGINT: {e}")
        
    subprocess.run("pkill -INT tcpdump", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    try:
        tcpdump.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("[*] tcpdump wait timed out. Force killing...")
        try:
            os.killpg(os.getpgid(tcpdump.pid), 9) # SIGKILL
        except Exception:
            pass
        subprocess.run("pkill -9 tcpdump", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        tcpdump.kill()
        tcpdump.wait(timeout=2)
        
    print("[*] tcpdump stopped.")
    
    # Clean up testbed to prevent charon instances leaking between scenarios
    print("[*] Cleaning up scenario testbed...")
    try:
        run("./scripts/cleanup_testbed.sh")
    except Exception as e:
        print(f"[!] Warning: cleanup script failed: {e}")
    
    # Validation
    if not pcap_path.exists():
        print(f"[!] Error: Capture file not found: {pcap_path}")
        return False
        
    size = pcap_path.stat().st_size
    if size == 0:
        print(f"[!] Error: Capture file is empty (0 bytes): {pcap_path}")
        return False
        
    print(f"[*] Capture written: {pcap_path}")
    print(f"[*] Capture size: {size} bytes")
    print(f"[*] Proceeding to next scenario...")
    return True

def main():
    if os.geteuid() != 0:
        print("Must run as root")
        return
        
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)
    
    success_list = []
    failed_list = []
    
    for sid, conf in SCENARIOS.items():
        success = False
        try:
            success = generate_scenario(sid, conf)
        except Exception as e:
            print(f"[!] Exception during generation of {sid}: {e}")
            
        if success:
            success_list.append(sid)
        else:
            failed_list.append(sid)
            
    print("\n==============================================")
    print("SUMMARY")
    print("==============================================")
    print("SUCCESS:")
    for s in success_list:
        print(f" - {s}.pcap")
    
    print("\nFAILED:")
    if not failed_list:
        print(" - None")
    else:
        for s in failed_list:
            print(f" - {s}")
            
    # Final safety cleanup
    run("./scripts/cleanup_testbed.sh")

if __name__ == "__main__":
    main()
