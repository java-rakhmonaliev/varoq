output "server_ip" {
  description = "Public IP of the EC2 instance (add this to GitHub Secrets as EC2_HOST)"
  value       = aws_eip.app.public_ip
}

output "ssh_command" {
  description = "SSH into your server"
  value       = "ssh ubuntu@${aws_eip.app.public_ip}"
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.app.id
}
