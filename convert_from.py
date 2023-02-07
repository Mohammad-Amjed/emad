from tools import read
import EMADA
import re
from pprint import pprint

def main(map, input_tag):
    map_driver = read.read_map_rev(map)
    
    ordered_tags = addOrder(input_tag, map_driver)
    if ordered_tags == []:
        return None
    #pprint(ordered_tags)
    output = []

    for tag in ordered_tags:
        feat_dict = output_feat_dict(tag, map_driver)
        #print(feat_dict)
        if feat_dict not in output:
            output.append(feat_dict)
        
        # output_tags = generate_output_tags(feat_dict, map_driver['format'])

        # #TODO this is a QUICK FIX, must be changed
        # for tag in output_tags:
        #     tag = re.sub("\\(|\\)|\\?|\\\\|#.{0,5}#", "", tag)
        #     tag = re.sub("^\\++", "", tag)
        #     tag = re.sub("\\++$", "", tag)
        #     tag = re.sub("\\++", "+", tag)
        #     if tag not in output:
        #         output.append(tag)
    
    return output

def addOrder(input_tag, map_driver):
    order_list = []

    bwo = int(map_driver['base_word_order'])
    mwo = int(map_driver['max_word_order'])

    for sub_tag in input_tag:
        order_list.append([])
        pos_val = sub_tag['pos']

        if sub_tag['orth'] == 'proc':
            order_range = range(0, bwo)
        elif sub_tag['orth'] == 'enc':
            order_range = range(bwo + 1, mwo + 1)
        elif sub_tag['orth'] == 'base':
            order_list[-1].append(bwo)
            continue
        else:
            print('Error: invalid orth value')
            continue

        for ord in order_range:

            for feat_comb in map_driver['map']:
                for feat_pair in feat_comb:
                    if int(feat_pair[0]) == ord and feat_pair[1] == 'pos' and feat_pair[2] == pos_val:
                        if subtag_compatible(sub_tag, feat_comb, ord):
                            if ord not in order_list[-1]:
                                order_list[-1].append(ord)

        if len(order_list[-1]) == 0:
            print(f"Error: subtag {sub_tag} is not compatible with the map")

    #print(order_list)
    ordered_tags = make_ordered_tags(input_tag, order_list)

    return ordered_tags

def make_ordered_tags(input_tag, order_list):
    #base case
    if len(order_list) == 1:
        ordered_tags = []
        for ord in order_list[0]:
            new_dict = {str(ord): input_tag[0]}
            ordered_tags.append(new_dict)
        return ordered_tags
    
    #general case
    ordered_tags = make_ordered_tags(input_tag[1:], order_list[1:])
    new_ordered_tags = []
    for ord in order_list[0]:
        for tag in ordered_tags:
            if order_can_be_inserted(ord, tag):
                new_dict = {str(ord): input_tag[0]}
                new_ordered_tags.append({**tag, **new_dict})
    
    return new_ordered_tags

def order_can_be_inserted(ord, tag):
    for tg_ord in tag:
        if int(ord) >= int(tg_ord):
            return False
    
    return True

def subtag_compatible(sub_tag, feat_comb, ord):
    for feat_pair in feat_comb:
        ft_ord, ft, ft_val = feat_pair
        if int(ft_ord) == ord:
            if sub_tag[ft] not in [ft_val, '-1', '*']:
                return False
    
    return True

def tag_compatible(ordered_tag, feat_comb):
    for ord, feat, val in feat_comb:
        if ord not in ordered_tag:
            return False
        
        if ordered_tag[ord][feat] not in ['-1', '*', val]:
            return False
    
    return True

def output_feat_dict(ordered_tag, map_driver):
    feat_dict = {}
    #print(ordered_tag)
    for feat_comb in map_driver['map']:
        #print('h')
        if tag_compatible(ordered_tag, feat_comb):
            out_feat, out_val = map_driver['map'][feat_comb]
            
            if out_feat not in feat_dict:
                feat_dict[out_feat] = []
            feat_dict[out_feat].append(out_val)
    
    return feat_dict

def generate_output_tags(feat_dict, output_format):
    #base case
    if len(feat_dict) == 1:
        output_tags = []
        for feat in feat_dict:
            for val in feat_dict[feat]:
                tag = output_format.replace(f"#{feat}#", val)
                output_tags.append(tag)
            return output_tags

    #general case
    feat = list(feat_dict.keys())[0]
    vals = feat_dict[feat]
    feat_dict.pop(feat)

    output_tags = generate_output_tags(feat_dict, output_format)
    new_output_tags = []

    for val in vals:
        for tag in output_tags:
            new_tag = tag.replace(f"#{feat}#", val)
            new_output_tags.append(new_tag)

    return new_output_tags

if __name__ == "__main__":
    map = "BW_to_EMADA"
    input_tag = EMADA.Tag([
        {'orth': 'proc', 'lex': 'Al', 'pos': 'part_det', 'per': 'na', 'asp': 'na', 'cas': 'na', 'stt': 'na', 'mod': 'na', 'vox': 'na', 'form_gen': 'na', 'gen': 'na', 'form_num': 'na', 'num': 'na', 'rat': 'na'},
        {'orth': 'base', 'per': 'na', 'asp': 'na', 'cas': 'a', 'stt': 'c', 'mod': 'na', 'vox': 'na', 'form_gen': 'm', 'gen': 'm', 'form_num': 's', 'num': 's', 'rat': 'i', 'pos': 'noun'}, 
        {'orth': 'enc', 'per': '1', 'asp': 'na', 'cas': 'g', 'stt': '*', 'mod': 'na', 'vox': 'na', 'form_gen': '*', 'gen': '*', 'form_num': '*', 'num': 's', 'rat': '*', 'pos': 'pron'}
        ])
    
    output_tags = main(map, input_tag)
    pprint(output_tags)