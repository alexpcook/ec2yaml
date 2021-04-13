import sys
import yaml

class EC2Volume():
    """
    Encapsulates settings for an AWS EBS volume.
    """

    def __init__(self, device, size_gb, vol_type, mount):
        self.device = device
        self.size_gb = size_gb
        self.vol_type = vol_type
        self.mount = mount

class EC2User():
    """
    Encapsulates settings for an AWS EC2 Linux user.
    """

    def __init__(self, login, ssh_key):
        self.login = login
        self.ssh_key = ssh_key

class EC2Config():
    """
    Encapsulates settings for an AWS EC2 instance with two EBS volumes and two users.
    """

    def __init__(self, yaml_config_file):
        try:
            with open(yaml_config_file) as f:
                raw_yaml = f.read()
        except FileNotFoundError:
            print(f'{yaml_config_file} not found')
            sys.exit(1)
        
        ec2_settings = yaml.safe_load(raw_yaml)['server']

        self.instance_type = ec2_settings['instance_type']
        self.ami_type = ec2_settings['ami_type']
        self.architecture = ec2_settings['architecture']
        self.root_device_type = ec2_settings['root_device_type']
        self.virtualization_type = ec2_settings['virtualization_type']
        self.min_count = ec2_settings['min_count']
        self.max_count = ec2_settings['max_count']

        volumes = ec2_settings['volumes']
        if len(volumes) != 2:
            raise ValueError(f'must supply two volumes for the instance, got {len(volumes)}')

        self.volumes = [EC2Volume(vol['device'], vol['size_gb'], vol['type'], vol['mount']) for vol in volumes]

        users = ec2_settings['users']
        if len(users) != 2:
            raise ValueError(f'must supply two users for the instance, got {len(users)}')

        self.users = [EC2User(user['login'], user['ssh_key']) for user in users]
