# The "name" of the availability domain to be used for the compute instance.
output "name-of-first-availability-domain" {
  value = data.oci_identity_availability_domains.ads.availability_domains[0].name
}

# Outputs for compute instance

output "public-ip-for-compute-instance" {
  value = oci_core_instance.mcserver2.public_ip
}


output "instance-name" {
  value = oci_core_instance.mcserver2.display_name
}

output "instance-OCID" {
  value = oci_core_instance.mcserver2.id
}

output "instance-region" {
  value = oci_core_instance.mcserver2.region
}

output "instance-shape" {
  value = oci_core_instance.mcserver2.shape
}

output "instance-state" {
  value = oci_core_instance.mcserver2.state
}

output "instance-OCPUs" {
  value = oci_core_instance.mcserver2.shape_config[0].ocpus
}

output "instance-memory-in-GBs" {
  value = oci_core_instance.mcserver2.shape_config[0].memory_in_gbs
}

output "time-created" {
  value = oci_core_instance.mcserver2.time_created
}
