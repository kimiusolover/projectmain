#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>

static unsigned char file[65536];
static size_t length;
static void ck(int ok,const char *s) { if(!ok){fprintf(stderr,"FAIL: %s\n",s);exit(1);} }
static uint16_t le16(const unsigned char *p){return p[0]|(uint16_t)p[1]<<8;}
static uint32_t le32(const unsigned char *p){return p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;}
static void put16(unsigned char *p,uint16_t v){p[0]=(unsigned char)v;p[1]=(unsigned char)(v>>8);}
static int32_t signed16(uint16_t v){return v&0x8000?(int32_t)v-65536:v;}
static uint16_t f16(size_t p){ck(p<=length && length-p>=2,"header bounds");return le16(file+p);}
static uint32_t f32(size_t p){ck(p<=length && length-p>=4,"header bounds");return le32(file+p);}
struct section { uint32_t rva,raw,off,span,flags; };
int main(int argc,char **argv){
  struct section sec[3];
  unsigned char *maps[2];
  int ti=-1,di=-1,ri=-1;
  ck(argc==2,"usage: loader-hilo hilo.efi");
  FILE *fp=fopen(argv[1],"rb");ck(fp!=NULL,"open PE");
  length=fread(file,1,sizeof(file),fp);ck(!ferror(fp)&&length<sizeof(file),"read/size");fclose(fp);
  ck(length>=64 && file[0]=='M' && file[1]=='Z',"DOS header");
  size_t pe=f32(60),opt=pe+24;
  ck(f32(pe)==0x4550 && f16(pe+4)==0x166,"MIPS PE signature");
  ck(f16(pe+6)==3 && f16(pe+20)==224,"fixture requires three sections / PE32 header");
  ck(opt<=length && length-opt>=224,"optional header bounds");
  ck(f16(opt)==0x10b && f16(opt+68)==10,"PE32 EFI application");
  uint32_t entry=f32(opt+16),base=f32(opt+28),size=f32(opt+56),headers=f32(opt+60);
  ck(base==0 && size>0 && size<=0x8000 && headers<=size && headers<=length,"image bounds/base");
  ck(f32(opt+92)==16,"directory count");
  for(unsigned i=0;i<16;i++)if(i!=5 && i!=6)ck(f32(opt+96+8*i)==0 && f32(opt+100+8*i)==0,"unsupported directory");
  size_t tab=opt+224;ck(tab<=headers && headers-tab>=120,"section table bounds");
  for(unsigned i=0;i<3;i++){
    size_t s=tab+40*i;uint32_t vs=f32(s+8);
    sec[i]=(struct section){f32(s+12),f32(s+16),f32(s+20),0,f32(s+36)};
    sec[i].span=vs>sec[i].raw?vs:sec[i].raw;
    ck(sec[i].rva>=headers && sec[i].rva<=size && sec[i].span<=size-sec[i].rva,"section image bounds");
    ck(sec[i].off<=length && sec[i].raw<=length-sec[i].off,"raw bounds");
    for(unsigned j=0;j<i;j++)ck(sec[i].rva>=sec[j].rva+sec[j].span || sec[j].rva>=sec[i].rva+sec[i].span,"overlapping sections");
    if(!memcmp(file+s,".text\0\0\0",8)){ck(ti<0,"duplicate text");ti=i;}
    else if(!memcmp(file+s,".data\0\0\0",8)){ck(di<0,"duplicate data");di=i;}
    else if(!memcmp(file+s,".reloc\0\0",8)){ck(ri<0,"duplicate reloc");ri=i;}
    else ck(0,"unknown section");
  }
  ck(ti>=0&&di>=0&&ri>=0,"required sections");
  struct section t=sec[ti],d=sec[di],r=sec[ri];
  ck(entry==t.rva && t.raw>=16,"entry bounds");
  ck((f32(t.off)&0xffff0000)==0x3c080000 && (f32(t.off+4)&0xffff0000)==0x8d020000 && f32(t.off+8)==0x03e00008 && f32(t.off+12)==0,"exact LUI/LW/JR/NOP");
  uint16_t initial_hi=f16(t.off),initial_lo=f16(t.off+4);
  ck(((uint32_t)initial_hi<<16)+(uint32_t)signed16(initial_lo)==d.rva,"initial instruction address");
  ck((t.flags&0x20000000)!=0 && (t.flags&0x80000000)==0,"text permissions");
  ck((d.flags&0x80000000)!=0 && (d.flags&0x20000000)==0,"data permissions");
  ck(d.raw>=4 && d.rva%4==0 && d.rva<0x8000 && f32(d.off)==0x12345678,"fixture data");
  uint32_t dir=f32(opt+136),bytes=f32(opt+140),high_target=0,low_target=0;
  ck(dir==r.rva && bytes>=8 && bytes<=r.raw,"relocation directory bounds");
  unsigned highs=0,lows=0; uint16_t payload=0;
  for(uint32_t p=0;p<bytes;){
    ck(bytes-p>=8,"relocation block header");
    uint32_t page=f32(r.off+p),block=f32(r.off+p+4);
    ck(page%4096==0 && block>=8 && block%4==0 && block<=bytes-p,"relocation block");
    for(uint32_t j=8;j<block;j+=2){
      uint16_t e=f16(r.off+p+j);unsigned type=e>>12;
      if(type==0)continue;
      ck(type==4 || type==2,"only HIGHADJ and LOW supported");
      ck(page<=size && (e&4095)<=size-page,"relocation RVA bounds");
      uint32_t target=page+(e&4095);
      if(type==4){
        ck(++highs==1 && target==entry,"only LUI immediate may receive HIGHADJ");
        ck(block-j>=4,"HIGHADJ missing payload");
        payload=f16(r.off+p+j+2);j+=2;
        ck(payload==initial_lo,"HIGHADJ payload must match original LOW");
        high_target=target;
      }else{
        ck(++lows==1 && target==entry+4,"only LW immediate may receive LOW");
        low_target=target;
      }
    }
    p+=block;
  }
  ck(highs==1 && lows==1,"exactly one HIGHADJ and one LOW required");
  /* Reserve first, then choose page-aligned bases across the signed-low boundary.
     No MAP_FIXED: never overwrite an existing mapping. */
  size_t reserve_size=0x40000;
  unsigned char *reserve=mmap(NULL,reserve_size,PROT_NONE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
  ck(reserve!=MAP_FAILED,"reserve mappings");
  uintptr_t aligned=((uintptr_t)reserve+0xffff)&~(uintptr_t)0xffff;
  maps[0]=(unsigned char *)aligned;
  maps[1]=(unsigned char *)(aligned+0x18000);
  for(unsigned i=0;i<2;i++)ck(mprotect(maps[i],size,PROT_READ|PROT_WRITE)==0,"mprotect RW");
  for(unsigned i=0;i<2;i++){
    unsigned char *mem=maps[i];memcpy(mem,file,headers);
    for(unsigned j=0;j<3;j++)memcpy(mem+sec[j].rva,file+sec[j].off,sec[j].raw);
    uint32_t delta=(uint32_t)(uintptr_t)mem-base;
    uint32_t adjusted=((uint32_t)le16(mem+high_target)<<16)
      +(uint32_t)signed16(payload)+delta+0x8000U;
    put16(mem+high_target,(uint16_t)(adjusted>>16));
    put16(mem+low_target,(uint16_t)(le16(mem+low_target)+delta));
    uint32_t pointer=((uint32_t)le16(mem+high_target)<<16)
      +(uint32_t)signed16(le16(mem+low_target));
    ck(pointer==(uint32_t)(uintptr_t)(mem+d.rva),"relocated instruction address");
    ck(((le16(mem+low_target)&0x8000)!=0)==(i==1),"opposite sides of signed LOW boundary");
    __builtin___clear_cache((char *)mem,(char *)mem+size);
    /* Small sections share a host page. After fixups this test makes all RX. */
    ck(mprotect(mem,size,PROT_READ|PROT_EXEC)==0,"mprotect RX");
    uint32_t observed=*(volatile const uint32_t *)(uintptr_t)pointer;
    ck(observed==0x12345678,"pointer dereference");
    uint32_t (*call)(void)=(uint32_t (*)(void))(mem+entry);
    uint32_t result=call();ck(result==0x12345678,"entry return value");
    printf("base=%p pointer=0x%08x value=0x%08x return=0x%08x\n",(void *)mem,pointer,observed,result);
  }
  ck(munmap(reserve,reserve_size)==0,"munmap reservation");
  puts("PASS: HIGHADJ + LOW; MIPS code returned 0x12345678 at two bases across signed LOW boundary");return 0;
}
