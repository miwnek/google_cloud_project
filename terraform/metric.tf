resource "google_logging_metric" "url_check_response_time" {
    name = "url_check_response_time_ms"
    description = "Response time for URL availability checks"

    filter = <<EOF
resource.type="cloud_run_revision"
jsonPayload.event="url_check"
jsonPayload.response_time_ms>=0
EOF

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "DISTRIBUTION"
    unit        = "ms"
  }

  value_extractor = "EXTRACT(jsonPayload.response_time_ms)"

  bucket_options {
    exponential_buckets {
      num_finite_buckets = 20
      growth_factor = 2
      scale = 10
    }
  }
}

resource "google_logging_metric" "url_check_by_success" {
  name        = "url_check_by_success"
  description = "Count of URL checks grouped by success"

  filter = <<EOF
resource.type="cloud_run_revision"
jsonPayload.event="url_check"
jsonPayload.is_success=true OR jsonPayload.is_success=false
EOF

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"

    labels {
        key = "success"
        value_type = "BOOL"
        description = "Whether the URL check succeeded"
    }
  }


  label_extractors = {
    success = "EXTRACT(jsonPayload.is_success)"
  }
}

resource "google_logging_metric" "url_check_by_status" {
  name        = "url_check_by_status"
  description = "Count of URL checks grouped by HTTP status"

  filter = <<EOF
resource.type="cloud_run_revision"
jsonPayload.event="url_check"
jsonPayload.status>=0
EOF

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"

    labels {
      key         = "status"
      value_type  = "INT64"
      description = "HTTP status code"
    }
  }


  label_extractors = {
    status = "EXTRACT(jsonPayload.status)"
  }
}
