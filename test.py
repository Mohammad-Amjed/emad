import re, json
from pprint import pprint

map_dir = "./mappings"
src = "MADA_to_EMADA.json"

with open(f"{map_dir}/{src}", 'r') as f:
        map_driver = json.load(f)

#pprint(map_driver["map"])
with open("test.txt") as f:
    for line in f:
        if line !="\n":
            line = line.strip().split(":")[1]
            for key in map_driver["map"]['ENC0'][line]['5']:
                print(key, map_driver["map"]['ENC0'][line]['5'][key], end = " ")
        print()