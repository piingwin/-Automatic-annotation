#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import glob
import nltk


def get_sentences(text):
    sentences = re.split(r'(?:[.]\s*){3}|[.?!\n]', text)
    return [x.strip() for x in sentences]

def there_finder():
    m = re.compile('(there(\'s|\'re|\s+was|\s+were|\s+is|\s+are))(.+)', flags=re.I)
    
    all_noun_forms = ('NN', 'NNS', 'NNP', 'NNPS')
    
    files = glob.glob("data for test coherence/*.txt")
    print(files)
    for file_name in files:
        i = 0
        with open (file_name, encoding = 'utf8') as one_file:
            file_content = one_file.read()
            sentences = get_sentences(file_content)
            for sentence in sentences:
                result = m.search(sentence)
                if result:
                    # в result.groups()[0] - лежит there + окончание, например there's
                    # в result.groups()[1] - лежит окончание  слова there, например 's
                    # в result.groups()[2] - лежит окончание  предложения
                    
                    there_tokens = nltk.word_tokenize(result.groups()[0])
                    # в there_tagged будет лежать [('there', 'EX'), ("'s", 'VBZ')]
                    there_tagged = nltk.pos_tag(there_tokens)


                    sentence_end_tokens = nltk.word_tokenize(result.groups()[2])
                    # в sentence_end_tagged будет лежать [('so', 'RB'), ('many', 'JJ'), ('dogs', 'NNS')]
                    sentence_end_tagged = nltk.pos_tag(sentence_end_tokens)

                    if sentence_end_tagged[0][1] in all_noun_forms:
                          if sentence_end_tagged[1][0] != 'there' or sentence_end_tagged[1][1] != 'IN' and sentence_end_tagged[2][1] != 'NN':
                                print(file_name, sentence) 
                                sentence_position = file_content.find(sentence)
                                print (sentence_position)
                                construction = result.groups()[0]
                                constr_position = sentence.find(construction)
                                print (constr_position)
                                start = sentence_position + constr_position
                                end = start + len(construction)
                                print (file_content[start:end])

                                file_name2 = file_name.split('.')[0] + '.ann'
                                with open (file_name2, encoding = 'utf-8') as f:
                                      file_content2 = f.read()
                                      print (start, end)

                                finded = re.findall('T(\d+)', file_content2)
                                finded2 = [int(x) for x in finded]
                                maxT = max(finded2)
                                print (maxT)
                                f1 = open('data for test coherence/esl_00231.ann', 'a')
                                f1.write('T508\tCoherence 1301 1310 \tthere are')

if __name__ == '__main__':
    there_finder()
