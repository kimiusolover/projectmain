# R_MIPS_32 → HIGHLOW 限定試験

GenFwは以前の再配置なしELFと今回のELFの全バイト完全一致だけを許可する。一般MIPS移植・入力検証の完成ではない。

input.S/input.elf: 検査入力。observed.efi: ユーザー実行時の生成物。
snapshot/とgenfw.patch: 現行ソースとHEADとの差分。
loader.c: Linux o32検査ローダー。3セクションを配置しHIGHLOWを1件補正する。
replay.py: GenFwソース一致を確認、再ビルド・変換・ローダー再ビルド・正負検査。
verification.log/results/: 保存時の検査記録。
manifest.json: SHA-256と検査終了コード。

再検査は `python replay.py`。既存EDK II checkout、ホストgcc/make/Python、OpenWrtツールチェーン、前の保存フォルダ mips-pe-20260920-030858 のQEMUと最小PEローダーに依存する。EDK2_ROOT/STAGING_DIR/QEMU_MIPSELでパスを指定できる。自己完結環境ではない。編集補助スクリプトprepare-rel32-gate.pyは当時の記録で/tmpを参照する。

2領域を同時に保持し異なる配置先で補正済みポインターを検査ローダーが読み、0x12345678を確認する。PE入口はゼロを返すだけ。ページを共有する小さなセクションは補正後にまとめてRXへ変更するため、一般のPE権限制御ではない。

HIGHLOW種類変更・補正位置変更・再配置欠落を拒否。ELF再配置種類変更を完全一致ゲートで拒否。以前の再配置なし入力も変換・実行を再確認。

Machine 0x0166とHIGHLOWは今回の変換器・試験ローダーの契約。UEFI LoadImage/StartImage、HI16/LO16、一般再配置、実機は未検証。前段のABI/PE証拠は隣接フォルダ参照。
