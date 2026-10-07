# EDK II MIPS P0 baseline

Status: accepted for research configuration; ELF probe verified; EDK II port unimplemented
Decided: 2026-09-18
Reason: Freeze source identity, compiler distribution, ABI and image-format choices before MIPS port work.
Supersedes: Unpinned baseline candidates in the feasibility discussion.
Related: [machine-readable decision](edk2-mips-p0.json), [toolchain profile](../../router-upstream/toolchains/mipsel-24kc-musl.yaml), [source-lock policy](../../router-upstream/policies/locked-input-v1.md), [DECISIONS.md#d-009-router-uefi-platform-architecture-v1](../../DECISIONS.md#d-009-router-uefi-platform-architecture-v1)

## 決定

| 項目 | 固定値 |
| --- | --- |
| EDK II | `2970e5699ba6267f3384ffab20f96647578aebc8` |
| 参照タグ | `edk2-stable202608`（ビルド識別にはSHAを使用） |
| toolchain | OpenWrt 25.12.5 ramips/mt7621 Linux-x86_64配布物 |
| GCC / binutils | `14.3.0` / `2.44`（取得物の実行結果） |
| compiler prefix | `mipsel-openwrt-linux-musl-` |
| ISA / tune | `mips32r2` / `1004kc` |
| ABI | little-endian、o32、soft-float、32bit pointer/UINTN |
| EFIAPI | 全モジュールで同じnative o32呼出規約。特別な属性なし |
| stack / CHAR16 | 最小8byte整列 / 16bit |
| libc | firmwareにはリンクしない。musl sysrootとLinux startup objectは使用しない |
| 中間形式 | ELF32 little-endian / EM_MIPS、ET_REL→ET_EXEC、再配置情報を保持 |
| 初期RAM入口 | ELF32 ET_EXEC。実機入口・ロードアドレスは未指定 |
| DXE/EFI application | PE32、OptionalHeader Magic `0x10b`、Machine `0x0166` |
| PE subsystem | EFI application=10、boot-service driver=11 |
| TE / runtime driver | 初期移植の対象外 |

PEのMachine値はMIPS EFIの既存慣例を参考にしたプロジェクト内の決定。標準UEFI MIPS ABIへの適合を主張しない。PE32+、MIPS64/N32、MIPS16、microMIPS、hard-floatと混在させない。

## CPU資料の扱い

ユーザー指定の `MT7621.pdf`、PDF 2/43ページのOverview/FeaturesにMIPS 1004Kc、各coreの32KB I/D cacheが記載されている。資料は `DSMT7621_V.0.2_Prelimanary` であり、AX23Vの搭載RAM、Flash配置、入口アドレスの証拠ではない。little-endianは既存platform定義に合わせたP0選択、o32/soft-floatはソフトウェア側の決定である。

PDF SHA-256: `1713012937102a9ec6d0fe1fe555d43437b1f2fd9ec60e2b4b0dca5b49851425`。

## コンパイル規約

```text
-EL -march=mips32r2 -mtune=1004kc -mabi=32 -msoft-float
-mno-abicalls -fno-pic -fno-pie -G0 -mno-mips16 -mno-micromips
-ffreestanding -fshort-wchar -fno-stack-protector
-fno-asynchronous-unwind-tables -fno-unwind-tables -O2
```

これはP0 probeの固定フラグ。`-fno-stack-protector`は初期CPU/ABI probe限定であり、productionの保護方針ではない。保護を有効化する際は正しいfailure handlerを実装し、Nullへ置換しない。DebugLib等のproduction設定も本決定の対象外。

リンクはtarget ldを直接使い、`-EL -m elf32ltsmip --emit-relocs`を指定する。GCC driver経由なら`-nostdlib`等で標準startup/libcを除外する。必要になるcompiler helperは個別に監査して採用し、libgcc全体を無条件リンクしない。`STAGING_DIR`は抽出したtoolchain rootに固定する。

`-G0`/`-mno-abicalls`でsmall-data/GOT前提を抑制するが、絶対参照の再配置は残る。コンパイル成功をPE移植成功と扱わない。

## 確認できた証拠

- Git remoteのタグを上記commitに解決し、GitHub Git commit APIでも同じcommit objectを確認。
- commit treeの全gitlinkをJSONに記録。サブモジュールは親commitに記録されたSHAのみを使用し、branch追従しない。必要なarchive/hashの取得は別のsource intake。
- 既存toolchainロック、公式sha256sums、取得した47MB程度のarchive bytesのSHA-256が一致。
- toolchain SHA-256: `04316e081dcaea0394d3a8eca761500c91d7d54e9d49ccb8f855ae257ea4f995`。
- 静的assertでpointer/long/64bit型幅、little-endian、MIPS32r2、soft-floatを確認。
- ELF32 ET_EXECへのリンク成功。readelfでo32/mips32r2/soft-float、dynamic sectionなしを確認。
- `R_MIPS_HI16` / `R_MIPS_LO16` / `R_MIPS_32`が実際に残ることを確認。
- probeは実行していない。`0x01000000`はhost link fixtureだけであり、実機ロード先ではない。

Probeソースとreadelf出力は同じフォルダの `edk2-mips-p0-probe.c` と `edk2-mips-p0-readelf.txt` に保存。

## 残る移植と境界

固定commitのGenFw/Elf32Convert.cにEM_MIPS経路は存在しない。Machine値を書き換えるだけでは起動できない。以下を実装して初めてP1/P2の検証対象になる。

1. BaseTools architecture/toolchain処理、ProcessorBind、CPU依存library。
2. ELF→PE変換とEDK II loaderのMachine判定。
3. HI16/LO16の対応関係と符号繰上がりを保った再配置、R_MIPS_32、直接jump R_MIPS_26等の扱い。未知の再配置は拒否する。ELF relocation番号をPEへそのままコピーしない。
4. .relocを持つPE32の異なるアドレスへのロード試験。HI16/LO16の境界、関数pointer、data pointer、module間callを試験する。
5. o32の可変引数、UINT64、構造体、stack整列の実行試験。

本記録はsource-lock-v1レコードではない。EDK II本体・必要submoduleのarchive SHA、完全なhost build環境、downstream patchsetは未固定のため、EDK IIビルド再現性の達成とは呼ばない。既存AX23V targetのpending-verificationとimage/flash/RFゲートは変更しない。

## 一次資料

- [EDK II固定commit](https://github.com/tianocore/edk2/commit/2970e5699ba6267f3384ffab20f96647578aebc8)
- [固定commitのGenFw](https://github.com/tianocore/edk2/blob/2970e5699ba6267f3384ffab20f96647578aebc8/BaseTools/Source/C/GenFw/Elf32Convert.c)
- [OpenWrt checksum](https://downloads.openwrt.org/releases/25.12.5/targets/ramips/mt7621/sha256sums)
- [GCC MIPS options](https://gcc.gnu.org/onlinedocs/gcc/MIPS-Options.html)
- [GNU GRUB MIPS EFI machine convention](https://lists.gnu.org/archive/html/grub-devel/2017-02/msg00043.html)
