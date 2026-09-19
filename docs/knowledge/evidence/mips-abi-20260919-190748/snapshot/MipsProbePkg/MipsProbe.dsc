[Defines]
  PLATFORM_NAME           = MipsProbe
  PLATFORM_GUID           = 380c1ee9-bb81-44ca-9e69-8e35e7adbd98
  PLATFORM_VERSION        = 0.1
  DSC_SPECIFICATION       = 0x00010005
  OUTPUT_DIRECTORY       = Build/MipsProbe
  SUPPORTED_ARCHITECTURES = MIPS
  BUILD_TARGETS           = DEBUG
  SKUID_IDENTIFIER        = DEFAULT

[Components]
  MipsProbePkg/Library/ProbeLib/ProbeLib.inf
