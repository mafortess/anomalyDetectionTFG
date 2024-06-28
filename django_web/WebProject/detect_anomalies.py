import os
import django
import logging
from django.conf import settings
from ai.views import collect_data, detect_anomalies, get_monitoring_state

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebProject.settings')
django.setup()

# Configurar logging
logging.basicConfig(
    filename=os.path.join(settings.BASE_DIR, 'cron_tasks.log'),
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        if get_monitoring_state():
            logger.info("Starting data collection and anomaly detection task...")
            collect_data()
            detect_anomalies(None)
            logger.info("Data collection and anomaly detection task completed successfully.")
        else:
            logger.info("Real-time monitoring is disabled.")
    except Exception as e:
        logger.error(f"Error during data collection and anomaly detection task: {e}")

if __name__ == "__main__":
    main()
