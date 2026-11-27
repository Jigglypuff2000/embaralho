import re, sys, unicodedata
aff, dic, out = sys.argv[1:4]
rules = {}  # flag -> (type, cross, [(strip, add, cont, regex)])
for line in open(aff, encoding='utf-8'):
    p = line.split()
    if len(p) >= 4 and p[0] in ('PFX','SFX') and p[2] in ('Y','N') and p[3].isdigit() and len(p)==4:
        rules[p[1]] = (p[0], p[2]=='Y', [])
    elif len(p) >= 5 and p[0] in ('PFX','SFX') and p[1] in rules:
        strip = '' if p[2]=='0' else p[2]
        add = p[3]; cont=''
        if '/' in add: add, cont = add.split('/',1)
        if add=='0': add=''
        cond = p[4]
        rx = re.compile(('^'+cond) if p[0]=='PFX' else (cond+'$')) if cond!='.' else None
        rules[p[1]][2].append((strip, add, cont, rx))
def apply(word, flag):
    t, cross, ents = rules[flag]; res=[]
    for strip, add, cont, rx in ents:
        if rx and not rx.search(word): continue
        if t=='SFX':
            if strip and not word.endswith(strip): continue
            w = (word[:-len(strip)] if strip else word) + add
        else:
            if strip and not word.startswith(strip): continue
            w = add + (word[len(strip):] if strip else word)
        res.append((w, cont, cross))
    return res
def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    return ''.join(c for c in w if unicodedata.category(c)!='Mn')
words=set()
def add(w):
    if not w or not w[0].islower(): return
    n = w.lower()
    if 3 <= len(n) <= 16 and n.isalpha(): words.add(n)
lines = open(dic, encoding='utf-8').read().split('\n')[1:]
for line in lines:
    if not line.strip(): continue
    if '/' in line: stem, flags = line.split('/',1)
    else: stem, flags = line, ''
    flags = flags.split()[0] if flags.strip() else ''
    if 'ý' in flags: continue
    add(stem)
    sfx=[f for f in flags if f in rules and rules[f][0]=='SFX']
    pfx=[f for f in flags if f in rules and rules[f][0]=='PFX']
    sforms=[]
    for f in sfx:
        for w,cont,cross in apply(stem,f):
            add(w); sforms.append((w,cross))
            for c in cont:
                if c in rules and rules[c][0]=='SFX':
                    for w2,_,_ in apply(w,c): add(w2)
    for f in pfx:
        for w,cont,cross in apply(stem,f):
            add(w)
            if cross:
                for sw,scross in sforms:
                    if scross:
                        for w2,_,_ in apply(sw,f): add(w2)
open(out,'w').write('\n'.join(sorted(words)))
print(len(words))
