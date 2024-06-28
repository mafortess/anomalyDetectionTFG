import logging
from flask import Flask, request, jsonify
from telegram import Bot, ParseMode

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot with your token
TELEGRAM_TOKEN = '<TOKEN>'
TELEGRAM_CHAT_ID = '<CHAT ID>'
bot = Bot(token=TELEGRAM_TOKEN)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    if 'alerts' in data:
        for alert in data['alerts']:
            send_alert_to_telegram(alert)
        return jsonify({'status': 'success'}), 200
    return jsonify({'error': 'No alerts found'}), 400
    
def send_alert_to_telegram(alert):
    try:
        message = format_message(alert)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)
        logger.info("Message sent to Telegram")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

def format_message(alert):
    status = alert.get('status', 'unknown')
    summary = alert.get('labels', {}).get('alertname', 'No alert name')
    description = alert.get('annotations', {}).get('description', 'No description provided')
    return f"*Status:* {status}\n*Alert:* {summary}\n*Description:* {description}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
