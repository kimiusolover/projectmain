#!/bin/bash
set -eo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo=${EDK2_ROOT:-/home/nakan/projectmain/edk2-mips-p0-shallow}
export STAGING_DIR=${STAGING_DIR:-/home/nakan/toolchains/openwrt-toolchain-25.12.5-ramips-mt7621_gcc-14.3.0_musl.Linux-x86_64/toolchain-mipsel_24kc_gcc-14.3.0_musl}
export GCC_MIPS_PREFIX="$STAGING_DIR/bin/mipsel-openwrt-linux-musl-"
cd "$repo"
source edksetup.sh
set -eo pipefail
build -a MIPS -t GCC -b DEBUG -p MipsProbePkg/MipsProbe.dsc -m MipsProbePkg/Library/ProbeLib/ProbeLib.inf clean
build -a MIPS -t GCC -b DEBUG -p MipsProbePkg/MipsProbe.dsc -m MipsProbePkg/Library/ProbeLib/ProbeLib.inf
probe_out="$repo/Build/MipsProbe/DEBUG_GCC/MIPS/MipsProbePkg/Library/ProbeLib/ProbeLib/OUTPUT"
mkdir -p "$here/results"
cp "$probe_out/MipsProbeLib.lib" "$here/results/"
"${GCC_MIPS_PREFIX}gcc" --version
"$here/qemu-mipsel" --version
for kind in abi add; do
  entry="$here/start.S"
  if [ "$kind" = add ]; then entry="$here/add-start.S"; fi
  "${GCC_MIPS_PREFIX}gcc" -EL -march=mips32r2 -mabi=32 -msoft-float -mno-abicalls -fno-pic -fno-pie -G0 -mno-mips16 -mno-micromips -O0 -ffreestanding -fno-builtin -fno-tree-loop-distribute-patterns -fno-stack-protector -nostdlib -static -no-pie -Wl,-e,_start "$entry" "$here/results/MipsProbeLib.lib" "$here/memcpy.c" -o "$here/results/$kind.elf"
  "${GCC_MIPS_PREFIX}readelf" -h -A "$here/results/$kind.elf" > "$here/results/$kind-readelf.txt"
  "$here/qemu-mipsel" -strace "$here/results/$kind.elf"
  echo "$kind runtime PASS (exit 0)"
done
"${GCC_MIPS_PREFIX}ar" t "$here/results/MipsProbeLib.lib"
"${GCC_MIPS_PREFIX}nm" --defined-only "$here/results/MipsProbeLib.lib"
