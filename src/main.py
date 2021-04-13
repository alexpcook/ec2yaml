import aws
import ec2_config
import cli

if __name__ == '__main__':
    parser = cli.get_parser()
    args = parser.parse_args()
    
    instance_config = ec2_config.EC2Config(args.file)
    ec2_client = aws.get_client()

    aws.create_instance(ec2_client, instance_config)
