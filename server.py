@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if not data:
            return {"status": "error", "message": "No JSON data received"}, 400
        required_fields = ['timeframe', 'event', 'zone_id', 'price', 'bounce_pts', 'direction', 'parent_structure']
        if not all(field in data for field in required_fields):
            return {"status": "error", "message": "Missing required fields"}, 400
        timestamp = datetime.utcnow().isoformat() + 'Z'
        entry = {
            "timestamp": timestamp,
            "timeframe": data['timeframe'],
            "event": data['event'],
            "zone_id": data['zone_id'],
            "price": float(data['price']),
            "bounce_pts": int(data['bounce_pts']),
            "direction": data['direction'],
            "parent_structure": data['parent_structure'],
            "fib_bounces": {0.3: {"bounces": [], "max_bounce": 0},
                           0.5: {"bounces": [], "max_bounce": 0},
                           0.7: {"bounces": [], "max_bounce": 0}},
            "status": "active"
        }
        try:
            with open(DATA_FILE, 'r+') as f:
                zones = json.load(f)
                zone_exists = next((z for z in zones if z['zone_id'] == entry['zone_id']), None)
                if zone_exists:
                    # ... (existing logic)
                else:
                    zones.append(entry)
                f.seek(0)
                json.dump(zones, f, indent=2)
                print(f"Zone saved to {DATA_FILE}: {entry}")  # Debug
        except FileNotFoundError:
            with open(DATA_FILE, 'w') as f:
                json.dump([entry], f, indent=2)
                print(f"Zone created in {DATA_FILE}: {entry}")
        return {"status": "ok"}, 200
    except Exception as e:
        print(f"Webhook error: {str(e)}")  # Log the exception
        return {"status": "error", "message": str(e)}, 500
