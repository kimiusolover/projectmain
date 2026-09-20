from pathlib import Path
import subprocess,struct
import os
p=Path(os.environ['HILO_RESULTS']);h=Path(__file__).resolve().parent;g=Path(os.environ['HILO_GENFW'])
u16=lambda b,o:struct.unpack_from('<H',b,o)[0]
u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
s16=lambda v:v-65536 if v&32768 else v
for name in ['mips-hilo','mips-hilo-8000']:
 out=p/(name+'.efi'); subprocess.run([str(g),'-e','UEFI_APPLICATION','-o',str(out),str(h/'inputs'/(name+'.elf'))],check=True)
 b=out.read_bytes();pe=u32(b,60);opt=pe+24;sh=opt+u16(b,pe+20)
 mem=bytearray(u32(b,opt+56))
 for i in range(u16(b,pe+6)):
  o=sh+40*i;va=u32(b,o+12);size=u32(b,o+16);off=u32(b,o+20);mem[va:va+size]=b[off:off+size]
 entry=u32(b,opt+16);rr=u32(b,opt+136);sz=u32(b,opt+140)
 assert u32(b,opt+28)==0
 for base in [0x10000000,0x10008000,0x20000000]:
  m=bytearray(mem);cursor=rr;types=[]
  while cursor<rr+sz:
   page=u32(m,cursor);end=cursor+u32(m,cursor+4);j=cursor+8
   while j<end:
    v=u16(m,j);j+=2;t=v>>12;a=page+(v&4095)
    if t==0:continue
    types.append(t)
    if t==4:
     low=s16(u16(m,j));j+=2
     val=(((u16(m,a)<<16)+low+base+0x8000)>>16)&65535
    elif t==2:val=(u16(m,a)+base)&65535
    else:raise AssertionError(t)
    struct.pack_into('<H',m,a,val)
   cursor=end
  assert types==[4,2],types
  hi=u32(m,entry);lo=u32(m,entry+4)
  assert hi>>16==0x3c08 and lo>>16==0x8d02
  address=((hi&65535)<<16)+s16(lo&65535)
  assert u32(m,address-base)==0x12345678
 print('PASS',name,'HIGHADJ/LOW, 3 simulated bases')
 bad=bytearray((h/'inputs'/(name+'.elf')).read_bytes());bad[-1]^=1
 inp=p/(name+'-mutated.elf');inp.write_bytes(bad)
 r=subprocess.run([str(g),'-e','UEFI_APPLICATION','-o',str(p/'rejected.efi'),str(inp)],capture_output=True)
 assert r.returncode!=0 and b'four exact test fixtures' in r.stderr+r.stdout
 print('PASS modified input rejected')
import re
source=(h/'snapshot/BaseTools/Source/C/GenFw/Elf32Convert.c').read_text()
for name in ['Minimal','Rel32']:
 body=re.search(r'mMips'+name+r'Fixture\[\] = \{(.*?)\};',source,re.S).group(1)
 inp=p/(name+'.elf');inp.write_bytes(bytes(int(x,16) for x in re.findall(r'0x([0-9a-fA-F]{2})',body)))
 subprocess.run([str(g),'-e','UEFI_APPLICATION','-o',str(p/(name+'.efi')),str(inp)],check=True)
 print('PASS existing fixture',name)
