import re

with open('frontend/src/components/charts/Charts.tsx', 'r') as f:
    content = f.read()

# We want to replace the YAxis in TrafficActivityAreaChart
# The YAxis currently looks like:
#             <YAxis
#                 stroke="#71717a"
#                 fontSize={10}
#                 tickLine={false}
#                 axisLine={false}
#                 tickFormatter={(value) => `${(value / 1024).toFixed(0)} KB`}
#             />

new_yaxis = """            <YAxis
                stroke="#71717a"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                domain={[0, 4096000]}
                ticks={[0, 1024000, 2048000, 3072000, 4096000]}
                tickFormatter={(value) => `${(value / 1024).toFixed(0)} KB`}
            />"""

# Using regex to find the specific YAxis under TrafficActivityAreaChart
# Since there are multiple YAxis, we can use a more specific regex or just string replacement if unique.
# Actually it is the only YAxis that has tickFormatter=(value) => `${(value / 1024).toFixed(0)} KB`

content = re.sub(
    r'<YAxis\s+stroke="#71717a"\s+fontSize=\{10\}\s+tickLine=\{false\}\s+axisLine=\{false\}\s+tickFormatter=\{\(value\) => `\$\{\(value / 1024\)\.toFixed\(0\)\} KB`\}\s+/>',
    new_yaxis,
    content,
    flags=re.MULTILINE
)

with open('frontend/src/components/charts/Charts.tsx', 'w') as f:
    f.write(content)

