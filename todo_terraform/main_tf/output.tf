# # show load balancer dns_name
# output "lb_dns_name" {
#     value = module.load_balancer.lb_dns_name
# }

output "rds_endpoint" {
    value = module.RDS.rds_endpoint
}