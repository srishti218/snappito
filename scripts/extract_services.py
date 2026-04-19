import sys

html_path = "/Users/apple/Varun/snappito/frontend/service-detail.html"
with open(html_path, "r") as f:
    html = f.read()

start_marker = "const SERVICES = ["
end_marker = "];"
start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    services_code = html[start_idx:end_idx]
    # Convert to export
    services_code = "export " + services_code
    with open("/Users/apple/Varun/snappito/src/features/catalog/data/serviceData.js", "w") as out:
        out.write(services_code)
    print("Extracted SERVICES to src/features/catalog/data/serviceData.js")
else:
    print("Could not find SERVICES array")
