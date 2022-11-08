from ast import parse
from pprint import pprint
from copy import deepcopy

def main():
    map_file = "./mappings/MADA_pp.txt"
    mapping = read_map(map_file)

    input = "diac:li>akotubahu lex:katab pos:verb prc3:0 prc2:0 prc1:li_sub prc0:0 per:1 asp:i vox:a mod:s form_gen:m gen:m form_num:s num:s stt:na cas:na enc0:3ms_dobj rat:n"
    
    parsed_input = parse_input(input)
    
    output = convert(parsed_input, mapping)

    pprint(output)

def read_map(map_file):
    mapping = {}
    with open(map_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip().split()
        [Class, mada, mada_pp] = line
        
        if Class not in mapping:
            mapping[Class] = {}
        
        mapping[Class][mada] = mada_pp

    return mapping

def parse_input(input):
    parsed_input = {}

    features = input.split()
    for feat in features:
        [key, val] = feat.split(":")
        parsed_input[key] = val

    return parsed_input

def convert(parsed_input, mapping):
    output = []

    output += convert_prc(parsed_input, mapping)
    
    #handling the base word

    output.append(convert_base(parsed_input))

    output += convert_enc(parsed_input, mapping)

    return output

def convert_prc(parsed_input, mapping):
    output = []
    for feat in ['prc3', 'prc2', 'prc1', 'prc0']:
        Class = 'proclitic'
        val = parsed_input[feat]

        if val not in ['na', '0']:
            new_tag = { 'ort': feat, 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na',
                        'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na',
                        'num': 'na', 'rat': 'na'}

            new_tag['pos'] = clitic_to_pos(mapping, val, Class)
            new_tag['diac'] = val.split('_')[0]
            new_tag['lex'] = 'TODO'

            output.append(new_tag)
        
    return output

def clitic_to_pos(mapping, val, Class):
    val_delex = "*_" + val.split('_')[1]
    return mapping[Class][val_delex]

def convert_base(parsed_input):
    base = deepcopy(parsed_input)
    base.pop("prc3")
    base.pop("prc2")
    base.pop("prc1")
    base.pop("prc0")
    base.pop("enc0")
    base['ort'] = "base"
    return base

def convert_enc(parsed_input, mapping):
    feat = "enc0"
    Class = "enclitic"
    val = parsed_input[feat]

    output = []

    if val not in ['0', 'na']:
        new_tag = { 'ort': feat, 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na',
                    'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na',
                    'num': 'na', 'rat': 'na'}
        
        new_tag['pos'] = clitic_to_pos(mapping, val, Class)
        new_tag['diac'] = 'TODO'
        new_tag['lex'] = 'TODO'

        if val[0].isdigit():
            new_tag['per'] = val[0]
            if val[2] == "_":
                new_tag['gen'] = "u"
                new_tag['num'] = val[1]
            elif val[3] == "_":
                new_tag['gen'] = val[1]
                new_tag['num'] = val[2]
        
        output.append(new_tag)

    return output

if __name__ == "__main__":
    main()