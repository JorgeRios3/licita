output "licitaciones_table_id" {
  value = aws_dynamodb_table.licitaciones_table.id
}

output "states_table_id" {
  value = aws_dynamodb_table.states_table.id
}

output "alerts_table_id" {
  value = aws_dynamodb_table.alerts_table.id
}
