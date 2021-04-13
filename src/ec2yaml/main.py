def main():
    from ec2yaml import aws, cli, ec2_config

    parser = cli.get_parser()
    args = parser.parse_args()

    instance_config = ec2_config.EC2Config(args.file)
    aws.create_instance(instance_config)
