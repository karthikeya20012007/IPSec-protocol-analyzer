import re

with open('frontend/src/api/client.ts', 'r') as f:
    content = f.read()

content = content.replace("import type { ScenarioAnalysis }", "import type { ScenarioAnalysis, CaptureMetadata }")
content = content.replace("Promise<Record<string, string>>", "Promise<CaptureMetadata[]>")

with open('frontend/src/api/client.ts', 'w') as f:
    f.write(content)
