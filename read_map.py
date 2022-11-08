from pprint import pprint
import json

def read(filename):
    tagset = {}
    tagset['features'] = []
    tagset['map'] = {}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            config = line[0]
            
            if config == "DEFINE":
                tagset['features'].append(line[1])
            
            elif config == "FORMAT":
                tagset['format'] = line[1]

            elif config == "CONFIG":
                tagset[line[1]] = line[2]
            elif config == "MAP":
                feature = line[1]
                if not feature in tagset['map'].keys():
                    tagset['map'][feature] = {}
                
                val = line[2]
                tagset['map'][feature][val] = {}

                i = 3
                order = 3
                while i < len(line):
                    if line[i].isdigit():
                        order = line[i]
                        tagset['map'][feature][val][order] = {}
                        i += 1
                    else:
                        tagset['map'][feature][val][order][line[i]] = line[i+1]
                        i += 2


    
    return tagset

map = "MADA_to_EMADA"

tagset = read(f"./mappings/{map}.txt")

with open(f'{map}.json', 'w') as fp:
    json.dump(tagset, fp)