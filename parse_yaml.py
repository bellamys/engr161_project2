import yaml

with open('layout.yml', 'r') as fid:
    data = yaml.load(fid, Loader=yaml.SafeLoader)

print(data)