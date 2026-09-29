import re

with open('backend/data/scenarios.py', 'r') as f:
    content = f.read()

# I will replace each SecurityFinding block manually or with string replacement since there are only 9 of them.
# The user wants strongSwan diff configs. Let's make some standard diff configs.

f1_old = """        SecurityFinding(
            id="FIND-001", severity="MEDIUM", category="Integrity",
            title="Weak Integrity Algorithm (SHA-1)",
            description="The connection uses SHA-1 for integrity, which is deprecated due to collision attacks.",
            recommendation="Upgrade to SHA-256 or use an AEAD cipher like AES-GCM."
        ),"""
f1_new = """        SecurityFinding(
            id="FIND-001", severity="MEDIUM", category="Integrity",
            title="Weak Integrity Algorithm (SHA-1)",
            description="The connection uses SHA-1 for integrity, which is deprecated due to collision attacks.",
            recommendation="Upgrade to SHA-256 or use an AEAD cipher like AES-GCM.",
            status="OPEN",
            evidence=["IKE SA payload: SHA-1 detected", "IPsec SA payload: HMAC-SHA-1-96 detected"],
            assessment="SHA-1 is no longer considered secure against well-funded adversaries. While HMAC-SHA-1 retains some theoretical security margin, its use in modern IPsec deployments violates compliance frameworks like NIST SP 800-131A.",
            remediation_config=\"\"\"connections {
    vpn {
-       proposals = aes128-sha1-modp2048
+       proposals = aes256gcm16-prfsha256-ecp256
    }
}\"\"\",
            evidence_type="OBSERVED"
        ),"""
content = content.replace(f1_old, f1_new)

f2_old = """        SecurityFinding(
            id="FIND-002", severity="MEDIUM", category="Encryption",
            title="Insufficient Key Length (AES-128)",
            description="AES-128-CBC provides adequate security currently but does not meet CNSA 2.0 or post-quantum readiness requirements.",
            recommendation="Upgrade to AES-256-GCM for long-term data protection."
        )"""
f2_new = """        SecurityFinding(
            id="FIND-002", severity="MEDIUM", category="Encryption",
            title="Insufficient Key Length (AES-128)",
            description="AES-128-CBC provides adequate security currently but does not meet CNSA 2.0 or post-quantum readiness requirements.",
            recommendation="Upgrade to AES-256-GCM for long-term data protection.",
            status="OPEN",
            evidence=["IKE SA payload: AES-CBC-128 detected"],
            assessment="While AES-128 is not currently broken, organizations moving toward CNSA 2.0 and post-quantum cryptography standards require 256-bit symmetric keys to defend against Grover's algorithm.",
            remediation_config=\"\"\"connections {
    vpn {
-       proposals = aes128-sha256-modp2048
+       proposals = aes256gcm16-prfsha256-ecp256
    }
}\"\"\",
            evidence_type="OBSERVED"
        )"""
content = content.replace(f2_old, f2_new)

f3_old = """        SecurityFinding(
            id="FIND-003", severity="HIGH", category="Key Exchange",
            title="Perfect Forward Secrecy (PFS) Disabled",
            description="The CHILD SA was negotiated without PFS. If the IKE keys are compromised, all IPsec traffic can be decrypted.",
            recommendation="Enable PFS with a strong Diffie-Hellman group in the IPsec configuration."
        ),"""
f3_new = """        SecurityFinding(
            id="FIND-003", severity="HIGH", category="Key Exchange",
            title="Perfect Forward Secrecy (PFS) Disabled",
            description="The CHILD SA was negotiated without PFS. If the IKE keys are compromised, all IPsec traffic can be decrypted.",
            recommendation="Enable PFS with a strong Diffie-Hellman group in the IPsec configuration.",
            status="OPEN",
            evidence=["CREATE_CHILD_SA exchange lacks KE payload", "No ephemeral DH keys negotiated for IPsec SA"],
            assessment="Without Perfect Forward Secrecy (PFS), the IPsec session keys are derived entirely from the parent IKE SA. If an attacker records the encrypted traffic and later compromises the IKE credentials or IKE SA keys, they can decrypt all historical traffic retroactively.",
            remediation_config=\"\"\"connections {
    vpn {
        children {
            net {
-               esp_proposals = aes256gcm16
+               esp_proposals = aes256gcm16-ecp256
            }
        }
    }
}\"\"\",
            evidence_type="OBSERVED"
        ),"""
content = content.replace(f3_old, f3_new)

f4_old = """        SecurityFinding(
            id="FIND-004", severity="MEDIUM", category="Key Exchange",
            title="Session Key Reuse Risk",
            description="Without PFS, compromising one session key exposes all sessions using the same IKE SA keying material.",
            recommendation="Configure create-child-sa with a DH group to ensure independent keying per CHILD SA."
        )"""
f4_new = """        SecurityFinding(
            id="FIND-004", severity="MEDIUM", category="Key Exchange",
            title="Session Key Reuse Risk",
            description="Without PFS, compromising one session key exposes all sessions using the same IKE SA keying material.",
            recommendation="Configure create-child-sa with a DH group to ensure independent keying per CHILD SA.",
            status="OPEN",
            evidence=["CHILD SA key derivation relies solely on IKE keying material"],
            assessment="Disabling PFS fundamentally weakens the compartmentalization of IPsec tunnels. The cryptographic health of the entire tunnel depends on a single point of failure.",
            remediation_config=\"\"\"connections {
    vpn {
        children {
            net {
-               esp_proposals = aes256gcm16
+               esp_proposals = aes256gcm16-ecp256
            }
        }
    }
}\"\"\",
            evidence_type="DERIVED"
        )"""
content = content.replace(f4_old, f4_new)

f5_old = """        SecurityFinding(
            id="FIND-005", severity="HIGH", category="Protocol",
            title="Deprecated Protocol (IKEv1)",
            description="IKEv1 is obsolete and vulnerable to various attacks (e.g., Bleichenbacher, DoS).",
            recommendation="Migrate to IKEv2."
        ),"""
f5_new = """        SecurityFinding(
            id="FIND-005", severity="HIGH", category="Protocol",
            title="Deprecated Protocol (IKEv1)",
            description="IKEv1 is obsolete and vulnerable to various attacks (e.g., Bleichenbacher, DoS).",
            recommendation="Migrate to IKEv2.",
            status="OPEN",
            evidence=["ISAKMP Header Version: 1.0 (IKEv1)"],
            assessment="IKEv1 (RFC 2409) was officially deprecated by IETF in 2018 (RFC 8436). It lacks built-in DoS protection, has complex and rigid negotiation phases (Main Mode/Aggressive Mode), and is susceptible to offline dictionary attacks if Aggressive Mode is used.",
            remediation_config=\"\"\"connections {
    vpn {
-       version = 1
+       version = 2
    }
}\"\"\",
            evidence_type="OBSERVED"
        ),"""
content = content.replace(f5_old, f5_new)

f6_old = """        SecurityFinding(
            id="FIND-006", severity="CRITICAL", category="Encryption",
            title="Weak Encryption (3DES)",
            description="3DES is cryptographically weak with an effective key size of 112 bits and is vulnerable to SWEET32 birthday attacks.",
            recommendation="Upgrade to AES-128 or AES-256."
        ),"""
f6_new = """        SecurityFinding(
            id="FIND-006", severity="CRITICAL", category="Encryption",
            title="Weak Encryption (3DES)",
            description="3DES is cryptographically weak with an effective key size of 112 bits and is vulnerable to SWEET32 birthday attacks.",
            recommendation="Upgrade to AES-128 or AES-256.",
            status="OPEN",
            evidence=["SA Proposal: ENCR_3DES"],
            assessment="3DES operates on 64-bit blocks, making it highly vulnerable to birthday attacks (SWEET32). By capturing approximately 32 GB of traffic, an attacker can reliably produce collisions and recover plaintext secrets (like HTTP session cookies).",
            remediation_config=\"\"\"connections {
    vpn {
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha256-ecp256
    }
}\"\"\",
            evidence_type="OBSERVED"
        ),"""
content = content.replace(f6_old, f6_new)

f7_old = """        SecurityFinding(
            id="FIND-007", severity="CRITICAL", category="Integrity",
            title="Broken Hash Function (MD5)",
            description="MD5 is cryptographically broken and vulnerable to collision attacks. HMAC-MD5 provides reduced security margins.",
            recommendation="Upgrade to SHA-256 or better."
        ),"""
f7_new = """        SecurityFinding(
            id="FIND-007", severity="CRITICAL", category="Integrity",
            title="Broken Hash Function (MD5)",
            description="MD5 is cryptographically broken and vulnerable to collision attacks. HMAC-MD5 provides reduced security margins.",
            recommendation="Upgrade to SHA-256 or better.",
            status="OPEN",
            evidence=["SA Proposal: AUTH_HMAC_MD5_96"],
            assessment="MD5 is completely broken. While HMAC construction protects against some known collision attacks, the security margin is extremely low and use of MD5 is prohibited by all modern compliance and security standards.",
            remediation_config=\"\"\"connections {
    vpn {
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha256-ecp256
    }
}\"\"\",
            evidence_type="OBSERVED"
        ),"""
content = content.replace(f7_old, f7_new)

f8_old = """        SecurityFinding(
            id="FIND-008", severity="HIGH", category="Key Exchange",
            title="Perfect Forward Secrecy (PFS) Disabled",
            description="The CHILD SA was negotiated without PFS, leaving all sessions vulnerable if the IKE SA key is compromised.",
            recommendation="Enable PFS with a strong Diffie-Hellman group."
        ),"""
f8_new = """        SecurityFinding(
            id="FIND-008", severity="HIGH", category="Key Exchange",
            title="Perfect Forward Secrecy (PFS) Disabled",
            description="The CHILD SA was negotiated without PFS, leaving all sessions vulnerable if the IKE SA key is compromised.",
            recommendation="Enable PFS with a strong Diffie-Hellman group.",
            status="OPEN",
            evidence=["Quick Mode exchange lacks KE payload"],
            assessment="Without Perfect Forward Secrecy (PFS), the IPsec session keys are derived entirely from the parent IKE SA. If an attacker records the encrypted traffic and later compromises the IKE credentials, they can decrypt all historical traffic.",
            remediation_config=\"\"\"connections {
    vpn {
        children {
            net {
-               esp_proposals = 3des-md5
+               esp_proposals = aes256gcm16-ecp256
            }
        }
    }
}\"\"\",
            evidence_type="OBSERVED"
        ),"""
content = content.replace(f8_old, f8_new)

f9_old = """        SecurityFinding(
            id="FIND-009", severity="HIGH", category="Key Exchange",
            title="Weak DH Group (modp1024)",
            description="DH group 2 (1024-bit MODP) is considered insufficient. NIST deprecated 1024-bit groups.",
            recommendation="Use DH group 14 (2048-bit) or stronger."
        )"""
f9_new = """        SecurityFinding(
            id="FIND-009", severity="HIGH", category="Key Exchange",
            title="Weak DH Group (modp1024)",
            description="DH group 2 (1024-bit MODP) is considered insufficient. NIST deprecated 1024-bit groups.",
            recommendation="Use DH group 14 (2048-bit) or stronger.",
            status="OPEN",
            evidence=["SA Proposal: DH Group 2 (1024-bit MODP)"],
            assessment="1024-bit Diffie-Hellman groups are vulnerable to nation-state level adversaries via the Logjam attack and general discrete logarithm precomputations. Modern infrastructure requires minimum 2048-bit MODP or Elliptic Curve groups.",
            remediation_config=\"\"\"connections {
    vpn {
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha256-ecp256
    }
}\"\"\",
            evidence_type="OBSERVED"
        )"""
content = content.replace(f9_old, f9_new)

with open('backend/data/scenarios.py', 'w') as f:
    f.write(content)

