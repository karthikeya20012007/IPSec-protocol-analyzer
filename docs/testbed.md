# IPsec Testbed

## Topology

The testbed uses Linux network namespaces to simulate a client, server, and two IPsec gateways.

```text
client namespace  (10.0.1.2)
       |
      veth
       |
gateway-a namespace (10.0.1.1 / 192.168.1.1)
       ||
       || IPsec / IKEv2 / ESP Tunnel
       ||
gateway-b namespace (192.168.1.2 / 10.0.2.1)
       |
      veth
       |
server namespace (10.0.2.2)
```

## IPsec Configuration

The initial phase uses a minimal working configuration:
* **Protocol:** IKEv2
* **Mode:** Tunnel
* **Encryption:** AES-256-GCM
* **Authentication:** Pre-Shared Key (PSK)
* **PFS:** Enabled
* **DH Group:** 14 (modp2048)
* **IP Version:** IPv4

Configurations are managed via `swanctl` and are located in `conf/gateway-a/` and `conf/gateway-b/`.

## Usage

* **Setup:** `sudo ./scripts/setup_testbed.sh`
* **Verify:** `sudo ./scripts/verify_testbed.sh`
* **Cleanup:** `sudo ./scripts/cleanup_testbed.sh`
