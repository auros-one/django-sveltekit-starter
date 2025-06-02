resource "hcloud_firewall" "app_firewall" {
  name = "${var.project_name}-firewall"

  # SSH
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "22"
    source_ips = [
      "0.0.0.0/0",
    ]
  }

  # HTTPS
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "443"
    source_ips = [
      "0.0.0.0/0",
    ]
  }

  # PostgreSQL
  rule {
    description = "Allow PostgreSQL access"
    direction   = "in"
    protocol    = "tcp"
    port        = "5432"
    source_ips  = [
      "0.0.0.0/0",
    ]
  }

  apply_to {
    server = hcloud_server.app_server.id
  }
}
