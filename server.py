from flask import Flask, request, jsonify
import json, os, time

app = Flask(__name__)

# Detect local vs Render
DATA_FILE = '/opt/render/project/src/zones.json' if os.getenv('RENDER') else 'zones.json'

# Ensure zones.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)

        # Check all required fields
        required = ["timeframe", "event", "zone_id", "price", "bounce_pts", "direction", "parent_structure"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Make zone_id unique with timestamp
        millis = int(time.time() * 1000)
        data['zone_id'] = f"{data['zone_id']}_{millis}"

        # Load zones
        with open(DATA_FILE, 'r') as f:
            zones = json.load(f)

        zones.append(data)

        # Save
        with open(DATA_FILE, 'w') as f:
            json.dump(zones, f, indent=2)

        print(f"[INFO] Zone saved: {data['zone_id']}")
        return jsonify({"status": "success", "zone_id": data['zone_id']}), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        print(f"[RAW DATA] {request.data.decode('utf-8')}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "webhook live"}), 200

if __name__ == '__main__':
    app.run(debug=True)
