provider "aws" {
  region  = var.region
  profile = "licitamex"
}


resource "aws_dynamodb_table" "licitaciones_table" {
  name           = "licitaciones"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "licitacion"
  range_key      = "entidad"

  attribute {
    name = "licitacion"
    type = "S"
  }

  attribute {
    name = "entidad"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

}


resource "aws_dynamodb_table" "states_table" {
  name           = "states"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "name"

  attribute {
    name = "name"
    type = "S"
  }

}


resource "aws_dynamodb_table" "alerts_table" {
  name           = "alerts"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "licitacion"
  range_key      = "usuario"

  attribute {
    name = "licitacion"
    type = "S"
  }

  attribute {
    name = "usuario"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

}
