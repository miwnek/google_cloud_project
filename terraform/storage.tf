resource "google_storage_bucket" "functions_bucket" {
  name = "${var.project_id}-functions"
  location = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "check_url_archive" {
  name = "check_url.zip"
  bucket = google_storage_bucket.functions_bucket.name
  source = "${path.module}/check_url.zip"
}

resource "google_storage_bucket_object" "send_alert" {
  name = "send_alert.zip"
  bucket = google_storage_bucket.functions_bucket.name
  source = "${path.module}/send_alert.zip"
}