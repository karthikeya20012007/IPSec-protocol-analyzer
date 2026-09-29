# IPSec Protocol Analyzer — Demo MVP

## Project Objective

Build a polished demonstration MVP of an AI-driven IPsec VPN protocol analysis platform.

The current submission prioritizes:
- Working software prototype
- Strong frontend/dashboard UX
- AI traffic classification presentation
- IPsec security analysis presentation
- Security findings and risk assessment
- Report generation
- Reliable demonstration flow

This is a demo MVP. Do not attempt to turn it into the complete production system during this sprint.

---

## Current MVP Scope

The MVP supports:

1. PCAP/PCAPNG file upload
2. Predefined demo captures
3. Filename-based scenario lookup
4. Precomputed/mock analysis results
5. IPsec protocol/security information
6. Encrypted traffic classification
7. Security findings
8. Risk score
9. Interactive dashboard
10. Reports

The backend should remain behind a realistic service/API boundary so that the mock analysis layer can later be replaced by real PCAP parsing and ML inference.

### Explicitly out of scope for this MVP

Do NOT implement:

- Live packet capture
- Arbitrary PCAP parsing
- Real-time traffic monitoring
- Real ML inference
- Model training
- Database
- Redis
- Kubernetes
- Cloud deployment
- Production authentication
- Complex infrastructure
- Unnecessary backend redesign

---

## Existing Project

This is an existing repository.

Before changing code:

- Inspect the existing frontend.
- Inspect the existing backend.
- Inspect existing routes.
- Inspect existing components.
- Inspect existing styling.
- Inspect existing APIs.
- Inspect existing IPsec-related code.
- Inspect existing mock/sample data.
- Inspect package/dependency configuration.
- Inspect build/test commands.

Preserve useful existing functionality.

Do not rewrite working functionality unnecessarily.

---

## Git

Work only on the `demo` branch.

Do not modify or merge into `main`.

Make small, logical commits.

Before destructive changes, inspect the existing implementation and preserve anything reusable.

---

## Demo Scenarios

The demo contains these predefined captures:

| ID | Filename | Scenario |
|---|---|---|
| S01 | 01-strong-gcm256.pcap | Strong IKEv2 / AES-256-GCM |
| S02 | 02-weak-cbc128.pcap | AES-128-CBC / SHA-1 |
| S03 | 03-transport-gcm.pcap | Transport mode / GCM |
| S04 | 04-cbc256-dh4096.pcap | AES-256-CBC / DH-4096 |
| S05 | 05-no-pfs.pcap | AES-256-GCM / No PFS |
| S06 | 06-weak-ikev1.pcap | IKEv1 / 3DES / MD5 |
| S07 | 07-ipv6-tunnel.pcap | IPv6 / Tunnel / CNSA 2.0 |
| S08 | 08-cert-auth.pcap | X.509 certificate authentication |

---

## Mock Data Architecture

Use a single source of truth for each scenario.

Preferred lookup flow:

uploaded filename
    ↓
PCAP_INDEX
    ↓
scenario_id
    ↓
SCENARIO_RESULTS[scenario_id]
    ↓
IPsec + traffic + findings + reports
    ↓
all UI pages

Example:

PCAP_INDEX = {
    "01-strong-gcm256.pcap": "S01",
    "02-weak-cbc128.pcap": "S02",
    "03-transport-gcm.pcap": "S03",
    "04-cbc256-dh4096.pcap": "S04",
    "05-no-pfs.pcap": "S05",
    "06-weak-ikev1.pcap": "S06",
    "07-ipv6-tunnel.pcap": "S07",
    "08-cert-auth.pcap": "S08"
}

Do not scatter scenario-specific values throughout React components.

If a scenario has a score of 42, every page must obtain that score from the same scenario object.

If a scenario uses IKEv1, every relevant page must obtain IKEv1 from the same source.

If a scenario contains MD5 or 3DES, the corresponding security findings must come from the same scenario data.

---

## Scenario Data

Each scenario should be capable of containing:

- id
- filename
- capture metadata
- packet count
- duration
- flow count
- bytes
- IP version
- IPsec protocol
- IKE version
- encryption
- integrity
- DH group
- PFS
- authentication
- mode
- traffic selectors
- security score
- risk level
- traffic classification
- classification confidence
- flows
- findings
- protocol composition
- timeline data
- report metadata

---

## Traffic Classification

The AI traffic classifier represents encrypted-traffic classification from observable flow behavior.

Potential application classes:

- Web
- Video Streaming
- VoIP / Audio
- Chat
- File Transfer
- DNS
- Bulk TCP
- Unknown

Use `DERIVED` for inferred/AI classification.

Use `OBSERVED` for deterministic protocol/capture evidence.

Do not claim that encrypted payloads were decrypted.

---

## UI Structure

Use separate pages rather than one extremely long analysis page.

Sidebar:

- Overview
- Captures
- Traffic
- IPsec
- Security
- Reports

Secondary navigation:

- Testbed
- Settings

### Captures

Include:

- PCAP/PCAPNG upload
- Demo capture selection
- Upload/loading state
- Selected capture
- Analysis initiation
- Reliable demo-mode scenario selection

### Overview

Show the most important information without excessive scrolling:

- Security/risk score
- Risk level
- Packets analyzed
- Flows analyzed
- IPsec coverage
- AI confidence
- Traffic distribution
- Major findings
- Executive summary

### Traffic

Show:

- Encrypted traffic classification
- Application distribution
- Classification confidence
- Flow table
- Flow details drawer

Flow details may include:

- Duration
- Packets
- Throughput
- Average packet size
- IAT
- Classification
- Classification signals

### IPsec

Show:

- IKE version
- Encryption
- Integrity
- DH group
- PFS
- Authentication
- Mode
- IPv4/IPv6
- Traffic selectors
- Security associations
- Protocol composition
- Handshake timeline

### Security

Show:

- Security score
- Risk level
- Severity counts
- Threat categories
- Findings
- Evidence
- Recommendations

Evidence should be expandable where appropriate.

### Reports

Show:

- Executive report
- Technical report
- Report preview
- Generate/download report

Reports must use the same scenario data displayed by the dashboard.

---

## Persistent Analysis Header

When a capture is selected, maintain a compact context header such as:

06-weak-ikev1.pcap

HIGH RISK    42/100    IKEv1    3DES    MD5    IPv4

Do not duplicate information unnecessarily.

---

## Demo Mode

Provide reliable demo scenario selection.

Recommended demo buttons:

- Strong IKEv2
- Weak IKEv1
- Transport
- No PFS
- IPv6
- Certificate

Demo mode must work even if an actual PCAP file is unavailable.

---

## Visual Design

Use a polished dark enterprise/SOC cybersecurity interface.

Design characteristics:

- Dark background
- Restrained blue accent
- Strong typography
- Subtle borders
- Compact status badges
- Clear information hierarchy
- Dense but readable technical information
- Professional enterprise/SOC appearance

Avoid:

- Excessive neon
- Hacker clichés
- Unnecessary animations
- Excessive gradients
- Visual clutter
- Huge decorative elements
- One giant scrolling dashboard

The UI should feel like a serious security analysis platform.

---

## Technical Architecture

Preferred conceptual flow:

PCAP / PCAPNG
    ↓
FastAPI Backend
    ↓
Scenario Lookup / Mock Analysis Engine
    ↓
IPsec Analyzer
    ↓
AI Traffic Classifier
    ↓
Security Rules Engine
    ↓
Risk / Findings
    ↓
React Dashboard
    ↓
Report Generator

For the MVP, these analysis components may use precomputed structured data.

Keep their interfaces separated so real implementations can replace them later.

---

## Frontend Rules

Do not hardcode scenario-specific analysis values directly inside page components.

Components should consume structured scenario data.

Prefer:

data → service/state → page → reusable component

rather than:

page component → hardcoded values

Create reusable components for:

- Metric cards
- Status badges
- Risk indicators
- Finding cards
- Charts
- Tables
- Detail drawers
- Protocol information
- Empty/loading states

---

## Backend Rules

Keep the backend simple.

Use FastAPI if the existing project already uses it.

Expose a clean API boundary for:

- capture upload
- scenario selection
- analysis result
- traffic data
- IPsec data
- findings
- reports

Do not introduce a database for the MVP unless the existing project already requires one.

---

## Data Integrity

The same scenario object must drive:

- Overview
- Traffic
- IPsec
- Security
- Reports

Never create contradictory values between pages.

For example:

If S06 contains:

IKEv1
3DES
MD5
No PFS
Score 42

then all relevant UI sections and reports must reflect those values.

---

## Implementation Order

Follow this order:

1. Inspect existing repository
2. Present implementation plan
3. Wait for approval
4. Create/organize mock data
5. Implement capture/demo selection
6. Implement shared analysis state/API
7. Implement Overview
8. Implement Traffic
9. Implement IPsec
10. Implement Security
11. Implement Reports
12. Refine visual design
13. Verify all demo scenarios
14. Run build/tests
15. Verify the application in the browser

Do not skip repository inspection.

---

## Verification

Before considering the MVP complete:

- Verify `demo` branch
- Run existing tests
- Run frontend build
- Run backend checks
- Verify upload flow
- Verify every demo scenario
- Verify navigation
- Verify no contradictory values between pages
- Verify reports use selected scenario data
- Check browser console for errors
- Check responsive layout where practical

---

## Important Rule

Do not implement large changes before presenting a plan.

First inspect the repository and explain:

1. What already exists
2. What can be reused
3. What needs to be added
4. What should remain untouched
5. Proposed implementation sequence

Then wait for approval.
