''' this file contains two functions for retrieving Inception annotations in .xmi format, 
comparing them to full sentences and returning a ready-to-use dataset '''

#imports 
import re
import pandas as pd
import nltk
nltk.download('punkt')
from nltk import tokenize

# cassis lib to work with Inception annotations
!pip install dkpro-cassis > /dev/null
from cassis import *


#loading TypeSystem framework just once
with open('TypeSystem.xml', 'rb') as f:
  typesystem = load_typesystem(f)


#main function 
def ann2df (filename1, filename2):
    
    '''
    Function 
    Create two dataframes and save to respective .csv with columns:
    1) [Sentence] - full sentence of text; Label - the label of a sentence. 
    For sentences with both a premise and a claim, the function calculates length of a span in terms of its elements' number and selects the longest.
    For sentences with e.g., two claims and one premise, the function sums up the lengths of all represented components and annotates according to the longest one.
    [Label] - none, claim or premise 
    [Components] - a dict for each sentence, representing components, their label and their lengths 
    2) [Component] - annotated span - argumentative component.
    [Label] - claim or premise 
    
    Input
    filename1: .xmi file loaded from Inception
    filename2: .txt respective text 
    
    Output
    main df with columns Sentence, Label, Components 
    + two .csv files are saved in the local folder
    
    '''

    with open(filename1, 'rb') as f:
        doc = load_cas_from_xmi(f, typesystem=typesystem)

    #custom.Span

    with open('output.txt', 'w') as f:
        for segment in doc.select('custom.Span'):
            f.write(f"{segment.get_covered_text()}\t{segment.label}\n")

    with open('output.txt') as f:
        lines = f.readlines()

    with open(filename2) as f:
        lines2 = f.readlines()

    sents = []
    for p in lines2:
        sents.extend(tokenize.sent_tokenize(p))

    l_sent = []
    l_label = []
    l_label_clear = []

    for i in lines:
        s = {}
        i = i.split('\t')
        l_sent.append(i[0])
        l_label_clear.append(i[1][:-1])
        s[i[1][:-1]] = len(i[0])
        l_label.append(s)


    d = {}

    for i in sents:
        a = {'claim': 0, 'premise': 0}
        for ind, l in enumerate(l_sent):
            if l in i:
                try:
                    a['premise'] += l_label[ind]['premise']
                except:
                    a['claim'] += l_label[ind]['claim']
        if max(list(a.values())) == 0:
            d[i] = 'none'
        else:
            d[i] = max(a, key = a.get)

    dict_clear = dict(zip(l_sent, l_label_clear))

    d_db = {}

    for k, v in d.items():
        a = []
        a.append(v)
        d_db[k] = a
        val_dict = {}
        a.append(val_dict)
        for x, y in dict_clear.items():
            if x in k:
                val_dict[x] = [y, len(x)]
    
    ds = dict(zip(lines, l_label_clear))
    df_ds = pd.DataFrame.from_dict(ds.items())
    df_ds.columns=['Component', 'Label']
    df_ds.to_csv(filename2[:-4] + '_comp' + '.csv', index=False)
    
    
    df = pd.DataFrame({key: pd.Series(val) for key, val in d_db.items()}).T
    df.columns=['Label', 'Components']
    df['Sentence'] = list(d_db.keys())
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.to_csv(filename2[:-4] + '.csv', index=False)


    return df


'''
Adaptation of the former function but for texts which were incorrectly fragmented in the .txt format. 

'''

def ann2df_adapted (filename1, filename2):

    with open(filename1, 'rb') as f:
        doc = load_cas_from_xmi(f, typesystem=typesystem)

    with open('output.txt', 'w') as f:
        for segment in doc.select('custom.Span'):
            f.write(f"{segment.get_covered_text()}\t{segment.label}\n")

    with open('output.txt') as f:
        lines = f.readlines()


    string_cl = ' '.join(lines)
    string_cl = string_cl.replace('\n', '')


    lines_re = re.split('\\tclaim |\\tpremise ', string_cl)
    ann_re = re.findall('\\tclaim|\\tpremise', string_cl)


    new_lines_ann = []
    for ind, x in enumerate(lines_re):
        if ann_re[ind] in x:
            str_new = x.replace(ann_re[ind], '')
            str_new = str_new + ' ' + ann_re[ind]
        else:
            str_new = x + ' ' + ann_re[ind]
        new_lines_ann.append(str_new)

    lines = new_lines_ann

    with open(filename2) as f:
        lines2 = f.readlines()

    string = ''.join(lines2)
    string = string.replace('\n', ' ')
    se = tokenize.sent_tokenize(string)

    l_sent = []
    l_label = []
    l_label_clear = []

    for i in lines:
        s = {}
        i = i.split('\t')
        l_sent.append(i[0])
        l_label_clear.append(i[1])
        s[i[1]] = len(i[0])
        l_label.append(s)

    ll_sent = []
    for l in l_sent:
        ll_sent.append(l[:-1])

    
    d = {}

    for i in se:
        a = {'claim': 0, 'premise': 0}
        for ind, l in enumerate(ll_sent):
            if l in i:
                try:
                    a['premise'] += l_label[ind]['premise']
                except:
                    a['claim'] += l_label[ind]['claim']
        if max(list(a.values())) == 0:
            d[i] = 'none'
        else:
            d[i] = max(a, key = a.get)

    dict_clear = dict(zip(ll_sent, l_label_clear))

    d_db = {}

    for k, v in d.items():
        a = []
        a.append(v)
        d_db[k] = a
        val_dict = {}
        a.append(val_dict)
        for x, y in dict_clear.items():
            if x in k:
                val_dict[x] = [y, len(x)]


    ds = dict(zip(lines, l_label_clear))
    df_ds = pd.DataFrame.from_dict(ds.items())
    df_ds.columns=['Component', 'Label']
    df_ds.to_csv(filename2[:-4] + '_comp' + '.csv', index=False)
    
    df = pd.DataFrame({key: pd.Series(val) for key, val in d_db.items()}).T
    df.columns=['Label', 'Components']
    df['Sentence'] = list(d_db.keys())
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.to_csv(filename2[:-4] + '.csv', index=False)
    

    return df
  
  
print("test")
