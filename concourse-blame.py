import json
import sys

if len(sys.argv) < 2:
    print('USAGE: python concourse-blame.py /path/to/config.json')
    exit(0)

# load configuration
config_path = sys.argv[1]
config = {}
with open(config_path) as config_file:
    config = json.load(config_file)
if not config:
    print('Could not read configuration from file {}'.format(config_path))
    exit(1)

print('It works! {}'.format(config))
