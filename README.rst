=======
ec2yaml
=======

This program deploys a Linux AWS EC2 instance with two volumes and two users based on a provided YAML configuration file. Note that this program is imperative and not declarative. In other words, each time the program runs, the specified configuration is created. There is no state that remembers past resources that were previously created.

Prerequisites
-------------
* Ensure ``python3.9``, ``pip``, and ``git`` are installed on your machine. For download information, see https://www.python.org/ and https://git-scm.com/.
* Configure the AWS CLI to connect to AWS. The simplest way is to specify a default profile with an access key, secret key, and region. If you have multiple profiles, you can set ``AWS_PROFILE=profile_name`` to specify that the configuration of profile ``profile_name`` should be used. For more info, see https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html.
* The IAM user associated with your access key and secret key must have administrative permissions to create EC2-related resources. Specifically the user must be able to call ``run_instances``, ``describe_images``, ``describe_vpcs``, ``create_default_vpc``, ``import_key_pair``, ``create_security_group``, and ``authorize_security_group_ingress`` from the boto3 client API library.

Installation
------------
* Clone the repository:

``git clone https://github.com/alexpcook/ec2yaml.git``

* Change into the repo directory:
 
``cd ec2yaml``

* Build and install the executable:
 
``pip install .``

* Or build and install a wheel:
 
``python setup.py bdist_wheel && pip install --user dist/*.whl``

* Ensure that the pip binary installation directory is in your ``PATH`` environment variable. That way, you can execute the program without having to remember the full filesystem prefix to the executable.

Usage
-----
* The executable requires a single filepath parameter to the YAML configuration file for the EC2 instance.

``ec2yaml /path/to/ec2/yaml/file``

* A starting YAML template file can be found in the repository at ``templates/ec2_sample_config.yaml``. The possible setings are:
  
``instance_type`` - The EC2 instance type to create (e.g. ``t2.micro``).

``ami_type`` - The prefix to search for in the EC2 instance name (e.g. specifying ``amzn2`` will filter on AMI IDs that have a name beginning with ``amzn2``).

``architecture`` - The architecture on which to filter AMI IDs (e.g. ``i386`` | ``x86_64`` | ``arm64``).

``root_device_type`` - The storage type on which to filter AMI IDs (e.g. ``ebs`` | ``instance-store``).

``virtualization_type`` - The hypervisor technology type on which to filter AMI IDs (e.g. ``paravirtual`` | ``hvm``).

``min_count`` - The minimum count of EC2 instances to create.

``max_count`` - The maximum count of EC2 instances to create.

``volumes`` - A list of volumes to create. The device (``device``), size in GiB (``size_gb``), filesystem type (``type``), and mount point (``mount``) are specified.

``users`` - A list of users to create. The user's login name (``login``) and public key for SSH to the EC2 instance (``ssh_key``) are specified.

* When an EC2 instance is successfully created, ``ec2yaml`` will show the public IP address of the instance. This IP address can then be used to SSH as one of the created users. Replace the private key file path, user name, and IP address in the following statement to match your own deployment:
  
``ssh -i /path/to/private/key/file user@1.2.3.4``

* All the users specified in the YAML file have access to the mounted volumes in the configuration via a shared Linux group ownership of the mount points.
