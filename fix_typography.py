import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    content = re.sub(r'text-\[8px\]', 'text-xs', content)
    content = re.sub(r'text-\[9px\]', 'text-xs', content)
    content = re.sub(r'text-\[10px\]', 'text-xs', content)
    content = re.sub(r'text-\[11px\]', 'text-xs', content)
    content = re.sub(r'text-\[12px\]', 'text-xs', content)
    content = re.sub(r'text-\[13px\]', 'text-sm', content)
    content = re.sub(r'text-\[14px\]', 'text-sm', content)
    content = re.sub(r'text-\[15px\]', 'text-base', content)
    content = re.sub(r'text-\[18px\]', 'text-lg', content)
    content = re.sub(r'text-\[24px\]', 'text-2xl', content)
    content = re.sub(r'text-\[26px\]', 'text-2xl', content)
    content = re.sub(r'text-\[32px\]', 'text-3xl', content)

    # In Tailwind, text-xs is 12px, text-sm is 14px, text-base is 16px.

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            process_file(os.path.join(root, file))

print("Done")
