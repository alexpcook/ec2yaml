import argparse

def get_parser():
    """
    Returns the CLI parser to get the YAML file for the EC2 instance configuration.
    Retrieve the YAML configuration file using the 'file' argument.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the YAML file to use for making the EC2 instances')
    return parser
