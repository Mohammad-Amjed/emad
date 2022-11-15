import re, json
from pprint import pprint

# TODO handle DIAC
# TODO handle the morphological analysis of each "subword"
# TODO replace -1 in output tag with default values

map_dir = "./mappings"
src = "CAMEL_to_EMADA.json"
#input_tag = "diac:wawAsiTatahum lex:wAsiTap pos:noun prc3:0 prc2:wa_conj prc1:0 prc0:0 per:na asp:na vox:na mod:na form_gen:f gen:f form_num:s num:s stt:c cas:a enc0:3mp_poss rat:i"
input_tag = "CONJ+PART_FUT+ADJ.MS+PRON"

def main():
    with open(f"{map_dir}/{src}", 'r') as f:
        map_driver = json.load(f)

    def_dict = readDefaults("./mappings/defaults.txt")
    pprint(def_dict)
    
    src_format = compileRE(map_driver)
    
    m = src_format.match(input_tag)

    src_vals = extractFeats(map_driver, m)
    print(src_vals)

    trg_feats = convertFeats(src_vals, map_driver)

    trg_tag = orderTag(trg_feats, map_driver)

    trg_tag = addDefaults(trg_tag, def_dict)

    pprint(trg_tag)

def readDefaults(def_file):
    def_dict = {}
    with open(def_file) as f:
        for line in f:
            line = line.strip().split('\t')
            pos = line[0].split(':')[1]
            feat_val = [pair.split(':') for pair in line[1].split()]
            def_tag = {pair[0]:pair[1] for pair in feat_val}
            def_dict[pos] = def_tag

    return def_dict

def compileRE(map_driver):
    src_format = map_driver["format"]
    src_feats = map_driver["features"]

    for feat in src_feats:
        if feat in map_driver['map'] and '#VAL#' not in map_driver['map'][feat]:
            values = '(' + '|'.join(map_driver['map'][feat].keys()) + ')'
        else:
            values = "\\S+"
        src_format = src_format.replace(f"#{feat}#", f"(?P<{feat}>{values})", 1)

    #print(src_format)
    return re.compile(src_format)

def extractFeats(map_driver, match):
    vals = {}
    for feat in map_driver['features']:
        if match.group(feat):
            vals[feat] = match.group(feat)

    return vals

def empty_tag():
    new_tag = { 'orth': '-1', 'per': '-1', 'asp': '-1', 'cas': '-1', 'stt': '-1',
                'mod': '-1', 'vox': '-1', 'form_gen': '-1', 'gen': '-1', 'form_num': '-1',
                'num': '-1', 'rat': '-1'}
    return new_tag

def convertFeats(src_vals, map_driver):
    output = {}
    mapping = map_driver['map']
    for feat in src_vals.keys():
        if feat in mapping.keys():
            val = src_vals[feat]
            if val in mapping[feat].keys():
                for order in mapping[feat][val].keys():
                    if order not in output:
                        output[order] = empty_tag()
                    for outfeat in mapping[feat][val][order]:
                        output[order][outfeat] = mapping[feat][val][order][outfeat]

            elif "#VAL#" in mapping[feat].keys():
                for order in mapping[feat]["#VAL#"].keys():
                    if order not in output:
                        output[order] = empty_tag()
                    for outfeat in mapping[feat]["#VAL#"][order]:
                        output[order][outfeat] = mapping[feat]["#VAL#"][order][outfeat].replace("#VAL#", val)
    
    return output

def orderTag(trg_feats, map_driver):
    ordered = []
    keys = [int(i) for i in trg_feats.keys()]
    keys.sort()
    keys = [str(i) for i in keys]
    base_order = int(map_driver['base_word_order'])
    
    for k in keys:
        ordered.append(trg_feats[k])
        if int(k) == base_order:
            ordered[-1]['orth'] = "base"
        elif int(k) < base_order:
            ordered[-1]['orth'] = "proc"
        elif int(k) > base_order:
            ordered[-1]['orth'] = "enc"

    return ordered

def addDefaults(tag, def_tag):
    for subtag in tag:
        pos = subtag['pos']
        if pos not in def_tag:
            print(f"Error: pos {pos} not found in the defaults list")
        else:
            for feat in subtag:
                if subtag[feat] == '-1':
                    subtag[feat] = def_tag[pos][feat]

    return tag

if __name__ == "__main__":
    main()