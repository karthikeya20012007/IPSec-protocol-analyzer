import re

# 1. Update backend/models.py
with open('backend/models.py', 'r') as f:
    content = f.read()

new_finding_model = """class SecurityFinding(BaseModel):
    id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str
    title: str
    description: str
    recommendation: str
    status: str = "OPEN"
    evidence: list[str] = []
    assessment: str = ""
    remediation_config: str = ""
    evidence_type: str = "OBSERVED\""""

content = re.sub(r'class SecurityFinding\(BaseModel\):\n    id: str\n    severity: str.*?recommendation: str', new_finding_model, content, flags=re.DOTALL)

with open('backend/models.py', 'w') as f:
    f.write(content)

# 2. Update frontend/src/types/index.ts
with open('frontend/src/types/index.ts', 'r') as f:
    content = f.read()

new_ts_finding = """export interface SecurityFinding {
    id: string;
    severity: string;
    category: string;
    title: string;
    description: string;
    recommendation: string;
    status: string;
    evidence: string[];
    assessment: string;
    remediation_config: string;
    evidence_type: string;
}"""

content = re.sub(r'export interface SecurityFinding \{\n    id: string;\n    severity: string;\n    category: string;\n    title: string;\n    description: string;\n    recommendation: string;\n\}', new_ts_finding, content, flags=re.DOTALL)

with open('frontend/src/types/index.ts', 'w') as f:
    f.write(content)

