#include <Base.h>

typedef struct {
  UINT32 Tag;
  UINT64 Value;
  UINT32 Tail;
} ABI_RECORD;

UINT64
EFIAPI
AbiAdd64 (
  UINT32 Marker,
  UINT64 Left,
  UINT64 Right
  )
{
  return Left + Right + Marker;
}

UINT64
EFIAPI
AbiVarArgs (
  UINT32 Marker,
  ...
  )
{
  VA_LIST Args;
  UINT32  First;
  UINT64  Wide;
  UINT32  Last;

  VA_START (Args, Marker);
  First = VA_ARG (Args, UINT32);
  Wide  = VA_ARG (Args, UINT64);
  Last  = VA_ARG (Args, UINT32);
  VA_END (Args);

  return Marker + (UINT64)First + Wide + Last;
}

ABI_RECORD
EFIAPI
AbiTransform (
  ABI_RECORD Input
  )
{
  Input.Tag   += 1U;
  Input.Value += 0x100000002ULL;
  Input.Tail  ^= 0x55AA55AAU;
  return Input;
}
