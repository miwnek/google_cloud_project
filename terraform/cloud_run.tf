resource "google_cloud_run_service" "uptime_api" {
  name = "uptime-api"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/uptime-api/uptime-api:latest"

        env {
          name = "PROJECT_ID"
          value = var.project_id
        }
      }
    }
  }

  traffic {
    percent = 100
    latest_revision = true
  }
}

// IAM API permissions
resource "google_cloud_run_service_iam_member" "public_access" {
  service = google_cloud_run_service.uptime_api.name
  location = var.region
  role = "roles/run.invoker"
  member = "allUsers"
}

// Pokazywanie adresu 
output "cloud_run_url" {
  value = google_cloud_run_service.uptime_api.status[0].url
}