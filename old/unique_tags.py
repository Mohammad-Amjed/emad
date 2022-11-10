import re
from pprint import pprint

from camel_tools.utils.charmap import CharMapper
from camel_tools.utils.transliterate import Transliterator

bw2ar_translit = Transliterator(CharMapper.builtin_mapper('bw2ar'))

input_file = "./data/ATB123-train.almor-msa-s31.calima-msa-s31_0.4.2"
output_file = f"{input_file}.uniq.ex.txt"

def main():
    tags = read_tags()
    write_results(tags)


def find_word(section):
    word_line = re.findall(";;WORD .*\n", section)
    return word_line[0].strip().split()[1]

def find_tag(section):
    tag_line = re.findall("\n\\*.*\n", section)
    tag = re.findall("pos:.*rat:[^ ]*", tag_line[0])
    return tag[0]

def read_tags():

    tags = {}

    with open(input_file, "r") as f:
        sections = f.read().split("--------------\n")
        for sec in sections:
            if "SENTENCE BREAK" not in sec and sec.strip() != "":
                word = find_word(sec)
                tag = find_tag(sec)

                if tag in tags:
                    if word in tags[tag]:
                        tags[tag][word] += 1
                    else:
                        tags[tag][word] = 1
                else: 
                    tags[tag] = {}
                    tags[tag][word] = 1

    return tags

def write_results(tags):
    with open(output_file, "w") as f:
        for tag in sorted(tags.keys()):
            f.write(tag)
            f.write(" ")
            max_word = max(tags[tag], key=tags[tag].get)
            f.write(f"ex:{max_word}|{bw2ar_translit.transliterate(max_word)} ")

            count = sum([i for i in tags[tag].values()])
            f.write(f"cnt:{count}")
            f.write("\n")

if __name__ == "__main__":
    main()