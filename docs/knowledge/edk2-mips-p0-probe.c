typedef unsigned int UINTN;
typedef unsigned long long UINT64;
_Static_assert(sizeof(void *) == 4, "pointer32");
_Static_assert(sizeof(long) == 4, "long32");
_Static_assert(sizeof(UINT64) == 8, "uint64");
_Static_assert(__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__, "little-endian");
_Static_assert(__mips == 32 && __mips_isa_rev == 2, "mips32r2");
#ifndef __mips_soft_float
#error soft-float required
#endif
volatile UINTN probe_data = 7;
UINTN (*probe_callback)(UINTN);
UINTN probe(UINTN x) { return probe_callback(x) + probe_data; }
