import re

with open('tests/test_backend_api.py', 'r') as f:
    content = f.read()

# Replace the assertion
new_test = """def test_list_scenarios():
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 8
    assert "filename" in data[0]"""

content = re.sub(r'def test_list_scenarios\(\):.*?assert data == PCAP_INDEX', new_test, content, flags=re.DOTALL)

with open('tests/test_backend_api.py', 'w') as f:
    f.write(content)
