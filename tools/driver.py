import pandas as pd
from tools import parse_tag

map_dir = "./mappings"

class Driver(dict):
    def __init__(self):
        self['features'] = []
        self['format'] = None
        self['map'] = None
        self['fst'] = None

    def read(self, tagset):
        
        file = f"{map_dir}/{tagset}_def.txt"
        with open(file, 'r') as f:
            for line in f:
                line = line.strip().split('\t')
                config = line[0]
                
                if config == "DEFINE":
                    self['features'].append(line[1])
                
                elif config == "FORMAT":
                    self['format'] = line[1]

        mapping_file = f"{map_dir}/{tagset}_map.txt"
        self['map'] = pd.read_csv(mapping_file, delimiter='\s+')

    def make_fst(self):
        self['fst'] = parse_tag.make_fst(self)

def setup_driver(tagset):
    map_driver = Driver()
    map_driver.read(tagset)
    map_driver.make_fst()

    return map_driver