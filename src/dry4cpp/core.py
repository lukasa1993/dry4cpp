from pathlib import Path
EXCLUDED={".git","build","dist","target","vendor",".venv","venv","node_modules"}
def discover(root, exts):
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts and not any(x in EXCLUDED for x in p.parts))

from dataclasses import dataclass,asdict
import re,hashlib
@dataclass
class Duplicate:
    first_file:str; first_line:int; second_file:str; second_line:int; tokens:int
def tokens(text):
    text=re.sub(r'/\*.*?\*/',' ',text,flags=re.S);text=re.sub(r'//[^\n]*',' ',text);text=re.sub(r'"(?:\\\.|[^"\\\\])*"','STR',text)
    out=[]
    for m in re.finditer(r'[A-Za-z_]\w*|\d+(?:\.\d+)?|==|!=|<=|>=|&&|\|\||::|->|\S',text):
        t=m.group()
        if re.fullmatch(r'[A-Za-z_]\w*',t) and t not in {'if','else','for','while','switch','case','return','class','struct','enum','const','static','void','int','char','float','double','bool','true','false','template','typename','namespace'}:t='ID'
        elif re.fullmatch(r'\d+(?:\.\d+)?',t):t='NUM'
        out.append((t,text.count("\n",0,m.start())+1))
    return out
def find(root,files,n=30):
    seen={}; out=[]
    for p in files:
        rel=p.relative_to(root).as_posix(); ts=tokens(p.read_text(errors="ignore"))
        for i in range(max(0,len(ts)-n+1)):
            seq=tuple(x for x,_ in ts[i:i+n]); h=hashlib.sha1(repr(seq).encode()).hexdigest()
            if h in seen:
                f,l=seen[h]
                if f!=rel:out.append(Duplicate(f,l,rel,ts[i][1],n))
            else:seen[h]=(rel,ts[i][1])
    return out
