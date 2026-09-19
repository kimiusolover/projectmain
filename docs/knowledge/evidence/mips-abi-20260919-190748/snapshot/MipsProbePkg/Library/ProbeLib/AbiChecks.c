#include <Base.h>

typedef struct {
  UINT32 Tag;
  UINT64 Value;
  UINT32 Tail;
} ABI_RECORD;

UINT64 EFIAPI AbiAdd64 (UINT32 Marker, UINT64 Left, UINT64 Right);
UINT64 EFIAPI AbiVarArgs (UINT32 Marker, ...);
ABI_RECORD EFIAPI AbiTransform (ABI_RECORD Input);

STATIC_ASSERT (OFFSET_OF (ABI_RECORD, Value) == 8, "Value alignment");
STATIC_ASSERT (OFFSET_OF (ABI_RECORD, Tail) == 16, "Tail offset");
STATIC_ASSERT (sizeof (ABI_RECORD) == 24, "Structure size");

UINTN
EFIAPI
AbiRunChecks (
  VOID
  )
{
  ABI_RECORD Input;
  ABI_RECORD Output;

  /* 64bit引数・戻り値と、下位32bitからの桁上がり */
  if (AbiAdd64 (3U, 0x00000001FFFFFFFFULL,
                0x0000000200000002ULL) != 0x0000000400000004ULL) {
    return 1;
  }

  /* 異なる幅の可変引数。後半はスタック経由になる */
  if (AbiVarArgs (3U, (UINT32)5U, (UINT64)0x0000000200000007ULL,
                  (UINT32)11U) != 0x000000020000001AULL) {
    return 2;
  }

  /* 構造体を値渡しし、変更した構造体を返す */
  Input.Tag   = 10U;
  Input.Value = 0x00000002FFFFFFFFULL;
  Input.Tail  = 0x12345678U;
  Output = AbiTransform (Input);

  if ((Output.Tag != 11U) ||
      (Output.Value != 0x0000000400000001ULL) ||
      (Output.Tail != 0x479E03D2U)) {
    return 3;
  }

  /* 値渡しなので、呼出元の構造体は変わらない */
  if ((Input.Tag != 10U) ||
      (Input.Value != 0x00000002FFFFFFFFULL) ||
      (Input.Tail != 0x12345678U)) {
    return 4;
  }

  return 0;
}
