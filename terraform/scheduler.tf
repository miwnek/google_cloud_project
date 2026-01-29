resource "google_cloud_scheduler_job" "check_urls_job" {
  name  = "check_urls_job"
  schedule = "*/5 * * * *"
  time_zone = "Europe/Warsaw"

  pubsub_target {
    topic_name = google_pubsub_topic.check_urls.id
    data = base64encode("{}")
  }
}