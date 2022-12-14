FEATURES = ['orth', 'lex', 'pos', 'per', 'asp', 'cas', 'stt', 'mod', 
            'vox', 'form_gen', 'gen', 'form_num', 'num', 'rat']

def readDefaults(def_file):
        def_dict = {}
        with open(def_file) as f:
            for line in f:
                line = line.strip().split('\t')
                pos = line[0].split(':')[1]
                feat_val = [pair.split(':') for pair in line[1].split()]
                def_tag = {pair[0]:pair[1] for pair in feat_val}
                def_dict[pos] = def_tag

        return def_dict

DEFAULTS = readDefaults("./mappings/defaults.txt")

class Subtag(dict):
    def __init__(self, input_dict = {'pos': '*'}):
        for k in FEATURES:
            if k in input_dict:
                self[k] = input_dict[k]
            else:
                self[k] = '-1'
        
        if self['pos'] == '-1':
            self['pos'] = "*"

    def addDefaults(self):
        pos = self['pos']
        if pos not in DEFAULTS:
            print(f"Error: pos {pos} not found in the defaults list")
        else:
            for feat in self:
                if feat != 'orth' and self[feat] == '-1':
                    self[feat] = DEFAULTS[pos][feat]

    def __eq__(self, object):
        for key in self:
            if key not in object:
                return False
            
            if self[key] != object[key]:
                return False
        
        return True

    def __ne__(self, object):
        return not self == object
    
class Tag(list):
    def __init__(self, input = None):
        if input:
            for stag in input:
                self.append(Subtag(stag))
    
    def addDefaults(self):
        for subtag in self:
            subtag.addDefaults()

    def __str__(self):
        string = ""
        COL_W = 10
        COL_SP = 3
        string += " "*COL_W 

        for i in range(len(self)):
            string += " "*COL_SP
            string += f'SUBTAG {i:<{COL_W-7}}'

        for feat in FEATURES:
            string += '\n'
            string += f'{feat:<{COL_W}}'
            for subtag in self:
                string += " "*COL_SP
                string += f'{subtag[feat]:<{COL_W}}'

        return string

    def __eq__(self, object):
        if len(self) != len(object):
            return False
        
        for sub1, sub2 in zip(self, object):
            if sub1 != sub2:
                return False
        
        return True

    def __ne__(self, object):
        return not self == object