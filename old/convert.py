import re, json

map_dir = "./mappings"
src = "camel.map.json"
input_tag = "PART_CONNECT+ADJ.MS+PRON"

def main():
    with open(f"{map_dir}/{src}", 'r') as f:
        map_driver = json.load(f)

    src_format = compileRE(map_driver)

    m = src_format.match(input_tag)

    src_feats = extractFeats(map_driver, m)

    trg_feats = convertFeats(src_feats, map_driver)

    print(trg_feats)

def compileRE(map_driver):
    i = 1
    src_format = map_driver["format"]

    while True:
        if src_format.find(f"GRP{i}") != -1:
            group = map_driver["groups"][i - 1]
            name = group["name"]
            options = "|".join(list(group["map"].keys()))

            src_format = src_format.replace(f"GRP{i}", f"(?P<{name}>{options})", 1)
        else:
            break
        i += 1
    #print(src_format)
    return re.compile(src_format)

def extractFeats(map_driver, match):
    feats = {}
    for group in map_driver['groups']:
        name = group['name']
        if match.group(name):
            feats[name] = match.group(name)

    return feats

def convertFeats(src_feats, map_driver):
    trg_feats = {}
    for feat in src_feats.keys():
        for group in map_driver['groups']:
            if group['name'] == feat:
                trg_feats[group['mapsto'][0]] = group['map'][src_feats[feat]]
    
    return trg_feats

if __name__ == "__main__":
    main()