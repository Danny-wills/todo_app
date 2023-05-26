resource "aws_db_subnet_group" "todo_app" {
  name       = "todo_app"
  subnet_ids = [var.pub_subnet1, var.pub_subnet2]
}

#create a RDS Database Instance
resource "aws_db_instance" "myinstance" {
  engine               = "postgres"
  identifier           = "todo-app"
  allocated_storage    =  5
  engine_version       = "14.1"
  instance_class       = "db.t3.micro"
  username             = "postgress"
  password             = "Owdanny400"
  db_subnet_group_name = aws_db_subnet_group.todo_app.name
  vpc_security_group_ids = ["${var.rds_sg_id}"]
  skip_final_snapshot  = true
  publicly_accessible =  true
  port                  = "5432"
  db_name               = "todo_app"
}