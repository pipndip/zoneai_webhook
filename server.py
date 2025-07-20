from flask import Flask, request, jsonify
import json, os, time
from google_sheets import append_to_sheet

app = Flask(__name__)
DATA_FILE = '/opt/render/project/src/zones.json' if os.getenv('RENDER') else 'zones.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if not data:
            raw_data = request.data.decode('utf-8').strip()
            if raw_data.startswith('Webhook: '):
                parts = raw_data.replace('Webhook: ', '').split('|')
                if len(parts) == 7:
                    data = {
                        'timeframe': parts[0],
                        'event': parts[1],
                        'zone_id': parts[2],
                        'price': float(parts[3]) if parts[3].replace('.', '').isdigit() else 0.0,
                        'bounce_pts': int(parts[4]) if parts[4].isdigit() else 0,
                        'direction': parts[5],
                        'parent_structure': parts[6]
                    }
                else:
                    return jsonify({"status": "error", "message": "Invalid Webhook format"}), 400
            else:
                return jsonify({"status": "error", "message": "No valid data received"}), 400

        required = ["timeframe", "event", "zone_id", "price", "bounce_pts", "direction", "parent_structure"]
        for field in required:
            if field not in data or not data[field]:
                return jsonify({"status": "error", "message": f"Missing or empty field: {field}"}), 400

        millis = int(time.time() * 1000)
        data['zone_id'] = f"{data['zone_id']}_{millis}" if not data['zone_id'].endswith(str(millis)) else data['zone_id']

        with open(DATA_FILE, 'r') as f:
            zones = json.load(f)
        zones.append(data)
        with open(DATA_FILE, 'w') as f:
            json.dump(zones, f, indent=2)

        print(f"[INFO] Zone saved: {data['zone_id']}")

        try:
            append_to_sheet(data)
            print(f"[INFO] Zone pushed to Google Sheet: {data['zone_id']}")
        except Exception as sheet_err:
            print(f"[WARNING] Failed to push to Google Sheet: {sheet_err}")

        return jsonify({"status": "success", "zone_id": data['zone_id']}), 200

    except ValueError as ve:
        print(f"[ERROR] Value error: {ve}")
        print(f"[RAW DATA] {request.data.decode('utf-8')}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        print(f"[ERROR] {e}")
        print(f"[RAW DATA] {request.data.decode('utf-8')}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "webhook live"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)