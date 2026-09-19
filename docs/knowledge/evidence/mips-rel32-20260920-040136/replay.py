from pathlib import Path
import os, subprocess, struct
h=Path(__file__).resolve().parent
repo=Path(os.environ.get('EDK2_ROOT','/home/nakan/projectmain/edk2-mips-p0-shallow'))
tc=Path(os.environ.get('STAGING_DIR','/home/nakan/toolchains/openwrt-toolchain-25.12.5-ramips-mt7621_gcc-14.3.0_musl.Linux-x86_64/toolchain-mipsel_24kc_gcc-14.3.0_musl'))
os.environ['STAGING_DIR']=str(tc)
cc=tc/'bin/mipsel-openwrt-linux-musl-gcc'
q=Path(os.environ.get('QEMU_MIPSEL',str(h.parent/'mips-pe-20260920-030858/qemu-mipsel')))
r=h/'results';r.mkdir(exist_ok=True)
def run(a):
 print('+',' '.join(map(str,a)),flush=True)
 subprocess.run(list(map(str,a)),cwd=repo,check=True)
s=Path('BaseTools/Source/C/GenFw/Elf32Convert.c')
assert (repo/s).read_bytes()==(h/'snapshot'/s).read_bytes(), 'GenFw source mismatch'
run(['make','-C','BaseTools/Source/C','HOST_ARCH=X64','CC=/usr/bin/gcc','CXX=/usr/bin/g++','GenFw-clean'])
run(['make','-C','BaseTools/Source/C','HOST_ARCH=X64','CC=/usr/bin/gcc','CXX=/usr/bin/g++','GenFw'])
g=repo/'BaseTools/Source/C/bin/GenFw'
run([cc,'--version']);run([q,'--version'])
run([g,'-e','UEFI_APPLICATION','-o',r/'rel32.efi',h/'input.elf'])
run([cc,'-EL','-march=mips32r2','-mabi=32','-msoft-float','-mno-mips16','-mno-micromips','-O2','-Wall','-Wextra','-Werror','-static',h/'loader.c','-o',r/'loader'])
run([q,r/'loader',r/'rel32.efi'])
b=(r/'rel32.efi').read_bytes();pe=struct.unpack_from('<I',b,60)[0];opt=pe+24
s=opt+struct.unpack_from('<H',b,pe+20)[0]
for i in range(struct.unpack_from('<H',b,pe+6)[0]):
 p=s+40*i
 if b[p:p+8]==b'.reloc\0\0': off=struct.unpack_from('<I',b,p+20)[0]
def reject(a,expected):
 p=subprocess.run(list(map(str,a)),cwd=repo,capture_output=True,text=True)
 print(p.stdout+p.stderr,flush=True)
 assert p.returncode!=0 and expected in p.stdout+p.stderr
 print('PASS: rejected with exit',p.returncode,flush=True)
for name,at,value,fmt,msg in [('type',off+8,0x5244,'H','only HIGHLOW supported'),('target',off+8,0x3240,'H','only ProbePointer may be relocated'),('missing',opt+140,0,'I','relocation directory bounds')]:
 m=bytearray(b);struct.pack_into('<'+fmt,m,at,value);p=r/('invalid-'+name+'.efi');p.write_bytes(m)
 reject([q,r/'loader',p],msg)
f=bytearray((h/'input.elf').read_bytes());shoff=struct.unpack_from('<I',f,32)[0];ents,n=struct.unpack_from('<HH',f,46)
for i in range(n):
 p=shoff+i*ents
 if struct.unpack_from('<I',f,p+4)[0]==9:
  at=struct.unpack_from('<I',f,p+16)[0];f[at+4]=5;break
(r/'invalid.elf').write_bytes(f)
reject([g,'-e','UEFI_APPLICATION','-o',r/'must-reject.efi',r/'invalid.elf'],'differs from the two exact test fixtures')
run([g,'-e','UEFI_APPLICATION','-o',r/'minimal.efi',h.parent/'mips-pe-20260920-030858/accepted.elf'])
run([q,h.parent/'mips-pe-20260920-030858/results/loader',r/'minimal.efi'])
print('ALL CHECKS PASS',flush=True)
