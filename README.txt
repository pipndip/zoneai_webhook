ZoneAI Flask Webhook + Dashboard
===============================
1. Install dependencies:
    pip install -r requirements.txt

2. Deploy to Render:
    - Create a GitHub repo (e.g., ZoneAI-Webhook).
    - Upload these files.
    - Sign up at https://render.com, connect GitHub, and create a Web Service.
    - Set Build Command: pip install -r requirements.txt
    - Set Start Command: gunicorn --bind 0.0.0.0:${PORT} server:app
    - Deploy and note the URL (e.g., https://zoneai-webhook.onrender.com).

3. Configure TradingView Alerts:
    Use webhook URL: https://yourapp.onrender.com/webhook
    Example alert JSON:
    {
      "timeframe": "4h",
      "event": "fib_50_touch",
      "zone_id": "2025-07-17T08:12:00_41230_bullish",
      "price": 18225.75,
      "bounce_pts": 10,
      "direction": "bullish",
      "parent_structure": "bullish"
    }
    - Configure alerts for: "New Zone," "Fib 30 Touch," "Fib 50 Touch," "Fib 70 Touch," "Zone Re-entry," "Zone Invalidated" on 1m, 15m, 60m, 4hr charts.

4. Keep Active:
    - Set up UptimeRobot[](https://uptimerobot.com) to ping the URL every 5-10 minutes.
    - Check dashboard daily at the Render URL.