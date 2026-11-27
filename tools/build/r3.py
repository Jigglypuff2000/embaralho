import sys,json,re,unicodedata,collections,random
sys.path.insert(0,'/home/claude/embaralho/tools')
from dictread import load
def nrm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn').replace('ç','c')
d=load('/home/claude/embaralho/dict-pt.json')
DLc=collections.defaultdict(set)
for l in open('/home/claude/dl/unitex/delas.txt',encoding='utf-8'):
    if ',' in l:
        w,c=l.strip().split(',',1);DLc[nrm(w)].add('PR' if '+Pr' in c else re.match(r'[A-Z]+',c).group(0))
conj={nrm(x) for x in open('/home/claude/dl/conjug',encoding='utf-8').read().split()}
new=set(json.load(open('/tmp/vb/new.json')))
icf=set()
for l in open('/home/claude/dl/icf',encoding='utf-8'):icf.add(nrm(l.strip().rpartition(',')[0]))
src=open('/home/claude/build/ptbuild.py',encoding='utf-8').read()
FUNC={nrm(x) for x in src.split("FUNC=set('''")[1].split("'''")[0].split()}
T=json.load(open('/home/claude/embaralho/tools/dict_tests.json'))['pt']
def sing(n):
    c={n}
    if n.endswith('s'):c.add(n[:-1])
    if n.endswith('es'):c.add(n[:-2])
    for a,b in [('oes','ao'),('aes','ao'),('ais','al'),('eis','el'),('ois','ol'),('ns','m'),('is','il'),('a','o'),('as','o'),('as','os')]:
        if n.endswith(a):c.add(n[:-len(a)]+b)
    return c
def common(n):return any(DLc.get(x,set())-{'PR'} for x in sing(n))
def verb(n):return n in conj or n in new
PN=re.compile(r'(ismo|ista|ian[oa]|ense|ita|áce[oa]|íase|ose|ímetro|agem|ístic[oa]|ês|esa|ianismo|ianista|ido)s?$')
KEEP=set('volt volts watt watts kelvin kelvins quilowatt quilowatts megawatt megawatts déficit déficits superávit habitat habitats hein'.split())
def foreign(f):
    n=nrm(f);acc=f!=n.replace('c','c') and any(ch in f for ch in 'áéíóúâêôãõà')
    if f in KEEP:return False
    if PN.search(f) and re.search(r'[kwy]|sh|th|ph|ck|ll|tt|ff|pp|bb|dd|gg|mm|nn',n):return False
    if re.search(r'[kwy]',n):return True
    if re.search(r'sh|th|ph|ck|ll|tt|ff|pp|bb|dd|gg|mm|nn|ss$',n):return True
    if re.search(r'[bcdfghjpqtv]$',n):return True
    if re.search(r'[aiou]n$',n) and not acc:return True
    if re.search(r'[bcdfgkqtv]s$',n):return True
    return False
R={}
R['estrangeiro']=sorted((dv or n) for n,(lv,dv) in d.items() if foreign(dv or n) and not verb(n) and n not in FUNC)
R['estrangeiro']+= [x for x in ['nurse','nurses','toner','toners'] if x in d]
LET='efe efes agá agás jota jotas ípsilon ípsilons dáblio dáblios xis bês cês gês tês zês ués quês erres'.split()
R['letras']=[w for w in LET if nrm(w) in d and not verb(nrm(w)) and nrm(w) not in FUNC]
R['proprio']=sorted((dv or n) for n,(lv,dv) in d.items() if any('PR' in DLc.get(x,set()) for x in sing(n)) and not common(n) and not verb(n) and n not in FUNC)
R['pt']=[x for x in ['ecra','ecras'] if x in d]
R['oa']=sorted((dv or n) for n,(lv,dv) in d.items() if re.search(r'oas?$',n) and (n[:-2] if n.endswith('oa') else n[:-3])+'ao' in d and n not in icf and not verb(n) and not common(n))
for k,v in R.items():print(k,len(v),v if len(v)<400 else v[:400]);print()
json.dump(R,open('/tmp/cl/r3.json','w'),ensure_ascii=False)
