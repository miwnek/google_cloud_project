CHECK_URL_DIR=cloud_functions/check_url
SEND_ALERT_DIR=cloud_functions/send_alert

CHECK_URL_ZIP=terraform/check_url.zip
SEND_ALERT_ZIP=terraform/send_alert.zip

PROJECT_ID=original-mason-480715-v1
REGION=europe-central2

IMAGE=$(REGION)-docker.pkg.dev/$(PROJECT_ID)/uptime-api/uptime-api:latest

build-api:
	cd cloud_run_api && gcloud builds submit --tag $(IMAGE)

zip-check-url:
	@echo "Tworzenie archiwum ZIP dla check_url ..."
	cd $(CHECK_URL_DIR) && zip -r ../../$(CHECK_URL_ZIP) .

zip-send-alert:
	@echo "Tworzenie archiwum ZIP dla send_alert ..."
	cd $(SEND_ALERT_DIR) && zip -r ../../$(SEND_ALERT_ZIP) .

zip-all: zip-check-url zip-send-alert
	@echo "Tworzenie wszystkich archiwum ZIP ..."

clean:
	@echo "Usuwanie plików zip ..."
	rm terraform/*.zip