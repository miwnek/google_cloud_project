resource "google_cloudfunctions2_function" "check_url" {
  name = "check_url"
  location = var.region
  //runtime = "python312"

  build_config {
    entry_point = "main"
    runtime = "python312"
    source {
      storage_source {
        bucket = google_storage_bucket.functions_bucket.name
        object = google_storage_bucket_object.check_url_archive.name
      }
    }
  }

  service_config {
    max_instance_count = 3
  }

  event_trigger {
    event_type = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic = google_pubsub_topic.check_urls.id
    retry_policy = "RETRY_POLICY_RETRY"
  }
}

resource "google_cloudfunctions2_function" "send_alert" {
  name = "send_alert"
  location = var.region
  build_config {
    entry_point = "main"
    runtime = "python312"
    source {
      storage_source {
        bucket = google_storage_bucket.functions_bucket.name
        object = google_storage_bucket_object.send_alert.name
      }
    }
  }

  service_config {
    max_instance_count = 3
  }

  event_trigger {
    event_type = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic = google_pubsub_topic.availability_results.id
    retry_policy = "RETRY_POLICY_RETRY"
  }
}