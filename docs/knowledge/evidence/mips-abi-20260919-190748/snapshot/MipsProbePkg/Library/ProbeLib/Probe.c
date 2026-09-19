#include <Base.h>

STATIC_ASSERT (sizeof (UINTN) == 4, "UINTN must be 32-bit");
STATIC_ASSERT (sizeof (VOID *) == 4, "pointer must be 32-bit");

UINTN
EFIAPI
ProbeAdd (
		  IN UINTN Left,
		    IN UINTN Right
		      )
{
	  return Left + Right;
}
