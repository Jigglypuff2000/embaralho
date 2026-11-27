import re,sys,unicodedata,json,collections
exec(open('/home/claude/build/expand.py').read().split("words=set()")[0].replace("aff, dic, out = sys.argv[1:4]","aff='/home/claude/dl/pt/package/index.aff'"))
sys.path.insert(0,'/home/claude/embaralho/tools')
from dictread import load
def nrm(s):return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').replace('ç','c')
LV=set()
for l in open('/home/claude/dl/unitex/delas.txt',encoding='utf-8'):
    if ',' in l:
        w,c=l.strip().split(',',1)
        if c.startswith('V') and '+Pr' not in c: LV.add(w)
d=load(sys.argv[1])
E={'ar':'o as a amos ais am ei aste ou astes aram ava avas ávamos áveis avam ara aras áramos áreis arei arás ará aremos areis arão aria arias aríamos aríeis ariam e es emos eis em asse asses ássemos ásseis assem ar ares armos ardes arem ando ado ada ados adas ai',
   'er':'o es e emos eis em i este eu estes eram ia ias íamos íeis iam era eras êramos êreis erei erás erá eremos ereis erão eria erias eríamos eríeis eriam a as amos ais am esse esses êssemos êsseis essem er eres ermos erdes erem endo ido ida idos idas ei',
   'ir':'o es e imos is em i iste iu istes iram ia ias íamos íeis iam ira iras íramos íreis irei irás irá iremos ireis irão iria irias iríamos iríeis iriam a as amos ais am isse isses íssemos ísseis issem ir ires irmos irdes irem indo ido ida idos idas'}
E={k:set(v.split()) for k,v in E.items()}
def stems(st,cl):
    s={st}
    if cl=='ar':
        if st.endswith('c'):s.add(st[:-1]+'qu')
        if st.endswith('g'):s.add(st[:-1]+'gu')
        if st.endswith('ç'):s.add(st[:-1]+'c')
    else:
        if st.endswith('c'):s.add(st[:-1]+'ç')
        if st.endswith('g'):s.add(st[:-1]+'j')
        if st.endswith('gu'):s.add(st[:-2]+'g')
        if st.endswith('qu'):s.add(st[:-2]+'c')
    return s
para={}
for line in open('/home/claude/dl/pt/package/index.dic',encoding='utf-8').read().split('\n')[1:]:
    if '/' not in line:continue
    stem,fl=line.split('/',1);fl=fl.split()[0] if fl.strip() else ''
    if stem not in LV or stem[-2:] not in E or nrm(stem) not in d or 'ý' in fl:continue
    out=set()
    for f in fl:
        if f in rules and rules[f][0]=='SFX':
            for w,cont,_ in apply(stem,f):
                out.add(w)
                for c in cont:
                    if c in rules and rules[c][0]=='SFX':
                        for w2,_,_ in apply(w,c):out.add(w2)
    cl=stem[-2:];st=stem[:-2];ok=set()
    for w in out:
        for s in stems(st,cl):
            if w.startswith(s) and w[len(s):] in E[cl]:ok.add(w)
    para.setdefault(stem,set()).update(ok)
json.dump({k:sorted(v) for k,v in para.items()},open('/tmp/vb/para.json','w'),ensure_ascii=False)
print('verbos',len(para),'formas',sum(len(v) for v in para.values()))
for k in ['lanhar','parar','pelar','entrar','sobrar','comer','conformar','suar','estar','ser','ter','ler','dar','elar','aquelar','dessar','delir','ondar','desdar','antar','distar','atar']:print(k,[w for w in para.get(k,[]) if len(w)<=7][:40])
