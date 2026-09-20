#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,shutil,subprocess,tempfile
h=Path(__file__).resolve().parent
manifest=json.loads((h/'manifest.json').read_text())
for name,digest in manifest['sha256'].items():
 if hashlib.sha256((h/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Hash mismatch: '+name)
print('PASS: saved evidence hashes',flush=True)
tc=Path(os.environ.get('STAGING_DIR',manifest['toolchain']))
env=os.environ.copy();env['STAGING_DIR']=str(tc)
cc=tc/'bin/mipsel-openwrt-linux-musl-gcc'
for name,digest in manifest['tool_sha256'].items():
 if hashlib.sha256((tc/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Tool mismatch: '+name)
with tempfile.TemporaryDirectory(prefix='mips-hilo-replay-') as tmp:
 w=Path(tmp);shutil.copytree(h/'snapshot',w/'build');r=w/'results';r.mkdir()
 g=w/'build/BaseTools/Source/C/bin/GenFw'
 env['HILO_RESULTS']=str(r);env['HILO_GENFW']=str(g)
 def run(args):
  print('+',' '.join(map(str,args)),flush=True)
  subprocess.run(list(map(str,args)),env=env,check=True,cwd=w)
 run([cc,'--version']);run([h/'tools/qemu-mipsel','--version'])
 run(['make','-C',w/'build/BaseTools/Source/C','HOST_ARCH=X64','CC=/usr/bin/gcc','CXX=/usr/bin/g++','GenFw'])
 flags=['-EL','-march=mips32r2','-mabi=32','-msoft-float','-mno-mips16','-mno-micromips']
 for name,extra in [('mips-hilo',[]),('mips-hilo-8000',['-Wl,-Tdata=0x00418000'])]:
  out=r/(name+'.elf')
  run([cc,*flags,'-mno-abicalls','-fno-pic','-fno-pie','-G0','-nostdlib','-static','-no-pie','-Wl,-e,MinimalEntry,--emit-relocs,--build-id=none',*extra,h/'inputs/mips-hilo.S','-o',out])
  if out.read_bytes()!=(h/'inputs'/out.name).read_bytes():raise RuntimeError('Rebuilt ELF differs: '+name)
  run([tc/'bin/mipsel-openwrt-linux-musl-readelf','-h','-r','-A',out])
  run([tc/'bin/mipsel-openwrt-linux-musl-objdump','-dr',out])
 run(['python3',h/'check-conversion.py'])
 run([cc,*flags,'-O2','-Wall','-Wextra','-Werror','-static',h/'loader-hilo.c','-o',r/'loader-hilo'])
 for name in ['mips-hilo','mips-hilo-8000']:
  run([h/'tools/qemu-mipsel',r/'loader-hilo',r/(name+'.efi')])
 run(['python3',h/'check-loader.py'])
 # Keep generated files only when explicitly requested; original evidence is immutable.
 if os.environ.get('HILO_OUTPUT'):
  shutil.copytree(r,Path(os.environ['HILO_OUTPUT']))
print('PASS: replay complete (exact fixtures; Linux user-mode QEMU only)',flush=True)
