def Defaults(def_file):
        def_dict = {}
        with open(def_file) as f:
            for line in f:
                line = line.strip().split('\t')
                pos = line[0].split(':')[1]
                feat_val = [pair.split(':') for pair in line[1].split()]
                def_tag = {pair[0]:pair[1] for pair in feat_val}
                def_dict[pos] = def_tag

        return def_dict