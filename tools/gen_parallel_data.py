from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.utils.charmap import CharMapper
from camel_tools.utils.transliterate import Transliterator

db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)
analyzer = Analyzer(db, 'NOAN_PROP')
analyzer = Analyzer(db, backoff='NOAN_PROP')

bw2ar = CharMapper.builtin_mapper('bw2ar')
bw2ar_translit = Transliterator(bw2ar)

with open('./data/parallel/BW_MADA.par', "w") as outFile:
    with open('./data/MADA_grammar/ATB123-train.almor-msa-s31.calima-msa-s31_0.4.2', 'r') as inFile:
        for line in inFile:
            if line.startswith(";;WORD"):
                word = line.strip().split(' ')[1]
                
                analyses = analyzer.analyze(bw2ar_translit.transliterate(word))
                if len(analyses) > 0:
                    a = analyses[0]
                    outFile.write(a['bw'])
                    outFile.write(',')
                    for feat in ['diac', 'lex', 'pos', 'prc3', 'prc2', 'prc1', 'prc0', 'per', 'asp', 'vox', 'mod', 'gen', 'form_gen', 'num', 'form_num', 'stt', 'cas', 'enc0', 'rat']:
                        if feat in ['form_gen']:
                            outFile.write(f"fgen:{a[feat]}")
                        elif feat in ['form_num']:
                            outFile.write(f"fnum:{a[feat]}")
                        else:
                            outFile.write(f"{feat}:{a[feat]}")
                        
                        outFile.write(' ')
                    
                    outFile.write('\n')
