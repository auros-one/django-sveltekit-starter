# Network for internal communication between Dokku apps
resource "hcloud_network" "project_network" {
  name     = "${var.project_name}-network"
  ip_range = "10.0.0.0/16"
}

resource "hcloud_network_subnet" "project_subnet" {
  network_id   = hcloud_network.project_network.id
  type         = "cloud"
  network_zone = "eu-central"
  ip_range     = "10.0.1.0/24"
}

# Attach the server to the network
resource "hcloud_server_network" "app_server_network" {
  server_id  = hcloud_server.app_server.id
  network_id = hcloud_network.project_network.id
  ip         = "10.0.1.1"
}
