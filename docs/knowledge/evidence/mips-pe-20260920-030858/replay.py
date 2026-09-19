from pathlib import Path
import os, subprocess, struct
here=Path(__file__).resolve().parent
repo=Path(os.environ.get('EDK2_ROOT','/home/nakan/projectmain/edk2-mips-p0-shallow'))
tc=Path(os.environ.get('STAGING_DIR','/home/nakan/toolchains/openwrt-toolchain-25.12.5-ramips-mt7621_gcc-14.3.0_musl.Linux-x86_64/toolchain-mipsel_24kc_gcc-14.3.0_musl'))
os.environ['STAGING_DIR']=str(tc)
cc=str(tc/'bin/mipsel-openwrt-linux-musl-gcc')
r=here/'results';r.mkdir(exist_ok=True)
def run(args):
 print('+', ' '.join(map(str,args)),flush=True)
 subprocess.run(list(map(str,args)),check=True,cwd=repo)
source=Path('BaseTools/Source/C/GenFw/Elf32Convert.c')
if (repo/source).read_bytes()!=(here/'snapshot'/source).read_bytes():
 raise SystemExit('GenFw source differs from saved snapshot; restore/review before replay')
run(['make','-C','BaseTools/Source/C','HOST_ARCH=X64','CC=/usr/bin/gcc','CXX=/usr/bin/g++','GenFw-clean'])
run(['make','-C','BaseTools/Source/C','HOST_ARCH=X64','CC=/usr/bin/gcc','CXX=/usr/bin/g++','GenFw'])
gen=repo/'BaseTools/Source/C/bin/GenFw'
run([gen,'--version']);run([here/'qemu-mipsel','--version']);run([cc,'--version'])
run([gen,'-e','UEFI_APPLICATION','-o',r/'minimal.efi',here/'accepted.elf'])
b=(r/'minimal.efi').read_bytes()
u16=lambda n:struct.unpack_from('<H',b,n)[0]
u32=lambda n:struct.unpack_from('<I',b,n)[0]
assert b[:2]==b'MZ'
pe=u32(60);opt=pe+24
assert b[pe:pe+4]==b'PE\0\0' and u16(pe+4)==0x166
assert u16(opt)==0x10b and u16(opt+68)==10
assert u32(opt+136)==0 and u32(opt+140)==0
assert u16(pe+6)==1
s=opt+u16(pe+20);off=u32(s+20)
assert b[s:s+8]==b'.text\0\0\0'
assert u32(opt+16)==u32(s+12)
assert b[off:off+16]==bytes.fromhex('251000000800e0030000000000000000')
print('PASS: PE32 headers, entry, instructions, empty relocation directory',flush=True)
run([cc,'-EL','-march=mips32r2','-mabi=32','-msoft-float','-mno-mips16','-mno-micromips','-O2','-Wall','-Wextra','-Werror','-static',here/'loader.c','-o',r/'loader'])
run([here/'qemu-mipsel',r/'loader',r/'minimal.efi'])
def reject(args, message):
 p=subprocess.run(list(map(str,args)),cwd=repo,capture_output=True,text=True)
 print(p.stdout+p.stderr,flush=True)
 assert p.returncode!=0 and message in p.stdout+p.stderr
 print('PASS: rejected; exit',p.returncode,flush=True)
reject([gen,'-e','UEFI_APPLICATION','-o',r/'must-reject.efi',here/'original.elf'],'differs from the exact no-relocation fixture')
e=bytearray((here/'accepted.elf').read_bytes());e[0xf0]^=1
(r/'mutated.elf').write_bytes(e)
reject([gen,'-e','UEFI_APPLICATION','-o',r/'must-reject.efi',r/'mutated.elf'],'differs from the exact no-relocation fixture')
p=bytearray(b);p[off]^=1;(r/'mutated.efi').write_bytes(p)
reject([here/'qemu-mipsel',r/'loader',r/'mutated.efi'],'only the exact return-zero instructions are allowed')
print('ALL CHECKS PASS',flush=True)
