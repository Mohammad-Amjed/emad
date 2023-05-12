import EMAD
from tools import driver

def convert(input_tag, map_driver):

    output_dict = output_feat_val_dict(input_tag, map_driver)

    return output_dict

def output_feat_val_dict(input_tag, map_driver):
    output_dict = {}

    output_dict = positive_map(input_tag, output_dict, map_driver)
    output_dict = negative_map(input_tag, output_dict, map_driver)
    
    return output_dict

def positive_map(input_tag, output_dict, map_driver):
    map_df = map_driver['map']
    #print(input_tag)
    for EMAD_cat, subtag in input_tag.items():
        if subtag:
            #print(EMAD_cat)
            rows = get_matching_rows(EMAD_cat, subtag, map_df)
            #print(rows)
            output_dict = add_rows_to_output(rows, output_dict)

    return output_dict

def get_matching_rows(EMAD_cat, subtag, map_df):
    rows = map_df[map_df['EMAD_cat'] == EMAD_cat]

    for feat, val in subtag.items():
        #print(feat, val)
        if val not in ['-1', '*']:
            rows = rows[(rows[feat] == val) | (rows[feat] == '-')]

    #print(EMAD_cat)
    #rint(rows)
    rows = rows[(rows[EMAD.FEATURES] != '-').any(axis=1)]

    return rows

def add_rows_to_output(rows, output_dict):
    for id, row in rows.iterrows():
        output_feat, output_val = row['feat'], row['val']
        if output_feat not in output_dict.keys():
            output_dict[output_feat] = []
        if output_val not in output_dict[output_feat]:
            output_dict[output_feat].append(output_val)
    
    return output_dict

def negative_map(input_tag, output_dict, map_driver):
    map_df = map_driver['map']

    for EMAD_cat, subtag in input_tag.items():
        if not subtag:
            rows = map_df[map_df['EMAD_cat'] == EMAD_cat]
            rows = rows[(rows[EMAD.FEATURES] == '-').all(axis=1)]
            output_dict = add_rows_to_output(rows, output_dict)

    return output_dict

if __name__ == "__main__":
    tagset = "BW"

    input_tag = EMAD.Tag({
        'PRC_DET': {'lex': 'Al', 'pos': 'part_det', 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na', 'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na', 'num': 'na', 'rat': 'na'},
        'BASE': {'per': 'na', 'asp': 'na', 'cas': 'a', 'stt': 'c', 'mod': 'na', 'vox': 'na', 'form_gen': 'm', 'gen': 'm', 'form_num': 's', 'num': 's', 'rat': 'i', 'pos': 'noun'}, 
        'ENC_PRON': {'per': '1', 'asp': 'na', 'cas': 'g', 'stt': '*', 'mod': 'na', 'vox': 'na', 'form_gen': '*', 'gen': '*', 'form_num': '*', 'num': 's', 'rat': '*', 'pos': 'pron'}
        })
    
    input_tag = EMAD.Tag({'PRC_QUES': None, 'PRC_CONJ': {'lex': 'wa', 'pos': 'conj', 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na', 'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na', 'num': 'na', 'rat': 'na'}, 'PRC_PREP': None, 'PRC_VPAR': {'lex': 'li', 'pos': 'part_sub', 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na', 'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na', 'num': 'na', 'rat': 'na'}, 'PRC_DET': None, 'BASE': {'lex': '*', 'pos': 'verb', 'per': '1', 'asp': 'i', 'cas': 'na', 'stt': 'na', 'mod': 's', 'vox': 'a', 'form_gen': 'm', 'gen': 'm', 'form_num': 's', 'num': 's', 'rat': 'n'}, 'ENC_PRON': None, 'ENC_PART': None})
    
    '''
    input_tag = EMAD.Tag([
        {'orth': 'proc', 'lex': 'Al', 'pos': 'part_det', 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na', 'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na', 'num': 'na', 'rat': 'na'},
        {'orth': 'base', 'lex': '>um~ap', 'pos': 'noun_prop', 'per': 'na', 'asp': 'na', 'cas': 'n', 'stt': 'd', 'mod':'na', 'vox':'na', 'form_gen':'m', 'gen':'f', 'form_num':'s', 'num': 'p', 'rat': 'i'}, 
        ])
    '''

    map_driver = driver.setup_driver(tagset)
    
    output_dict = convert(input_tag, map_driver)

    print(output_dict)