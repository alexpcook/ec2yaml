import aws
import ec2_config
import cli

if __name__ == '__main__':
    parser = cli.get_parser()
    args = parser.parse_args()

    instance_config = ec2_config.EC2Config(args.file)
    aws.create_instance(instance_config)
