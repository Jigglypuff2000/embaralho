"""Verifica os dict-xx.json publicados contra tools/dict_tests.json e a regra de comprimento (>=3 letras)."""
import json,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from dictread import load
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T=json.load(open(os.path.join(root,'tools','dict_tests.json'),encoding='utf-8'));bad=0
for lang in ['pt','en','es','fr','de','it']:
    d=load(os.path.join(root,f'dict-{lang}.json'))
    short=[w for w in d if len(w)<3]
    if short:bad+=1;print(f'[{lang}] palavras com menos de 3 letras:',short[:10])
    t=T.get(lang)
    if not t:continue
    for w,why in t['aceitar'].items():
        if w not in d:bad+=1;print(f'[{lang}] FALHOU aceitar {w!r} ({why})')
    for w,why in t['rejeitar'].items():
        if w in d:bad+=1;print(f'[{lang}] FALHOU rejeitar {w!r} ({why}) nível={d[w][0]}')
    for w,f in t.get('exibir',{}).items():
        if w in d and d[w][1]!=f:bad+=1;print(f'[{lang}] FALHOU grafia {w!r}: {d[w][1]!r} != {f!r}')
# colisao: palavra rejeitada cuja forma sem acento coincide com uma conjugação válida (faco = faço)
import unicodedata
_n=lambda x:''.join(c for c in unicodedata.normalize('NFD',x) if unicodedata.category(c)!='Mn').replace('ç','c')
_cj=os.path.join(root,'tools','conj_pt.txt')
if os.path.exists(_cj):
    CJ={_n(w) for w in open(_cj,encoding='utf-8').read().split()}
    for w in T['pt']['rejeitar']:
        if w in CJ and w not in T['pt'].get('colisao_ok',{}):bad+=1;print(f'[pt] colisão: {w!r} rejeitada mas é forma verbal sem acento')
print('OK' if not bad else f'{bad} falha(s)');sys.exit(1 if bad else 0)
