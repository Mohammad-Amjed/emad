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

    src_format = compileRE(map_driver)
    
    m = src_format.match(input_tag)

    src_vals = extractFeats(map_driver, m)
    print(src_vals)

    trg_feats = convertFeats(src_vals, map_driver)

    trg_tag = finalTag(trg_feats, map_driver)

    pprint(trg_tag)


def compileRE(map_driver):
    src_format = map_driver["format"]
    src_feats = map_driver["features"]

    for feat in src_feats:
        if feat in map_driver['map'] and '#VAL#' not in map_driver['map'][feat]:
            values = '(' + '|'.join(map_driver['map'][feat].keys()) + ')'
        else:
            values = "\\S+"
        src_format = src_format.replace(f"#{feat}#", f"(?P<{feat}>{values})", 1)

    print(src_format)
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

def finalTag(trg_feats, map_driver):
    final = []
    keys = [int(i) for i in trg_feats.keys()]
    keys.sort()
    keys = [str(i) for i in keys]
    base_order = int(map_driver['base_word_order'])
    
    for k in keys:
        final.append(trg_feats[k])
        if int(k) == base_order:
            final[-1]['orth'] = "base"
        elif int(k) < base_order:
            final[-1]['orth'] = "proc"
        elif int(k) > base_order:
            final[-1]['orth'] = "enc"

    return final

if __name__ == "__main__":
    main()