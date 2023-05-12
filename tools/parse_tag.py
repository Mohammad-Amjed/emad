from pyfoma import FST, Paradigm
import re

def cln_re_spcl_chrs(value):
    for i in "[]^$?*+()/|_:":       # in case any regex chrs are in the values, expecially BW
        value = value.replace(i, f"\{i}")
    value = value.replace(".", "。")
    return value

def get_vals(feat, map_driver):
    vals = [cln_re_spcl_chrs(v) for v in list(map_driver['map'][feat].keys())]
    vals = "|".join(vals)
    #print(vals)
    return vals

def make_fst_format(feats, format):
    format = format.replace(":", "\:")
    format = format.replace(".", "。")
    format = format.replace("_", "\_")
    for feat in feats:
        format = format.replace(f"#{feat}#", f" ${feat} ")
    
    #print(format)
    return format

def make_fst(map_driver):
    fsts = {}

    #print(map_driver)
    for feat in map_driver['features']:
        if feat in map_driver['map']:
            #print(f"'':'<{feat}>' ({get_vals(feat, map_driver)}) '':'<\/{feat}>'")
            fsts[feat] = FST.re(f"'':'<{feat}>' ({get_vals(feat, map_driver)}) '':'<\/{feat}>'")
            #print(f"'':'<{feat}>' ({get_vals(feat, map_driver)}) '':'<\/{feat}>'")

    fst_format = make_fst_format(map_driver['features'], map_driver['format'])
    #print(fst_format)
    fst = FST.re(fst_format, fsts)

    return fst

def extract_feats(input_tag, map_driver):
    #print(map_driver['format'])
    fst = make_fst(map_driver)
    #x = Paradigm(fst, ".*")
    print(input_tag)
    x = Paradigm(fst, input_tag)
    return x

def get_feat_val_dicts(parsed_tag, map_driver):
    feat_val_dict = {}
    for feat in map_driver['features']:
        if m := re.search(f"<{feat}>(?P<val>.*)</{feat}>", parsed_tag):
            feat_val_dict[feat] = m['val']
    return feat_val_dict

def parse(input_tag, map_driver):
    dicts = []

    input_tag = cln_re_spcl_chrs(input_tag)
    parsed_tags = extract_feats(input_tag, map_driver)
    #print(parsed_tags)
    for tag in parsed_tags.para:
        tag = tag[2]
        #get_feat_val_dicts(tag, map_driver)
        dicts.append(get_feat_val_dicts(tag, map_driver))
    
    return dicts
'''
map = "CAMeL_to_EMADA"
input_tag = "PART+ADJ+PRON"
map_driver = read.read_map(map)
parse(input_tag, map_driver)
'''