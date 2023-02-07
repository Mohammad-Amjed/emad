import re
from camel_tools.utils.charmap import CharMapper
from camel_tools.utils.transliterate import Transliterator

ar2bw = CharMapper.builtin_mapper('ar2bw')
ar2bw_translit = Transliterator(ar2bw)

input_path = "./data/gumar/magold/GA_10_nvls_dev.utf8.magold"

tags = []

with open(input_path, "r") as f:
    for line in f:
        if line[0] == "*":
            bw_tag = re.findall("\\s(bw:\\S+)", line)
            bw_tag = bw_tag[0][3:]

            mada_tag1 = re.findall("\\s(diac:\\S+ lex:\\S+)", line)
            mada_tag1 = ar2bw_translit.transliterate(mada_tag1[0])

            mada_tag2 = re.findall("\\s(pos:.+rat:\\S+)", line)
            mada_tag2 = re.sub(" enc1:\\S+ enc2:\\S+", "", mada_tag2[0])
            
            mada_tag = mada_tag1 + " " + mada_tag2

            tags.append((bw_tag, mada_tag))

output_path = "./data/parallel/BW_MADA.par"

with open(output_path, "w") as f:
    for tag in tags:
        f.write(f"{tag[0]},{tag[1]}\n")