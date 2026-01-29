import requests
import time
import os
import json
#from dotenv import load_dotenv
from google.cloud import firestore
from google.cloud import pubsub_v1

#load_dotenv()

#PROJECT_ID = os.getenv("PROJECT_ID")

#topic_path = publisher.topic_path(PROJECT_ID, "availability_results")
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
        except Exception:
            status = 0

        response_time = round((time.time() - start) * 1000, 2)

        result = {
            "url": url,
            "status": status,
            "response_time": response_time,
            "timestamp": time.time()
        }

        publisher.publish(topic_path, json.dumps(result).encode('utf-8'))