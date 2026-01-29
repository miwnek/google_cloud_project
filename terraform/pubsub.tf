resource "google_pubsub_topic" "check_urls" {
  name = "check_urls"
}

resource "google_pubsub_topic" "availability_results" {
  name = "availability_results"
}