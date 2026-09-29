import re

with open('frontend/src/pages/IPsec.tsx', 'r') as f:
    content = f.read()

new_header = """            <div className="mb-6 border-b border-[#25282C] pb-5">
                <div className="text-[11px] uppercase tracking-widest text-[#666C75] font-medium mb-1">IPSEC</div>
                <h2 className="text-[26px] font-semibold text-[#E7E9EC] tracking-wide mb-1">IPsec Protocol Analysis</h2>
                <p className="text-[13px] text-[#969CA5]">Cryptographic context and state</p>
            </div>"""
content = re.sub(r'<h2 className="text-2xl font-medium text-white tracking-wide mb-6">IPsec Protocol Analysis</h2>', new_header, content)

with open('frontend/src/pages/IPsec.tsx', 'w') as f:
    f.write(content)
