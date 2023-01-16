from pprint import pprint
import json

def Defaults(def_file):
        def_dict = {}
        with open(def_file) as f:
            for line in f:
                line = line.strip().split('\t')
                pos = line[0].split(':')[1]
                feat_val = [pair.split(':') for pair in line[1].split()]
                def_tag = {pair[0]:pair[1] for pair in feat_val}
                def_dict[pos] = def_tag

        return def_dict

def map_to_json(map): # ex: map = "MADA_to_EMADA"

    filename = f"./mappings/{map}.txt"

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

    with open(f'./mappings/{map}.json', 'w') as fp:
        json.dump(tagset, fp)
