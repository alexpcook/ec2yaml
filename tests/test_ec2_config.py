import pytest
import yaml

from ec2yaml import ec2_config

def test_file_does_not_exist():
    """
    If the EC2 configuration file does not exist, the utility should raise a FileNotFoundError.
    """
    
    with pytest.raises(FileNotFoundError):
        config = ec2_config.EC2Config('/some/invalid/path')

def test_file_exists_but_is_not_valid_yaml():
    """
    If the given file is not valid YAML, the utility should raise an error.
    In this particular case, using a str key index on a str type raises a TypeError.
    """

    with pytest.raises(TypeError):
        config = ec2_config.EC2Config('tests/test.txt')

def test_file_with_vaild_yaml():
    """
    If the given file is valid YAML, the utility should not raise an error.
    The instance of the EC2Config class should have all expected properties.
    """

    config = ec2_config.EC2Config('tests/test.yaml')

    assert config.instance_type == 't2.micro'
    assert config.ami_type == 'amzn2'
    assert config.architecture == 'x86_64'
    assert config.root_device_type == 'ebs'
    assert config.virtualization_type == 'hvm'
    assert config.min_count == 1
    assert config.max_count == 1

    assert len(config.volumes) == 2
    for volume in config.volumes:
        assert isinstance(volume, ec2_config.EC2Volume)

    assert config.volumes[0].device == '/dev/xvda'
    assert config.volumes[0].size_gb == 10
    assert config.volumes[0].vol_type == 'gp2'
    assert config.volumes[0].mount == '/'
    assert config.volumes[1].device == '/dev/xvdf'
    assert config.volumes[1].size_gb == 100
    assert config.volumes[1].vol_type == 'gp3'
    assert config.volumes[1].mount == '/data'

    assert len(config.users) == 2
    for user in config.users:
        assert isinstance(user, ec2_config.EC2User)
    
    assert config.users[0].login == 'user1'
    assert config.users[0].ssh_key == '--user1 ssh public key goes here-- user1@localhost'
    assert config.users[1].login == 'user2'
    assert config.users[1].ssh_key == '--user2 ssh public key goes here-- user2@localhost'
