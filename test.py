from tools import driver
from conv_to_EMAD import convert as convert_to_EMAD
from conv_from_EMAD import convert as convert_from_EMAD
import json
input_tag = "CONJ+IV3MP+IV+IVSUFF_SUBJ:MP_MOOD:SJ+CVSUFF_DO:2D"
bw_input = "IV3MP+I+VERB+IVSUFF_MOOD:+IVSUFF_SUBJ:3MP_MOOD:I+IVSUFF_SUBJ:MP_MOOD:I+NSUFF_MASC_PL"
tagset1 = "BW"
tagset2 = "CAMeL"
arrs = []
map_driver_1 = driver.setup_driver(tagset=tagset1)
map_driver_2 = driver.setup_driver(tagset=tagset2)
with open("full_verbs_mapping.txt", 'r') as infile:
    for line in infile:
        arr = json.loads(line.strip())
        arrs.append(arr)
with open("quran_verbs_connected.txt", "r") as vfile:
    verbs = vfile.readlines()
# EMAD_tags = convert_to_EMAD(input_tag=input_tag, map_driver=map_driver_1)
# EMAD_tags = [{"PRC_QUE": None, "PRC_CONJ": None, "PRC_PREP": None, "PRC_VPAR": None, "PRC_DET": None, "BASE": {"lex": "naEobudu", "pos": "verb", "per": "1", "asp": "i", "cas": "na", "stt": "na", "mod": "i", "vox": "a", "form_gen": "*", "gen": "*", "form_num": "p", "num": "p"}, "ENC_PRON": None, "ENC_PART": None}]
# print(dict)

# for tag in EMAD_tags:
#     print(tag)
#     output_tag = convert_from_EMAD(input_tag=tag, map_driver=map_driver_2)
    # print(output_tag)

with open("mada_quran.txt", "w") as outfile:
    for index, tag in enumerate(arrs):
        output_tag = convert_from_EMAD(input_tag=arrs[index][0], map_driver=map_driver_2)
        outfile.write(verbs[index] + json.dumps(output_tag) + "\n")
        print(output_tag)
        # for tag in tags:


