import re

with open('frontend/src/index.css', 'r') as f:
    content = f.read()

content = content.replace("--color-soc-dark: #070809;", "--color-soc-dark: #0B0C0D;")
content = content.replace("--color-soc-panel: #101214;", "--color-soc-panel: #111315;")
content = content.replace("--color-soc-border: #1e2025;", "--color-soc-border: #25282C;")
content = content.replace("--color-soc-text: #a1a1aa;", "--color-soc-text: #969CA5;")
content = content.replace("--color-soc-text-hover: #f4f4f5;", "--color-soc-text-hover: #E7E9EC;")

with open('frontend/src/index.css', 'w') as f:
    f.write(content)
