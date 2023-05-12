from tools import read

CATEGORIES = ['PRC_QUES', 'PRC_CONJ', 'PRC_PREP', 'PRC_VPAR', 
              'PRC_DET', 'BASE', 'ENC_PRON', 'ENC_PART']

FEATURES = ['lex', 'pos', 'per', 'asp', 'cas', 'stt', 'mod', 
            'vox', 'form_gen', 'gen', 'form_num', 'num', 'rat']

# TODO add the pos:* to defaults file, or figure out why I didn't include it before
DEFAULTS = read.Defaults("./config/defaults.txt")

class Subtag(dict):
    def __init__(self, input_dict=None):
        if input_dict is None:
            input_dict = {}
        
        for k in FEATURES:
            self[k] = input_dict[k] if k in input_dict else '-1'

    def addDefaults(self):
        pos = self['pos']
        if pos in DEFAULTS:
            for feat in self:
                if self[feat] == '-1':
                    self[feat] = DEFAULTS[pos][feat]
        elif pos != '-1':
            print(f"Error: pos {pos} not found in the defaults list")
        
    def __eq__(self, object):
        if object == None:
            return False
        
        for key in self:
            if key not in object:
                return False
            
            if self[key] != object[key]:
                return False
        
        return True

    def __ne__(self, object):
        if object == None:
            return True
        
        return not self == object
    
class Tag(dict):
    def __init__(self, input = None):
        for cat in CATEGORIES:
            if input and cat in input and input[cat] != None:
                self[cat] = Subtag(input[cat]) if input and cat in input.keys() else None
            else:
                self[cat] = None
        
    def addDefaults(self):
        for subtag in self.values():
            if subtag:
                subtag.addDefaults()

    def __len__(self):
        return sum(0 if self[cat] is None else 1 for cat in CATEGORIES)

    def __str__(self):
        string = ""

        if len(self) > 0:
            COL_W = 14
            COL_SP = 3
            string += " "*COL_W 

            for cat in CATEGORIES:
                if self[cat]:
                    string += " "*COL_SP
                    string += cat
                    string += " "*(COL_W - len(cat))

            for feat in FEATURES:
                string += '\n'
                string += f'{feat:<{COL_W}}'
                for subtag in self.values():
                    if subtag != None:
                        string += " "*COL_SP
                        string += f'{subtag[feat]:<{COL_W}}'

        return string

    def __eq__(self, object):
        return all(self[cat] == object[cat] for cat in CATEGORIES)

    def __ne__(self, object):
        return not self == object

'''
test = {'pos': 'noun', 'gen': 'm'}
test2 = {'pos': 'noun', 'gen': 'f'}
test_sub = Subtag(test)
test_sub2 = Subtag(test2)

test_tag = Tag({"BASE":test_sub, "ENC_PRON":test_sub2})
test_tag.addDefaults()
print(test_tag)

test_tag2 = Tag({"BASE":test_sub, "ENC_PRON":test_sub2})
print(test_tag2)

print(test_tag == test_tag2)
'''