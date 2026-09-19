# 最小MIPS PE変換・配置・実行の記録

GenFwの入力全体完全一致ゲートを使う試験専用の変換。一般のMIPS ELF変換・再配置実装ではない。

- accepted.elf: 許可する入力全体。再リンクで内容が変われば拒否される。
- original.elf / minimal.S: .pdr再配置を含む元ELFとソース。
- observed.efi: ユーザーが生成・実行したPEの保存コピー。
- snapshot/ / genfw.patch: 現行GenFwソースとHEADとの差分。
- loader.c: Linuxユーザーモードの試験用ローダー。正確な最小命令列だけを許可。
- replay.py: GenFwのソース一致を確認して再ビルド、PE検査、ローダー再ビルド、正負の実行検査。
- verification.log / results/: 保存時の再検査ログと生成物。
- manifest.json: 実ソースHEAD、検査終了コード、保存物SHA-256。

再検査: `python /この保存フォルダ/replay.py`

現在のEDK II checkout、ホストgcc/make/Python、OpenWrtクロスツールチェーンが必要。EDK2_ROOT/STAGING_DIRでパス変更可。QEMUは保存したホスト用実行ファイルを使用し、ホスト共有ライブラリに依存する。自己完結した環境アーカイブではない。
prepare-fixture-gate.pyは当時の編集スクリプトの記録であり/tmp入力を参照する。再検査はreplay.pyを使用する。

Machine 0x0166はプロジェクト内の試験用選択。PE32/Subsystem 10/入口命令保持を検査する。Linux上でmmap、コピー、キャッシュ同期、mprotectを使って入口を呼ぶ。UEFI LoadImage/StartImage、一般PE再配置、DXE、実機起動は未検証。

前段のABI検査は ../mips-abi-20260919-190748/ を参照。コミット・pushは今回行わない。
