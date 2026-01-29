import requests
import time
import os
import json
import logging
from google.cloud import logging as cloud_logging
from google.cloud import firestore
from google.cloud import pubsub_v1

client = cloud_logging.Client()
client.setup_logging()

logger = logging.getLogger("availability_checker")
logging.basicConfig(level=logging.INFO)

db = firestore.Client(database="urlsdb")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("original-mason-480715-v1", "availability_results")

def main(event, context):

    urls_ref = db.collection("urls")
    docs = urls_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        url = data["url"]

        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            success = 200 <= status < 300
        except Exception as e:
            status = 0
            success = False
            logger.error({
                "event": "url_check",
                "url": url,
                "status": status,
                "error": str(e),
            })

        response_time = round((time.time() - start) * 1000, 2)

        logger.info({
            "event": "url_check",
            "url": url,
            "status": status,
            "is_success": success,
            "response_time_ms": response_time
        })

        result = {
            "url": url,
            "status": status,
            "response_time": response_time,
            "timestamp": time.time()
        }

        publisher.publish(topic_path, json.dumps(result).encode('utf-8'))