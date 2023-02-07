import convert_from, convert_to, EMADA
from tools import read

def main():
    map_driver = read.read_map("MADA_to_EMADA")

    with open("./data/parallel/BW_MADA.par", "r") as f:
        count, true_count, error_count, false_count = 0, 0, 0, 0
        flag = False

        for line in f:
            count += 1
            bw_tag, mada_tag = line.strip().split(",")

            output_tags = convert("BW", "MADA", bw_tag)
            
            if output_tags == None:
                error_count += 1
                with open("error_log.txt", 'a') as f:
                    f.write(f"Error in converting tag: {bw_tag}\n")
            
            else:
                matches = convert_to.findAllMatches(mada_tag, map_driver)
                expected = [convert_to.extractFeats(map_driver, match) for match in matches]
                print(bw_tag)
                print(f"OUTPUT:\t{output_tags}")
                print(f"EXPECTED:\t{expected}")
                flag = False
                for tag in output_tags:
                    if output_matches(tag, expected):
                        true_count += 1
                        flag = True
                        #print("H")
                        break
                
                if not flag:
                    false_count += 1

            if count % 10 == 0:
                print(count)
                return

        print(count)
        print(true_count + false_count)
        print(true_count / (true_count + false_count), false_count / (true_count + false_count))
        return
    
def output_matches(output, expected):
    for feat, val_list in output.items():
        flag = False

        for val in val_list:
            for tag in expected:
                if tag[feat]==val:
                    flag = True
        
        if not flag:
            return False
    
    return True

def convert(src, trgt, input_tag):
    map = f"{src}_to_EMADA"
    #input_tag = "Asm/NOUN+hA/POSS_PRON_3FS"

    intermediate_tags = convert_to.main(map, input_tag)
    if intermediate_tags == None:
        return None
    
    map = f"{trgt}_to_EMADA"
    output_tags = []
    for tag in intermediate_tags:
        output = convert_from.main(map, tag)
        if output != None:
            output_tags += output
        else:
            return None

    return output_tags
    #print(output_tags)

if __name__ == "__main__":
    with open("mismatch_log.txt", "w") as f:
        pass
    main()