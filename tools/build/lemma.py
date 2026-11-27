import sys,json,re,unicodedata,collections,pickle
exec(open('/home/claude/build/expand.py').read().split("words=set()")[0].replace("aff, dic, out = sys.argv[1:4]","aff='/home/claude/dl/pt/package/index.aff'"))
def nrm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn').replace('ç','c')
L=collections.defaultdict(set)
for line in open('/home/claude/dl/pt/package/index.dic',encoding='utf-8').read().split('\n')[1:]:
    if not line.strip():continue
    st,fl=(line.split('/',1)+[''])[:2];fl=fl.split()[0] if fl.strip() else ''
    if not st or not st[0].islower() or '-' in st:continue
    L[nrm(st)].add(st)
    for f in fl:
        if f in rules and rules[f][0]=='SFX':
            for w,cont,_ in apply(st,f):
                L[nrm(w)].add(st)
                for c in cont:
                    if c in rules and rules[c][0]=='SFX':
                        for w2,_,_ in apply(w,c):L[nrm(w2)].add(st)
pickle.dump(dict(L),open('/tmp/ptbr/lemmas.pkl','wb'))
print(len(L))
