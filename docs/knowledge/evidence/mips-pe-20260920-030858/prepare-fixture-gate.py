from pathlib import Path
import hashlib,struct,sys
repo=Path(sys.argv[1])
p=repo/'BaseTools/Source/C/GenFw/Elf32Convert.c'
f=Path('/tmp/mips-pe-minimal-nopdr.elf').read_bytes()
assert hashlib.sha256(f).hexdigest()=='e1d37efb3ed7319c4804f1a2f2b4ea775241e8f04bea0ec0790f5f28d809d9b8','Fixture changed: stop'
assert f[:7]==b'\x7fELF\x01\x01\x01'
h=struct.unpack_from('<HHIIIIIHHHHHH',f,16)
assert h[0:2]==(2,8) and h[6]==0x70001001
sections=[struct.unpack_from('<10I',f,h[5]+i*h[10]) for i in range(h[11])]
assert not any(s[1] in (4,9) for s in sections)
textsecs=[s for s in sections if s[2]&6==6]
assert len(textsecs)==1
s=textsecs[0]
assert h[3]==s[3] and f[s[4]:s[4]+s[5]]==bytes.fromhex('251000000800e0030000000000000000')
assert not any(s[2]&1 and s[5] for s in sections)
raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n';src=raw.decode().replace('\r\n','\n')
assert 'mMipsMinimalFixture' not in src,'Already patched'
def replace(old,new):
 global src
 assert src.count(old)==1,old
 src=src.replace(old,new)
array='\n/* Experimental exact-fixture gate; not general MIPS support. */\n#define MIPS_FIXTURE_MACHINE  8\n#define MIPS_FIXTURE_PE_MACHINE  0x0166 /* Project convention only. */\nSTATIC CONST UINT8 mMipsMinimalFixture[] = {\n'+''.join('  '+', '.join('0x%02x'%b for b in f[i:i+16])+',\n' for i in range(0,len(f),16))+'};\n'
replace('#include "Elf32Convert.h"','#include "Elf32Convert.h"\n'+array)
replace('  mEhdr = (Elf_Ehdr*) FileBuffer;','''  if (mFileBufferSize < sizeof (Elf_Ehdr)) {
    Error (NULL, 0, 3000, "Invalid", "Truncated ELF32 header.");
    return FALSE;
  }
  mEhdr = (Elf_Ehdr*) FileBuffer;
  if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
    if ((mFileBufferSize != sizeof (mMipsMinimalFixture)) ||
        (memcmp (FileBuffer, mMipsMinimalFixture, sizeof (mMipsMinimalFixture)) != 0)) {
      Error (NULL, 0, 3000, "Unsupported", "MIPS input differs from the exact no-relocation fixture.");
      return FALSE;
    }
  }''')
replace('if (!((mEhdr->e_machine == EM_386) || (mEhdr->e_machine == EM_RISCV)))','if (!((mEhdr->e_machine == EM_386) || (mEhdr->e_machine == EM_RISCV) || (mEhdr->e_machine == MIPS_FIXTURE_MACHINE)))')
replace('  case EM_386:\n    mCoffOffset += sizeof (EFI_IMAGE_NT_HEADERS32);','  case MIPS_FIXTURE_MACHINE:\n  case EM_386:\n    mCoffOffset += sizeof (EFI_IMAGE_NT_HEADERS32);')
replace('  case EM_386:\n    NtHdr->Pe32.FileHeader.Machine', '''  case MIPS_FIXTURE_MACHINE:
    NtHdr->Pe32.FileHeader.Machine = MIPS_FIXTURE_PE_MACHINE;
    NtHdr->Pe32.OptionalHeader.Magic = EFI_IMAGE_NT_OPTIONAL_HDR32_MAGIC;
    break;
  case EM_386:
    NtHdr->Pe32.FileHeader.Machine''')
replace('''IsTextShdr (
  Elf_Shdr *Shdr
  )
{
''','''IsTextShdr (
  Elf_Shdr *Shdr
  )
{
  if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
    return (BOOLEAN) ((Shdr->sh_type == SHT_PROGBITS) &&
                     (Shdr->sh_flags == (SHF_ALLOC | SHF_EXECINSTR)) &&
                     (Shdr->sh_size != 0));
  }
''')
replace('''IsDataShdr (
  Elf_Shdr *Shdr
  )
{
''','''IsDataShdr (
  Elf_Shdr *Shdr
  )
{
  if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
    return FALSE;
  }
''')
backup=p.with_name(p.name+'.before-exact-fixture')
assert not backup.exists(),'Backup exists: stop'
backup.write_bytes(raw);p.write_bytes(src.encode().replace(b'\n',nl))
print('Applied exact-fixture gate:',p)
