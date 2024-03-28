module "kubernetes" {
  source       = "/home/joaome/Personal/Estudos/terraform-eks"
  cidr_block   = "10.34.0.0/16"
  project_name = "restapi-flask"
  region       = "us-east-1"
  tags = {
    Department = "DevOps"
  }
}
