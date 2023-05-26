provider "aws" {
  region  = var.region
  profile = "default"
}

# create vpc
module "vpc" {
  source               = "../modules/VPC"
  region               = var.region
  vpc_cidr             = var.vpc_cidr
  project_name         = var.project_name
  public_subnet1_cidr  = var.public_subnet1_cidr
  public_subnet2_cidr  = var.public_subnet2_cidr
  private_subnet1_cidr = var.private_subnet1_cidr
  private_subnet2_cidr = var.private_subnet2_cidr
}

# # create nat gateway
# module "NAT_gateway" {
#   source             = "../modules/NAT_gateway"
#   vpc_id             = module.vpc.vpc_id
#   public_subnet1_id  = module.vpc.public_subnet1_id
#   public_subnet2_id  = module.vpc.public_subnet2_id
#   private_subnet1_id = module.vpc.private_subnet1_id
#   private_subnet2_id = module.vpc.private_subnet2_id
#   project_name       = module.vpc.project_name
#   internet_gateway   = module.vpc.internet_gateway
# }
# create security groups
module "security_groups" {
  source       = "../modules/SG"
  vpc_id       = module.vpc.vpc_id
  project_name = module.vpc.project_name
}

# Create RDS instance
module "RDS" {
  source       ="../modules/RDS"
  rds_sg_id    = module.security_groups.rds_sg 
  pub_subnet1 = module.vpc.public_subnet1_id
  pub_subnet2 = module.vpc.public_subnet2_id

  depends_on = [ module.security_groups ]
}

# # create bastion host
# module "bastion_host" {
#   source             = "../modules/Bastion_host"
#   ami                = var.ami
#   instance_type      = var.instance_type
#   public_subnet1_id  = module.vpc.public_subnet1_id
#   bastion_host_sg_id = module.security_groups.bastion_host_sg
#   efs_id             = module.EFS.efs_id
# 	efs_dns_name 			 = module.EFS.efs_dns
# }

# # create load balancer
# module "load_balancer" {
# 	source						= "../modules/load_balancer"
# 	lb_sg						 	= module.security_groups.load_balancer_sg
# 	public_subnet1_id = module.vpc.public_subnet1_id
# 	public_subnet2_id = module.vpc.public_subnet2_id
# 	project_name 			= module.vpc.project_name
# 	vpc_id						= module.vpc.vpc_id
# }	

# # create autoscaling group
# module "autoscaling_group" {
# 	source 							= "../modules/ASG"
# 	image_id            = var.ami
# 	instance_type		    = var.instance_type
# 	user_data					  = module.bastion_host.user_data
# 	project_name		 		= module.vpc.project_name
# 	private_subnet1_id	= module.vpc.private_subnet1_id
# 	private_subnet2_id	= module.vpc.private_subnet2_id
# 	target_group_arn		= module.load_balancer.target_group_arn
# 	private_instance_sg = module.security_groups.private_instance_sg
# }

# # create dns
# module "DNS" {
# 	source 			= "../modules/DNS"
# 	lb_dns_name = module.load_balancer.lb_dns_name
# 	lb_zone_id 	= module.load_balancer.lb_zone_id
# }