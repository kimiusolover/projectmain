/* Compiler-generated copies: standalone ABI test support. */
void *
memcpy (
  void *Destination,
  const void *Source,
  __SIZE_TYPE__ Length
  )
{
  unsigned char *Dst = Destination;
  const unsigned char *Src = Source;

  for (__SIZE_TYPE__ Index = 0; Index < Length; ++Index) {
    Dst[Index] = Src[Index];
  }

  return Destination;
}
