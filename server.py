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
        # Append a unique suffix to zone_id if it exists
        base_zone_id = data['zone_id']
        entry = {
            "timestamp": timestamp,
            "timeframe": data['timeframe'],
            "event": data['event'],
            "zone_id": f"{base_zone_id}_{int(time.time() * 1000)}",  # Unique with millisecond timestamp
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
                zones.append(entry)  # Always append new entry
                f.seek(0)
                json.dump(zones, f, indent=2)
                print(f"Zone saved to {DATA_FILE}: {entry}")
        except FileNotFoundError:
            with open(DATA_FILE, 'w') as f:
                json.dump([entry], f, indent=2)
                print(f"Zone created in {DATA_FILE}: {entry}")
        return {"status": "ok"}, 200
    except Exception as e:
        print(f"Webhook error: {str(e)}")
<<<<<<< HEAD
        return {"status": "error", "message": str(e)}, 500
=======
        return {"status": "error", "message": str(e)}, 500
>>>>>>> bf3af3dce2f713510b4dc49382fea3eb7822321f
