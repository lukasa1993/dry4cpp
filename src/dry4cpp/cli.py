import argparse,json
from pathlib import Path
from dataclasses import asdict
from .core import *
EXTS=('.cpp', '.cc', '.cxx', '.hpp', '.hh', '.hxx', '.h'); VERSION="0.1.0"
def main():
 p=argparse.ArgumentParser(prog="dry4cpp");p.add_argument("filters",nargs="*");p.add_argument("--root",default=".");p.add_argument("--min-tokens",type=int,default=30);p.add_argument("--json",action="store_true");p.add_argument("--fail",action="store_true");p.add_argument("--version",action="version",version="%(prog)s "+VERSION);a=p.parse_args();r=Path(a.root).resolve();fs=discover(r,EXTS)
 if a.filters: fs=[f for f in fs if any(x in f.relative_to(r).as_posix() for x in a.filters)]
 ds=find(r,fs,a.min_tokens)
 if a.json: print(json.dumps([asdict(d) for d in ds],indent=2))
 else: [print(f"{d.first_file}:{d.first_line} <-> {d.second_file}:{d.second_line} ({d.tokens} tokens)") for d in ds]
 return 2 if a.fail and ds else 0
