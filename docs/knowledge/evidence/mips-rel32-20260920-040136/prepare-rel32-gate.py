from pathlib import Path
import hashlib,struct,sys
repo=Path(sys.argv[1]);f=Path('/tmp/mips-rel32.elf').read_bytes()
assert hashlib.sha256(f).hexdigest()=='a79b75050ee0f1cb9750e5c215b7cd517d2b1f2d10531a9d147dde1009205bdd','Fixture changed'
h=struct.unpack_from('<HHIIIIIHHHHHH',f,16)
assert f[:7]==b'\x7fELF\x01\x01\x01' and h[:2]==(2,8) and h[6]==0x70001001
ss=[struct.unpack_from('<10I',f,h[5]+i*h[10]) for i in range(h[11])]
rels=[s for s in ss if s[1] in (4,9)];assert len(rels)==1
r=rels[0];assert r[1]==9 and r[5]==r[9]==8
addr,info=struct.unpack_from('<II',f,r[4]);assert info&255==2
s=ss[r[7]];assert s[1]==1 and s[2]==3 and addr==s[3]+4
assert f[s[4]:s[4]+s[5]]==struct.pack('<IIII',0x12345678,s[3],0,0)
sym=ss[r[6]];sv=struct.unpack_from('<IIIBBH',f,sym[4]+(info>>8)*sym[9]);assert sv[1]==s[3] and ss[sv[5]]==s
p=repo/'BaseTools/Source/C/GenFw/Elf32Convert.c';raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n';t=raw.decode().replace('\r\n','\n')
assert 'mMipsRel32Fixture' not in t,'Already patched'
def rep(a,b):
 global t
 assert t.count(a)==1,a
 t=t.replace(a,b)
arr='STATIC CONST UINT8 mMipsRel32Fixture[] = {\n'+''.join('  '+', '.join('0x%02x'%v for v in f[i:i+16])+',\n' for i in range(0,len(f),16))+'};\n\n'
rep('STATIC CONST UINT8 mMipsMinimalFixture[] = {',arr+'STATIC CONST UINT8 mMipsMinimalFixture[] = {')
rep('''    if ((mFileBufferSize != sizeof (mMipsMinimalFixture)) ||
        (memcmp (FileBuffer, mMipsMinimalFixture, sizeof (mMipsMinimalFixture)) != 0)) {
      Error (NULL, 0, 3000, "Unsupported", "MIPS input differs from the exact no-relocation fixture.");''','''    if (!(((mFileBufferSize == sizeof (mMipsMinimalFixture)) &&
           (memcmp (FileBuffer, mMipsMinimalFixture, sizeof (mMipsMinimalFixture)) == 0)) ||
          ((mFileBufferSize == sizeof (mMipsRel32Fixture)) &&
           (memcmp (FileBuffer, mMipsRel32Fixture, sizeof (mMipsRel32Fixture)) == 0)))) {
      Error (NULL, 0, 3000, "Unsupported", "MIPS input differs from the two exact test fixtures.");''')
rep('''IsDataShdr (
  Elf_Shdr *Shdr
  )
{
  if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
    return FALSE;
  }''','''IsDataShdr (
  Elf_Shdr *Shdr
  )
{
  if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
    return (BOOLEAN) ((Shdr->sh_type == SHT_PROGBITS) &&
                     (Shdr->sh_flags == (SHF_ALLOC | SHF_WRITE)) &&
                     (Shdr->sh_size != 0));
  }''')
rep('''        if (mEhdr->e_machine == EM_386) {
          switch''','''        if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
          // Exact ET_EXEC fixture: stored value already includes S + A.
          // Translate the target section base; do not add S a second time.
          if (ELF_R_TYPE(Rel->r_info) != 2) { // R_MIPS_32
            Error (NULL, 0, 3000, "Unsupported", "MIPS relocation is not R_MIPS_32.");
            return FALSE;
          }
          *(UINT32 *)Targ = *(UINT32 *)Targ - SymShdr->sh_addr
            + mCoffSectionsOffset[Sym->st_shndx]; // Current PE ImageBase is zero.
        } else if (mEhdr->e_machine == EM_386) {
          switch''')
rep('''          if (mEhdr->e_machine == EM_386) {
            switch''','''          if (mEhdr->e_machine == MIPS_FIXTURE_MACHINE) {
            if (ELF_R_TYPE(Rel->r_info) != 2) { // R_MIPS_32
              Error (NULL, 0, 3000, "Unsupported", "MIPS relocation is not R_MIPS_32.");
              return;
            }
            // Private test-loader contract: 32-bit base adjustment.
            CoffAddFixup(mCoffSectionsOffset[RelShdr->sh_info]
              + (Rel->r_offset - SecShdr->sh_addr), EFI_IMAGE_REL_BASED_HIGHLOW);
          } else if (mEhdr->e_machine == EM_386) {
            switch''')
backup=p.with_name(p.name+'.before-rel32-fixture');assert not backup.exists()
backup.write_bytes(raw);p.write_bytes(t.encode().replace(b'\n',nl));print('Applied R_MIPS_32 exact-fixture experiment')
