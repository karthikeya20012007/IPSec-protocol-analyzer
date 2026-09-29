import re

with open('frontend/src/pages/Captures.tsx', 'r') as f:
    content = f.read()

if "useNavigate" not in content:
    content = content.replace("import React, { useEffect, useState, useRef } from 'react';", "import React, { useEffect, useState, useRef } from 'react';\nimport { useNavigate } from 'react-router-dom';")

content = content.replace("export const Captures: React.FC = () => {", "export const Captures: React.FC = () => {\n    const navigate = useNavigate();")

content = content.replace("setScenario(data);", "setScenario(data);\n            navigate('/app/overview');")

with open('frontend/src/pages/Captures.tsx', 'w') as f:
    f.write(content)
