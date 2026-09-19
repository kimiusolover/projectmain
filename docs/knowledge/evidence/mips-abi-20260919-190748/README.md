# MIPS 最小ライブラリ・ABI検査の保存

保存元 HEAD: `debbfa2ede69e231b9199cce1de7657049e0873c`。未コミット変更込みの記録。指定対象コミット 2970e5699ba6267f3384ffab20f96647578aebc8 の検証ではない。

- snapshot/: 編集済み移植ソース、検査パッケージ、有効な設定。
- port.patch: HEAD に対する追跡ファイルの変更。新規ファイルは snapshot/ に保存。
- start.S / add-start.S / memcpy.c: Linux o32 ユーザーモード専用の検査補助。
- qemu-mipsel: 今回使用したホスト用エミュレーター。ホスト共有ライブラリに依存する。
- replay.sh: 現在の作業ツリーで検査モジュールをクリーン再ビルドし、加算・ABI検査を実行。
- verification.log / results/: 再検査ログと成果物。

再実行: `bash replay.sh`。EDK2_ROOT と STAGING_DIR で場所を変更可能。自動で snapshot を復元したり依存物を取得したりはしない。元の toolchain、Python、make、必要な submodule が必要。

検査対象: ProbeAdd(10,7)、64bit引数と戻り値、混在する可変引数、構造体の値渡しと戻り値、入口スタック整列。全ABIや実機動作の保証ではない。BaseTools全体のCツールビルド、ELF→PE、UEFI起動、実機、RFは未検証。

既存のBrotli submodule変更は状態のみ記録し、今回の移植パッチには含めない。コミット・pushは行っていない。
