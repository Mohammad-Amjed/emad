import re

input_path = "./data/MADA_grammar/ATB123-train.almor-msa-s31.calima-msa-s31_0.4.2"

tags = []

with open(input_path, "r") as f:
    for line in f:
        if line[0] == "*":
            bw_tag = re.findall("\\s(bw:\\S+)", line)
            bw_tag = bw_tag[0][3:]

            mada_tag1 = re.findall("\\s(diac:\\S+ lex:\\S+)", line)
            mada_tag2 = re.findall("\\s(pos:.+rat:\\S+)", line)
            mada_tag = mada_tag1[0] + " " + mada_tag2[0]

            catib6_tag = re.findall("\\s(catib6:\\S+)", line)
            catib6_tag = catib6_tag[0][7:]

            tags.append((bw_tag, mada_tag, catib6_tag))

output_path = "./data/parallel/BW_MADA_atb.par"

with open(output_path, "w") as f:
    for tag in tags:
        f.write(f"{tag[0]},{tag[1]},{tag[2]}\n")