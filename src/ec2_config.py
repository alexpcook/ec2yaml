import yaml

class EC2Volume():
    """
    Encapsulates settings for an AWS EC2 volume.
    """

    def __init__(self, device, size_gb, vol_type, mount):
        self.device = device
        self.size_gb = size_gb
        self.vol_type = vol_type
        self.mount = mount

class EC2User():
    """
    Encapsulates settings for an AWS EC2 user.
    """

    def __init__(self, login, ssh_key):
        self.login = login
        self.ssh_key = ssh_key

class EC2Config():
    """
    Encapsulates settings for an AWS EC2 instance configuration with two volumes and two users.
    """

    def __init__(self, raw_yaml):
        ec2_settings = raw_yaml['server']

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
