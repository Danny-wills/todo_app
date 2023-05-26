# export bastion_host sg id
output "bastion_host_sg" {
    value = aws_security_group.bastion_host_sg.id
}
# export private instance sg id
output "private_instance_sg" {
    value = aws_security_group.private_instances.id
}
# export load balancer sg id
output "load_balancer_sg" {
    value = aws_security_group.lb_sg.id
}
# export rds sg id
output "rds_sg" {
    value = aws_security_group.rds_sg.id
} 
