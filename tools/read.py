map_dir = "./mappings"

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

def read_map(map): # ex: map = "MADA_to_EMADA"

    filename = f"{map_dir}/{map}.txt"

    tagset = {
        'features': [], 
        'map': {},
        'format': None
        }
    
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
                if not val in tagset['map'][feature].keys():
                    tagset['map'][feature][val] = [{}]
                else:
                    tagset['map'][feature][val].append({})

                if len(line) >= 4:
                    order = line[3]
                    tagset['map'][feature][val][-1][order] = {}

                    i = 4
                    while i < len(line):
                        if line[i].isdigit():
                            order = line[i]
                            if not order in tagset['map'][feature][val][-1].keys():
                                tagset['map'][feature][val][-1][order] = {}
                            i += 1
                        else:
                            out_feat = line[i]
                            out_val = line[i+1]
                            tagset['map'][feature][val][-1][order][out_feat] = out_val
                            i += 2

    return tagset

def read_map_rev(map):
    filename = f"{map_dir}/{map}.txt"

    map_dict = {
        'map': {},
        'format': None
    }

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            config = line[0]
            
            if config == "FORMAT":
                map_dict['format'] = line[1]

            elif config == "CONFIG":
                map_dict[line[1]] = line[2]

            elif config == "MAP":
                out_feat = line[1]
                out_val = line[2]

                if len(line) > 4:
                    order = line[3]
                    feat_comb = [] #combination of features

                    i = 4
                    while i < len(line):
                        if line[i].isdigit():
                            order = line[i]
                            i += 1
                        else:
                            feat_comb.append((order, line[i], line[i+1]))
                            i += 2
                    
                    feat_comb = tuple(feat_comb)
                    map_dict['map'][feat_comb] = (out_feat, out_val)
            
    return map_dict