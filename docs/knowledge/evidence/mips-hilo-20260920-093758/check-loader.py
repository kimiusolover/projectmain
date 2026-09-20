from pathlib import Path
import struct,subprocess
import os
h=Path(__file__).resolve().parent;p=Path(os.environ['HILO_RESULTS']);q=str(h/'tools/qemu-mipsel')
def run(f):return subprocess.run([q,str(p/'loader-hilo'),str(f)],capture_output=True,text=True)
r=run(p/'mips-hilo.efi');assert r.returncode==0,r.stderr;print(r.stdout,end='')
b=(p/'mips-hilo-8000.efi').read_bytes();u16=lambda o:struct.unpack_from('<H',b,o)[0];u32=lambda o:struct.unpack_from('<I',b,o)[0]
pe=u32(60);opt=pe+24;tab=opt+u16(pe+20)
rel=next(u32(tab+40*i+20) for i in range(u16(pe+6)) if b[tab+40*i:tab+40*i+8]==b'.reloc\0\0')
for name,off,val,msg in [('type',rel+8,0x3000,'only HIGHADJ and LOW'),('payload',rel+10,0xffff,'payload must match'),('missing_low',rel+12,0,'exactly one HIGHADJ'),('high_target',rel+8,0x4000,'only LUI immediate')]:
 bad=bytearray(b);struct.pack_into('<H',bad,off,val);f=p/(name+'-bad.efi');f.write_bytes(bad);r=run(f);assert r.returncode!=0 and msg in r.stderr,(name,r.stdout,r.stderr);print('PASS rejected',name)
