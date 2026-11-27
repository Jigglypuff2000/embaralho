import sys,json,re,unicodedata,collections,random
sys.path.insert(0,'/home/claude/embaralho/tools')
from dictread import load
exec(open('/tmp/cl/lists.py').read())
def nrm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn').replace('ç','c')
DL=set();DLA=collections.defaultdict(set)
for l in open('/home/claude/dl/unitex/delas.txt',encoding='utf-8'):
    if ',' in l:
        w,c=l.strip().split(',',1)
        if '+Pr' in c:continue
        DL.add(w);DLA[w].add(c)
DLN={nrm(x) for x in DL}
conj={nrm(x) for x in open('/home/claude/dl/conjug',encoding='utf-8').read().split()}
verbn=set(json.load(open('/tmp/vb/new.json')))
icf=set()
for l in open('/home/claude/dl/icf',encoding='utf-8'):icf.add(nrm(l.strip().rpartition(',')[0]))
src=open('/home/claude/build/ptbuild.py',encoding='utf-8').read()
FUNC={nrm(x) for x in src.split("FUNC=set('''")[1].split("'''")[0].split()}
T=json.load(open('/home/claude/embaralho/tools/dict_tests.json'))['pt']['aceitar']
d=load('/home/claude/embaralho/dict-pt.json')
def sing(n):
    c={n}
    if n.endswith('s'):c.add(n[:-1])
    if n.endswith('es'):c.add(n[:-2])
    for a,b in [('oes','ao'),('aes','ao'),('ais','al'),('eis','el'),('ois','ol'),('ns','m'),('is','il'),('a','o'),('as','o'),('as','os'),('ora','or'),('oras','or')]:
        if n.endswith(a):c.add(n[:-len(a)]+b)
    return c
def protected(n):return n in FUNC or n in T or n in conj or n in verbn or bool(sing(n)&DLN)
cat=collections.defaultdict(list)
# 1 topônimos de Portugal
for t in PT_TOP:
    n=nrm(t)
    if n in d and not protected(n):cat['top'].append(n)
# 2 marcas/modelos
for t in CARS:
    n=nrm(t)
    if n in d and not protected(n):cat['car'].append(n)
# 3 estrangeirismos
FOR=re.compile(r'[kwy]|sh|th|ph|ck|tt|ll|ff|pp|bb|dd|gg|nn|mm|ing$|tion|[bcdfgjkpqtvw]$|ou?gh|eau|^ps?[^aeiouhlr]')
for n,(lv,dv) in d.items():
    f=dv or n
    if FOR.search(n) and not protected(n):cat['est'].append(f)
# 4 derivações inventadas (sem lema brasileiro nem ocorrência no corpus)
DER=re.compile(r'(zinh[oa]s?|inh[oa]s?|zit[oa]s?|it[oa]s?|íssim[oa]s?|érrim[oa]s?|mente|bilidades?|ções|ção|mentos?|ão|ões|onas?|ad[oa]s?|dor(es)?|dora?s?|vel|veis|antes?|entes?|deir[oa]s?|ismos?|istas?|al|ais|oso|osa|osos|osas)$')
for n,(lv,dv) in d.items():
    f=dv or n
    if n in icf or protected(n):continue
    if any(x in icf for x in sing(n)):continue
    m=DER.search(f)
    if m and len(f)>=7:cat['der'].append((f,m.group(1),lv))
json.dump({k:v for k,v in cat.items()},open('/tmp/cl/cat.json','w'),ensure_ascii=False)
for k in ('top','car','est'):print(k,len(cat[k]),sorted(cat[k])[:400]);print()
print('der',len(cat['der']),collections.Counter(x[1] for x in cat['der']).most_common(30))
print(collections.Counter(x[2] for x in cat['der']))
random.seed(3);print(random.sample([x[0] for x in cat['der']],150))
print('der nivel>=1',random.sample([x[0] for x in cat['der'] if x[2]>=1],min(150,len([1 for x in cat['der'] if x[2]>=1]))))
