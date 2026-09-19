/** @file
  Processor binding draft for MIPS32 little-endian, o32, soft-float.
**/

#ifndef MIPS_PROCESSOR_BIND_H_
#define MIPS_PROCESSOR_BIND_H_

/*
 * This draft supports a GCC-compatible MIPS compiler only.
 */
#if !defined (__GNUC__) || !defined (__mips__)
#error "A GCC-compatible MIPS compiler is required"
#endif

#if !defined (_MIPS_SIM) || !defined (_ABIO32)
#error "Cannot identify the MIPS ABI"
#elif _MIPS_SIM != _ABIO32
#error "Only the o32 ABI is supported"
#endif

#if !defined (__MIPSEL__)
#error "Only little-endian MIPS is supported"
#endif

#if !defined (__mips_soft_float)
#error "Soft-float is required"
#endif

#if defined (__mips16) || defined (__mips_micromips)
#error "MIPS16 and microMIPS are not supported"
#endif

#define MDE_CPU_MIPS

/*
 * Integer and character types.
 * Let Base.h assertions verify their sizes and alignments.
 */
typedef unsigned long long  UINT64;
typedef long long           INT64;
typedef unsigned int        UINT32;
typedef int                 INT32;
typedef unsigned short      UINT16;
typedef short               INT16;
typedef unsigned char       UINT8;
typedef signed char         INT8;

typedef unsigned char       BOOLEAN;
typedef char                CHAR8;
typedef unsigned short      CHAR16;

/* Native-width integers: 32 bits for o32. */
typedef UINT32              UINTN;
typedef INT32               INTN;

#define MAX_BIT      0x80000000U
#define MAX_2_BITS   0xC0000000U
#define MAX_ADDRESS  0xFFFFFFFFU

#define MAX_INTN     ((INTN)0x7FFFFFFF)
#define MAX_UINTN    ((UINTN)0xFFFFFFFFU)

/* o32 stack alignment requirement. */
#define CPU_STACK_ALIGNMENT  8

/*
 * Initial firmware allocation policy.
 * These values do not describe the hardware TLB page size.
 */
#define DEFAULT_PAGE_ALLOCATION_GRANULARITY  0x1000
#define RUNTIME_PAGE_ALLOCATION_GRANULARITY  0x1000

/*
 * Project convention: use the compiler's native o32 calling convention.
 * Every linked module must use matching ABI options.
 */
#ifndef EFIAPI
#define EFIAPI
#endif

#define ASM_GLOBAL  .globl

#define FUNCTION_ENTRY_POINT(FunctionPointer) \
  ((VOID *)(UINTN)(FunctionPointer))

#endif
