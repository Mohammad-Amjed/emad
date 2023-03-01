import convert_from, convert_to, EMADA
from tools import read

def main():
    input = "MADA"
    output = "BW2"
    tags ={}

    output_map_driver = read.read_map(f"{output}_to_EMADA")
    output_map_driver_rev = read.read_map_rev(f"{output}_to_EMADA")
    input_map_driver = read.read_map(f"{input}_to_EMADA")

    with open("./data/parallel/BW_MADA_atb.par", "r") as f:
        count, true_count, error_count, false_count = 0, 0, 0, 0
        flag = False

        for i, line in enumerate(f):
            #print(line)
            if not line[0] ==',': # quick solution to ignore if the token is ","
                count += 1
                tags["BW2"], tags["MADA"], tags["CATiB6"] = line.strip().split(",")
            else:
                continue
        
            output_tags = convert(input, output, tags[input], input_map_driver, output_map_driver_rev)
            
            if output_tags == None:
                error_count += 1
                with open("error_log.txt", 'a') as f:
                    f.write(f"Error in converting tag: {tags[input]}\n")
            
            else:
                matches = convert_to.findAllMatches(tags[output], output_map_driver)
                #print(mada_tag)
                expected = [convert_to.extractFeats(output_map_driver, match) for match in matches]
                #print(bw_tag)
                #print(f"OUTPUT:\t{output_tags}")
                #print(f"EXPECTED:\t{expected}")
                flag = False
                for tag in output_tags:
                    if output_matches(tag, expected):
                        true_count += 1
                        flag = True
                        #print("H")
                        break
                
                if not flag:
                    false_count += 1
                    with open("mismatch_log.txt", 'a') as f:
                        f.write(f"Error in converting tag: {tags[input]}\n")
                        f.write(f"expected: {tags[output]}\n")
                        
                        f.write("feature")
                        f.write("\t\texpected"*len(expected))
                        f.write("\t\toutput"*len(output_tags))
                        f.write("\n")

                        for feat in output_tags[0].keys():
                            f.write(f"{feat}\t\t")
                            for ex in expected:
                                if feat in ex:
                                    f.write(f"{ex[feat]}\t\t")
                                else:
                                    f.write("-\t\t")
                            
                            for out in output_tags:
                                if feat in out:
                                    f.write(f"{out[feat]}\t\t")
                                else:
                                    f.write("-\t\t")
                            f.write("\n")
                        f.write("----------------------------------------------\n")

            if count % 100 == 0:
                print(i, count)
                #print(tags["BW2"], tags["MADA"], tags["CATiB6"])
            
            if count == 10000:
                
                print(count)
                print(true_count + false_count)
                print()
                print(true_count / (true_count + false_count))
                print(false_count / (true_count + false_count))
                return
        
def output_matches(output, expected):
    for feat, val_list in output.items():
        flag = False

        for val in val_list:
            for tag in expected:
                if feat in tag:
                    if tag[feat]==val or val == "#VAL#" or (tag[feat] in ['na', 'no'] and val in ['na', 'no']):
                        flag = True
                    
                    #TODO quick fix
                    if feat == "RAT" and tag[feat] in ['na', 'no', 'n'] and val in ['na', 'no', 'n']:
                        flag = True
        
        if not flag:
            return False
    
    return True

def convert(src, trgt, input_tag, input_map_driver, output_map_driver):
    map = f"{src}_to_EMADA"
    #input_tag = "Asm/NOUN+hA/POSS_PRON_3FS"

    intermediate_tags = convert_to.main(map, input_tag, input_map_driver)
    if intermediate_tags == None:
        return None
    
    map = f"{trgt}_to_EMADA"
    output_tags = []
    for tag in intermediate_tags:
        output = convert_from.main(map, tag, output_map_driver)
        if output != None:
            output_tags += output
        else:
            return None

    return output_tags
    #print(output_tags)

if __name__ == "__main__":
    with open("mismatch_log.txt", "w") as f:
        pass
    with open("error_log.txt", "w") as f:
        pass
    main()