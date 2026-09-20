#include <Base.h>

STATIC_ASSERT (sizeof (VOID *) == 4, "pointer must be 32-bit");
STATIC_ASSERT (sizeof (UINTN) == 4, "UINTN must be 32-bit");
STATIC_ASSERT (sizeof (INTN) == 4, "INTN must be 32-bit");
STATIC_ASSERT (ALIGNOF (UINT64) == 8, "UINT64 alignment must be 8");
STATIC_ASSERT (CPU_STACK_ALIGNMENT == 8, "o32 stack alignment");
