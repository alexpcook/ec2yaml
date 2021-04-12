import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the YAML file to use for making the EC2 instances')
    return parser
