#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

static unsigned char file[65536];
static size_t length;
static void require(int ok, const char *why) {
  if (!ok) { fprintf(stderr, "FAIL: %s\n", why); exit(1); }
}
static uint16_t u16(size_t p) {
  require(p <= length && length-p >= 2, "header bounds");
  return file[p] | (uint16_t)file[p+1]<<8;
}
static uint32_t u32(size_t p) {
  require(p <= length && length-p >= 4, "header bounds");
  return (uint32_t)file[p] | (uint32_t)file[p+1]<<8 |
         (uint32_t)file[p+2]<<16 | (uint32_t)file[p+3]<<24;
}
int main(int argc, char **argv) {
  static const unsigned char code[16] = {
    0x25,0x10,0,0, 8,0,0xe0,3, 0,0,0,0, 0,0,0,0
  };
  require(argc==2, "usage: loader minimal.efi");
  FILE *fp=fopen(argv[1],"rb");
  require(fp!=NULL,"open PE");
  length=fread(file,1,sizeof(file),fp);
  require(!ferror(fp) && length<sizeof(file),"read PE / size limit");
  fclose(fp);
  require(length>=64 && file[0]=='M' && file[1]=='Z',"DOS header");
  size_t pe=u32(60);
  require(u32(pe)==0x4550 && u16(pe+4)==0x166,"PE signature / MIPS machine");
  require(u16(pe+6)==1,"fixture must contain one section");
  size_t opt=pe+24, os=u16(pe+20);
  require(os==224 && opt<=length && os<=length-opt,"PE32 optional header");
  require(u16(opt)==0x10b && u16(opt+68)==10,"PE32 EFI application");
  require(u32(opt+28)==0,"fixture preferred image base");
  uint32_t entry=u32(opt+16), size=u32(opt+56), headers=u32(opt+60);
  require(size>0 && size<=65536 && headers<=size && headers<=length,"image bounds");
  require(u32(opt+92)==16,"data directory count");
  for (unsigned i=0;i<16;i++) {
    /* GenFw may retain a debug directory; the fixture executes no debug data. */
    if(i!=6) require(u32(opt+96+8*i)==0 && u32(opt+100+8*i)==0,"unsupported PE directory");
  }
  size_t s=opt+os;
  require(s<=length && length-s>=40,"section header");
  require(memcmp(file+s,".text\0\0\0",8)==0,"fixture text section");
  uint32_t vs=u32(s+8), rva=u32(s+12), raw=u32(s+16), off=u32(s+20), flags=u32(s+36);
  require(entry==rva && rva>=headers && rva<=size,"entry / section RVA");
  require(vs>=16 && raw>=16 && vs<=size-rva && raw<=size-rva,"section size");
  require(off<=length && raw<=length-off,"raw section bounds");
  require((flags&0x20000000)!=0 && (flags&0x80000000)==0,"executable non-writable text");
  require(memcmp(file+off,code,16)==0,"only the exact return-zero instructions are allowed");
  unsigned char *mem=mmap(NULL,size,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
  require(mem!=MAP_FAILED,"mmap");
  memcpy(mem,file,headers);
  memcpy(mem+rva,file+off,raw);
  __builtin___clear_cache((char *)mem,(char *)mem+size);
  require(mprotect(mem,size,PROT_READ|PROT_EXEC)==0,"mprotect RX");
  /* Native o32 indirect call sets ra. Whitelisted code uses neither gp nor data. */
  uint32_t (*call)(void)=(uint32_t (*)(void))(mem+entry);
  uint32_t result=call();
  printf("Loaded base=%p entry=%p return=%u\n",(void *)mem,(void *)(mem+entry),result);
  require(munmap(mem,size)==0,"munmap");
  require(result==0,"entry return value");
  puts("PASS: exact-fixture PE mapped and executed (Linux user mode)");
  return 0;
}
