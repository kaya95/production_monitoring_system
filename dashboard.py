from flask import Flask, render_template_string
from production_monitor import ProductionMonitor, services_to_monitor

app = Flask(__name__)
monitor = ProductionMonitor(services_to_monitor)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Production Monitor</title>
    <style>
        body { font-family: Arial; }
        .healthy { color: green; }
        .warning { color: orange; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Production Monitoring Dashboard</h1>
    <ul>
    {% for service in services %}
        <li class="{% if service.status == '🟢 HEALTHY' %}healthy{% else %}error{% endif %}">
            {{ service.url }} - {{ service.status }} - {{ service.response_time }}ms
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def dashboard():
    services_status = []
    for url in services_to_monitor:
        status = monitor.check_service_health(url)
        services_status.append({
            "url": url,
            "status": status["status"],
            "response_time": status.get("response_time", "N/A")
        })
    return render_template_string(TEMPLATE, services=services_status)

if __name__ == "__main__":
    app.run(port=5000)
