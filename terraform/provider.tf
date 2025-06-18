terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "oci" {
  tenancy_ocid = "ocid1.tenancy.oc1..aaaaaaaarm6f5422lt7uuimf3qkjt5emhyy73zoda37xvm3wofidihsxxvhq"
  user_ocid = "ocid1.user.oc1..aaaaaaaaaa3rg3dowhdpxptd4o7ef2iyavgpujhljccepcy72ylpmipcsg4a" 
  private_key_path = "~/.ssh/oci.pem"
  fingerprint = "86:8a:0f:62:b6:a3:36:79:ff:36:06:69:99:52:5e:5b"
  region = "us-chicago-1"
}


provider "cloudflare" {
  api_token = var.cloudflare_api_token
}