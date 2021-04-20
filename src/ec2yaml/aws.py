import boto3
import random
import requests
import string
import sys

def create_instance(config):
    """
    Creates an EC2 instance from the configuration settings.
    """

    try:
        client = boto3.client('ec2')
    except Exception as e:
        print(f'An error occurred while creating the boto3 client: {e}')
        sys.exit(1)

    ami_id = _get_ami_id(client, config.ami_type, config.architecture, config.root_device_type, config.virtualization_type)
    default_vpc_id = _ensure_default_vpc(client)
    key_pair_names = _create_key_pairs(client, config)

    blockDeviceMappings = []
    for volume in config.volumes:
        blockDeviceMappings.append({
            'DeviceName': volume.device,
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': volume.size_gb,
                'VolumeType': 'gp2',
            },
        })

    res = client.run_instances(
        BlockDeviceMappings=blockDeviceMappings,

        ImageId=ami_id,
        InstanceType=config.instance_type,

        MaxCount=config.max_count,
        MinCount=config.min_count,

        SecurityGroupIds=[
            _create_security_group(client, default_vpc_id)
        ],

        UserData=_user_data_script(config),
    )

    ec2 = boto3.resource('ec2')
    instances = res['Instances']

    for i, instance in enumerate(instances):
        public_ip = ec2.Instance(instance['InstanceId']).public_ip_address
        print(f'instance {i} public ip address = {public_ip}')

def _get_ami_id(client, ami_type, arch, root_dev_type, virtualization_type):
    """
    Finds an AMI ID given the AMI name, architecture, root device type, and virtualization type.
    Exits with status code 1 if no AMI ID was found. If more than one AMI ID was found, it selects
    the first one in the list.
    """

    res = client.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [f'{ami_type}*'],
            },
            {
                'Name': 'architecture',
                'Values': [arch],
            },
            {
                'Name': 'virtualization-type',
                'Values': [virtualization_type],
            },
            {
                'Name': 'root-device-type',
                'Values': [root_dev_type],
            },
        ],
    )

    images = res['Images']
    if len(images) < 1:
        print(f"""unable to find at least one AMI ID based on search critera:
    name: {ami_type}*
    architecture: {arch}
    virtualization_type: {virtualization_type}
    root_device_type: {root_dev_type}""")
        sys.exit(1)

    return images[0]['ImageId']

def _ensure_default_vpc(client):
    """
    Ensures that there is a default VPC available in the region used by the boto3 EC2 client.
    Create the default VPC if it doesn't exist.
    """

    default_vpc_filter_expression = [{
        'Name': 'isDefault',
        'Values': ['true'],
    }]

    res = client.describe_vpcs(Filters=default_vpc_filter_expression)

    if res['Vpcs']:
        return res['Vpcs'][0]['VpcId']
    else:
        return client.create_default_vpc()['Vpc']['VpcId']

def _create_key_pairs(client, config):
    """
    Creates the SSH key pairs from the EC2 instance configuration.
    """

    key_pair_names = []

    for user in config.users:
        res = client.import_key_pair(
            KeyName=f'{user.login}-kp-{_rand_chars(10)}',
            PublicKeyMaterial=bytes(user.ssh_key, encoding='UTF-8'),
        )
        key_pair_names.append(res['KeyName'])

    return key_pair_names

def _create_security_group(client, vpc_id):
    """
    Creates the security group for the EC2 instance to allow SSH traffic from
    the user's public IP address. If there is a problem determining the user's
    public IP address, SSH will be open to all IP addresses (0.0.0.0/0).
    """

    res = client.create_security_group(
        Description="Allow ssh from user public IP address",
        GroupName=f'ssh-from-public-ip-{_rand_chars(10)}',
        VpcId=vpc_id,
    )

    group_id = res['GroupId']

    try:
        public_ip = f'{requests.get("https://checkip.amazonaws.com/").text.strip()}/32'
    except Exception:
        print('encountered error getting public ip; using 0.0.0.0/0 instead')
        public_ip = '0.0.0.0/0'

    res = client.authorize_security_group_ingress(
        CidrIp=public_ip,
        FromPort=22,
        GroupId=group_id,
        IpProtocol='tcp',
        ToPort=22,
    )

    return group_id

def _user_data_script(config):
    """
    Returns the user data script for the initialization of the EC2 instance.
    """

    return f"""
#!/bin/bash
{_create_users(config.users)}
{_mount_volumes(config.volumes)}
{_set_user_permissions_for_volumes(config.users, config.volumes)}
"""

def _create_users(users):
    """
    Returns the section of the user data script to create a single Linux user
    and their SSH key pair on the EC2 instance.
    """

    user_data_script_section = ''

    for user in users:
        login = user.login
        ssh_key = user.ssh_key
        ssh_key_dir = f'~{login}/.ssh'
        ssh_auth_keys_file = f'{ssh_key_dir}/authorized_keys'

        user_data_script_section += f"""
adduser {login}
mkdir {ssh_key_dir}
chmod 700 {ssh_key_dir}
chown {login}:{login} {ssh_key_dir}
touch {ssh_auth_keys_file}
chmod 600 {ssh_auth_keys_file}
chown {login}:{login} {ssh_auth_keys_file}
echo {ssh_key} >> {ssh_auth_keys_file}
"""

    return user_data_script_section

def _mount_volumes(volumes):
    """
    Returns the section of the user data script to configure and mount
    the volumes on the EC2 instance.
    """

    user_data_script_section = ''

    for volume in volumes:
        device = volume.device
        vol_type = volume.vol_type
        directory = volume.mount

        user_data_script_section += f"""
mkfs -t {vol_type} {device}
ls {directory} || mkdir {directory}
mount {device} {directory}
"""

    return user_data_script_section

def _set_user_permissions_for_volumes(users, volumes):
    """
    Returns the section of the user data script to create a Linux
    user group and grant the group permission to access the mounted
    volumes on the EC2 instance.
    """

    group_name = 'volumes'

    user_data_script_section = f"""
groupadd {group_name}
"""

    for user in users:
        user_data_script_section += f"""
usermod -a -G {group_name} {user.login}
"""
    for volume in volumes:
        user_data_script_section += f"""
chgrp -R {group_name} {volume.mount}
chmod -R 2775 {volume.mount}    
"""

    return user_data_script_section

def _rand_chars(n):
    """
    Returns n random characters from the set of ASCII lowercase letters and digits.
    """

    return "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(n)])
