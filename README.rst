=======
ec2yaml
=======

This program deploys a Linux AWS EC2 instance with two volumes and two users based on a provided YAML configuration file. Note that this program is imperative and not declarative. In other words, each time the program runs, the specified configuration is created. There is no state that remembers past resources that were previously created.

Prerequisites
-------------
* Ensure ``python3.9``, ``pip``, ``git``, and the AWS CLI (``aws``) are installed on your machine. For download information, see https://www.python.org/, https://git-scm.com/, and https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html. To check for successful installation:

``python --version``

``pip --version``

``git --version``

``aws --version``

* Configure the AWS CLI to connect to AWS. The simplest method is to specify a default profile with an access key, secret key, and region. If you have multiple profiles, you can set the environment variable ``AWS_PROFILE=profile_name`` to specify that the configuration of profile ``profile_name`` should be used. For more info, see https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html. To validate access of the CLI to your AWS account, run a command, such as ``describe-instances``:

``aws ec2 describe-instances``

* The IAM user associated with your access key and secret key must have administrative permissions to create EC2-related resources. Specifically, the user must be able to call ``run_instances``, ``describe_images``, ``describe_vpcs``, ``create_default_vpc``, ``import_key_pair``, ``create_security_group``, and ``authorize_security_group_ingress`` from the boto3 client API library.

Installation
------------
* Clone the repository:

``git clone https://github.com/alexpcook/ec2yaml.git``

* Change into the repo directory:
 
``cd ec2yaml``

* Build and install the executable:
 
``pip install --user .``

* Or build and install a wheel:
 
``python setup.py bdist_wheel && pip install --user dist/*.whl``

* Ensure that the pip binary installation directory is in your ``PATH`` environment variable. That way, you can execute the program without having to remember the full filesystem prefix to the executable. For example, when the pip binary directory is ``/root/.local/bin``:

``WARNING: The script ec2yaml is installed in '/root/.local/bin' which is not on PATH.``

``export PATH=$PATH:/root/.local/bin``

Usage
-----
* The executable requires a single file path argument to the YAML configuration for the EC2 instance.

``ec2yaml /path/to/ec2/yaml/file``

* A starting YAML template file can be found in the repository at ``templates/ec2_sample_config.yaml``. At a minimum, you will need to replace the user SSH keys with public keys of key pairs you have access to. To create a key pair for use with AWS EC2 and output the public key:

``ssh-keygen -t rsa -b 2048 -f /path/to/my_key_file``

``cat /path/to/my_key_file.pub``

* The settings in the YAML configuration file are:
  
``instance_type`` - The EC2 instance type to create (e.g. ``t2.micro``).

``ami_type`` - The prefix to search for in the EC2 instance name (e.g. specifying ``amzn2`` will filter on AMI IDs that have a name beginning with ``amzn2``).

``architecture`` - The architecture on which to filter AMI IDs (e.g. ``i386`` | ``x86_64`` | ``arm64``).

``root_device_type`` - The storage type on which to filter AMI IDs (e.g. ``ebs`` | ``instance-store``).

``virtualization_type`` - The hypervisor technology type on which to filter AMI IDs (e.g. ``paravirtual`` | ``hvm``).

``min_count`` - The minimum count of EC2 instances to create.

``max_count`` - The maximum count of EC2 instances to create.

``volumes`` - A list of volumes to create. The device (``device``), size in GiB (``size_gb``), filesystem type (``type``), and mount point (``mount``) are specified.

``users`` - A list of users to create. The user's login name (``login``) and public key for SSH to the EC2 instance (``ssh_key``) are specified.

* When an EC2 instance is successfully created, ``ec2yaml`` will show the public IP address of the instance. You can also get the public IP address by using the AWS CLI: ``aws ec2 describe-instances``. This IP address can then be used to SSH as one of the created users. Replace the private key file path, user name, and IP address in the following statement to match your own deployment:
  
``ssh -i /path/to/my_key_file user@1.2.3.4``

* All the users specified in the YAML file have read/write access to the mounted volumes in the configuration via a shared Linux group ownership of the mount points.
