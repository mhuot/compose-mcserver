
# Data Source: Fetch SSH keys
data "http" "github_keys" {
  url = "https://github.com/mhuot.keys"
}

# Local Variable: Process SSH keys
locals {
  ssh_keys = try(
    split("\n", chomp(data.http.github_keys.response_body)),
    []
  )
}

resource "oci_core_instance" "mcserver2" {
    # Required
    availability_domain = data.oci_identity_availability_domains.ads.availability_domains[2].name
    compartment_id = "ocid1.tenancy.oc1..aaaaaaaarm6f5422lt7uuimf3qkjt5emhyy73zoda37xvm3wofidihsxxvhq"
    shape = "VM.Standard.A1.Flex"
    shape_config {
        ocpus = 4
        memory_in_gbs = 24
    }

    source_details {
        source_id = "ocid1.image.oc1.us-chicago-1.aaaaaaaazn6piezti3khlsminniokag5cs7jiu3csqdiib3ex2jqv76qx3cq"
        source_type = "image"
    }

    # Optional
    display_name = "mcserver2"
    create_vnic_details {
        assign_public_ip = true
        subnet_id = "ocid1.subnet.oc1.us-chicago-1.aaaaaaaat3gg7anhtnmp2uqsrch5fkd6twjyoeflepsvagy436uaorcgux5a"
    }
    
    metadata = {
        ssh_authorized_keys = join("\n", local.ssh_keys) # Join the list into a single string
    }

    preserve_boot_volume = false
}
