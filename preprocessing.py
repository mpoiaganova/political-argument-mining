def do2 (filename1, filename2):

    with open(filename1, 'rb') as f:
        doc = load_cas_from_xmi(f, typesystem=typesystem)

    #custom.Span

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
    df_ds.to_csv(filename2 + 'comps' + '.csv', index=False)
    
    df = pd.DataFrame({key: pd.Series(val) for key, val in d_db.items()}).T
    df['Sent'] = list(d_db.keys())
    df.to_csv(filename2 + '.csv', index=True)
    

    return df_ds, df
