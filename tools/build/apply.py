import sys,json,re,unicodedata,collections,gzip,base64,random
sys.path.insert(0,'/home/claude/embaralho/tools')
from dictread import load
def nrm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn').replace('ç','c')
cat=json.load(open('/tmp/cl/cat.json'))
DLC=collections.defaultdict(set)
for l in open('/home/claude/dl/unitex/delas.txt',encoding='utf-8'):
    if ',' in l:
        w,c=l.strip().split(',',1)
        if '+Pr' not in c:DLC[nrm(w)].add(c[:1])
P='/home/claude/embaralho/dict-pt.json';d=load(P)
rm=set()
KEEPT={'freixo','fundao','boticas'}
rm|={n for n in cat['top'] if n not in KEEPT}
rm|={'argo','cerato','cronos','fox','siena'}&set(d)
KEEPE=set('internet intranet funk funkeiro funkeiros kardecismo kardecismos kardecista kartodromo kartodromos keynesianismo keynesianismos taylorismo taylorismos toyotismo toyotismos taiwanesa taiwanesas'.split())
for f in cat['est']:
    n=nrm(f)
    if n in KEEPE:continue
    if 'tion' in n and not re.search(r'[kwy]|sh|th|ph|ck|tt|ll|ff|pp|bb|dd|gg',n):continue
    if re.match(r'^ps',n) and not re.search(r'[kwy]|sh|th|ph|ck|tt|ll|ff|pp|bb|dd|gg|ing$|[bcdfgjkpqtvw]$',n):continue
    if n.startswith(('pneu','metionin')):continue
    rm.add(n)
ABS=re.compile(r'(ção|são|ções|sões|dade|dades|ismo|ismos|ista|istas|mento|mentos|ância|ência|ado|ada|ados|adas|ido|ida|idos|idas|al|ar|vel|ente|ante|oso|osa|or|ora|ês|esa|ivo|iva|ico|ica)$')
kept=[];gone=0
for f,suf,lv in cat['der']:
    n=nrm(f)
    if suf.startswith('on'):
        if n.startswith('tabelion'):continue
        rm.add(n);gone+=1;continue
    m=re.match(r'^(.*?)(z?)(inh|it)([oa])(s?)$',f)
    ok=False
    if m:
        st,z,_,g,pl=m.groups()
        cands=[st] if z else [st+'o',st+'a',st+'e',st]
        for b in cands:
            bn=nrm(b)
            if bn in d and d[bn][0]>=1 and 'N' in DLC.get(bn,()) and not ABS.search(b):ok=True;break
    if ok:kept.append(f)
    else:rm.add(n);gone+=1
T=json.load(open('/home/claude/embaralho/tools/dict_tests.json'))['pt']['aceitar']
rm-=set(T)
print('cidades',len([n for n in cat['top'] if n not in KEEPT]),'carros',5,'estrangeirismos',len([1 for f in cat['est'] if nrm(f) in rm]),'derivações',gone,'diminutivos mantidos',len(kept))
random.seed(1);print('mantidos (amostra):',random.sample(kept,60))
print('estrangeirismos removidos:',sorted(nrm(f) for f in cat['est'] if nrm(f) in rm))
for n in rm:d.pop(n,None)
out=[];prev=''
for w in sorted(d):
    k=0
    while k<len(prev) and k<len(w) and prev[k]==w[k] and k<40:k+=1
    v,dv=d[w];out.append(chr(48+k)+w[k:]+{0:'!',1:'',2:'*',3:'^'}[v]+('='+dv if dv else ''));prev=w
j=json.load(open(P,encoding='utf-8'));j['d']=base64.b64encode(gzip.compress('\n'.join(out).encode(),9)).decode();j['n']=len(d)
json.dump(j,open(P,'w'),ensure_ascii=False)
print('total',len(d))
