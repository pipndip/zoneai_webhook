from flask import Flask, request, render_template, Response
import json
import os
from datetime import datetime
import time

app = Flask(__name__)
DATA_FILE = 'zones.json'

def event_stream():
    while True:
        with open(DATA_FILE, 'r') as f:
            zones = json.load(f)
        # Group zones by timeframe for multi-timeframe display
        timeframe_zones = {tf: [z for z in zones if z.get('timeframe') == tf] for tf in ['1m', '15m', '60m', '4hr']}
        yield f"data: {json.dumps({'timeframes': timeframe_zones})}\n\n"
        time.sleep(1)

@app.route('/')
def home():
    with open(DATA_FILE, 'r') as f:
        zones = json.load(f)
    return render_template('dashboard.html', zones=zones)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        required_fields = {'timeframe', 'event', 'zone_id', 'price'}
        if not all(field in data for field in required_fields):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        timestamp = datetime.utcnow().isoformat() + 'Z'
        entry = {"timestamp": timestamp, **data}
        # Handle specific alert types
        with open(DATA_FILE, 'r+') as f:
            zones = json.load(f)
            zone_exists = next((z for z in zones if z['zone_id'] == entry['zone_id']), None)
            if zone_exists:
                if entry['event'] in ['fib30_touch', 'fib50_touch', 'fib70_touch']:
                    fib_level = float(entry['event'].replace('fib', '').replace('_touch', ''))
                    if 'fib_bounces' not in zone_exists:
                        zone_exists['fib_bounces'] = {0.3: {'bounces': [], 'max_bounce': 0},
                                                     0.5: {'bounces': [], 'max_bounce': 0},
                                                     0.7: {'bounces': [], 'max_bounce': 0}}
                    bounce_pts = entry.get('bounce_pts', 0)
                    zone_exists['fib_bounces'][fib_level]['bounces'].append(bounce_pts)
                    zone_exists['fib_bounces'][fib_level]['max_bounce'] = max(zone_exists['fib_bounces'][fib_level]['max_bounce'], bounce_pts)
                elif entry['event'] == 'zone_invalid':
                    zone_exists['status'] = 'invalid'
                elif entry['event'] == 'reentry':
                    zone_exists['last_reentry'] = timestamp
            else:
                entry['fib_bounces'] = {0.3: {'bounces': [], 'max_bounce': 0},
                                       0.5: {'bounces': [], 'max_bounce': 0},
                                       0.7: {'bounces': [], 'max_bounce': 0}}
                entry['status'] = 'active'
                zones.append(entry)
            f.seek(0)
            json.dump(zones, f, indent=2)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)