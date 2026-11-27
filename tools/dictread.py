"""Lê um dict-xx.json publicado (mesmo formato que o jogo decodifica em loadDict)."""
import json,base64,gzip,sys
def load(path):
    j=json.load(open(path,encoding='utf-8'))
    txt=gzip.decompress(base64.b64decode(j['d'])).decode('utf-8')
    words={};prev=''
    for l in txt.split('\n'):
        if not l:continue
        k=ord(l[0])-48;s=l[1:];v=1;dv=None
        if '=' in s:s,dv=s.split('=',1)
        if s.endswith('!'):v=0;s=s[:-1]
        elif s.endswith('*'):v=2;s=s[:-1]
        elif s.endswith('^'):v=3;s=s[:-1]
        prev=prev[:k]+s;words[prev]=(v,dv)
    return words
if __name__=='__main__':
    d=load(sys.argv[1])
    for w in sys.argv[2:]:print(w,d.get(w))
