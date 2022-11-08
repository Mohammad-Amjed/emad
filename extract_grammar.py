import copy
from pprint import pprint

input_files = [ "./data/ATB123-train.almor-msa-s31.calima-msa-s31_0.4.2.uniq.ex.txt",
                "./data/additions.txt"]

output_name = "grammar_reduced_ex"

cnt_ex_bool = True

exclude_features = ["prc3", "prc2", "prc1", "prc0", "form_gen", "form_num", "enc0", "num", "gen", "rat"]
#exclude_tags = []
priority_features = ["per", "cas", "stt", "mod"]
#priority_features = []

def readdata(file_name):
    features = []
    tags = []

    with open(file_name, "r") as file:
        lines = file.readlines()
        
        #get names of the features from the file, except those in the execlude_feature list
        features = [i.split(":")[0] for i in lines[0].strip().split() if i.split(":")[0] not in exclude_features]
        
        for line in lines:
            line = line.strip().split()
            tags.append([i.split(":")[1] for i in line if i.split(":")[0] not in exclude_features])

    return features, tags

def make_unique(tags):
    unique_tags = []
    cnt_ex = []

    if cnt_ex_bool:
        for tag in tags:
            if tag[:-2] not in unique_tags:
                unique_tags.append(tag[:-2])
                cnt_ex.append(tag[-2:])
        
        n_unique_tags = [unique_tags[i] + cnt_ex[i] for i in range(len(unique_tags))]
            
        return n_unique_tags
    else:
        for tag in tags:
            if tag not in unique_tags:
                unique_tags.append(tag)

        return unique_tags

def write_results(file_name, features, tags, format):
    if len(features) != len(tags[0]):
        print("error in writing to file!")
        return
    
    else:
        with open(f"./output/{file_name}.{format}", "w") as f:
            if format == "csv":
                f.write(",".join(features))
                f.write("\n")

            for tag in tags:
                if format == "txt":
                    f.write(" ".join([f"{feat}:{val}" for feat,val in zip(features, tag)]))
                if format == "csv":
                    f.write(",".join(tag))
                f.write("\n")

# check if two tags are exactly the same, execpt for one feature which is indicated by the feat_id
def tags_similar(tag1, tag2, feat_id):
    if len(tag1) != len(tag2) or feat_id >= len(tag1):
        return False
    
    num_feats = len(tag1)-2 if cnt_ex_bool else len(tag1)
    for i in range(num_feats):
        if i != feat_id and tag1[i] != tag2[i]:
            return False
    
    return True

# merge two values of a certain feature in a tag
def merge_values(val1, val2):
    l1 = val1.split("|")
    l2 = val2.split("|")
    merged = list(set(l1 + l2))
    merged.sort()
    return "|".join(merged)

# merge two tags by merging the value of one feature specified by feat_id
def merge_tags(tag1, tag2, feat_id):
    merged = copy.deepcopy(tag1)
    merged[feat_id] = merge_values(tag1[feat_id], tag2[feat_id])
    
    if cnt_ex_bool:
        merged[-1] = str(int(tag1[-1]) + int(tag2[-1]))
        merged[-2] = tag1[-2] if tag1[-1]>tag2[-1] else tag2[-2]

    return merged

# collapse all tags using a single feature
def collapse_tags(tags, feature):
    feat_id = features.index(feature)
    new_tags = []
    used = []

    for i in range(len(tags)):
        tag1 = tags[i]
        if tag1 not in used:
            for j in range(i + 1, len(tags)):
                tag2 = tags[j]

                if tags_similar(tag1, tag2, feat_id):
                    tag1 = merge_tags(tag1, tag2, feat_id)
                    used.append(tag2)
            
            new_tags.append(tag1)
    
    return new_tags

tags = []

for file in input_files:
    features, returned_tags = readdata(file)
    tags = tags + returned_tags

print(len(tags))
#print(features)
#print(tags[5])

print("making unique")
unique_tags = make_unique(tags)

new_tags = copy.deepcopy(unique_tags)
print(len(new_tags))

'''
feat = "pos"
print(feat)
new_tags = collapse_tags(new_tags, feat)
print(len(new_tags))'''

for feat in priority_features:
    print(feat)
    new_tags = collapse_tags(new_tags, feat)
    print(len(new_tags))

for feat in features[::-1]:
    if feat not in priority_features and feat not in ["ex", "cnt"]:
        print(feat)
        new_tags = collapse_tags(new_tags, feat)
        print(len(new_tags))

write_results(output_name, features, new_tags, "csv")
write_results(output_name, features, new_tags, "txt")
