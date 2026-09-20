# MIPS HI16/LO16 exact-fixture evidence

2026-09-20 に保存。一般的な MIPS ELF 変換ではなく、バイト完全一致で許可した4入力の試験です。
PE Machine 0x0166 はこのプロジェクトの試験上の扱いです。UEFI ブート、実機、汎用再配置対応の証拠ではありません。

## 確認結果

- 通常入力の ProbeValue は 0x00410100、境界入力は 0x00418000。
- 境界入力の命令は `lui t0,0x42; lw v0,-32768(t0); jr ra; nop`。
- GenFw は ELF の配置を PE RVA へ補正し、HIGHADJ（追加WORDに元のLOWを格納）と LOW を出力。
- 保存したソースから GenFw を再ビルドし、両入力をアセンブリから再生成してバイト一致を確認。
- 両入力について3配置先の再配置計算を検査。
- 両入力について Linux user-mode QEMU で MIPS コードを実行。データアドレス下位16bitの符号が異なる2配置先で、0x12345678 を返すことを確認。
- 入力ELFの改変2件を拒否。既存の Minimal / Rel32 入力も変換成功。
- PEの不正な型、HIGHADJ付随値、LOW欠落、HIGHADJ対象の4件を拒否。
- 実行時の下位16bitは 0x0240 / 0x8240。実行時にちょうど 0x8000 へ配置した検査ではない。入力ELF側でちょうど 0x8000 を検査している。

## 再実行

このディレクトリで `python3 replay.py` を実行する。
任意の場所からはこのディレクトリの replay.py の絶対パスを指定できる。
最後の `PASS: replay complete (exact fixtures; Linux user-mode QEMU only)` と終了コード0が成功条件。

依存: Linux x86_64、Python 3、make、/usr/bin/gcc、/usr/bin/g++、libuuid開発ヘッダ・ライブラリ、および manifest.json に記録された OpenWrt クロスツールチェーン。
ツールチェーンの場所は STAGING_DIR で変更可能だが、gcc/ld/as のハッシュ一致が必要。
ツールチェーン全体は同梱せず、記録した実行ファイルのハッシュ検査は配布アーカイブ全体の検証を代替しない。
QEMU は tools/qemu-mipsel に同梱。外部の過去証拠ディレクトリや /tmp の元ファイルには依存しない。
ビルドと実行結果は新しい一時ディレクトリに生成し、終了時に削除する。
保存する場合は `HILO_OUTPUT=/新規出力先 python3 replay.py` を使用。出力先は存在しないこと。

## 内容

- inputs/: アセンブリと通常・境界ELF
- snapshot/: 現在の BaseTools ソースと MdePkg/Include。再実行はこのコピーを利用し、元チェックアウトを変更しない
- loader-hilo.c: HIGHADJ/LOW試験専用ローダー。LUI/LW/JR/NOPと再配置対象を限定
- genfw-hilo.diff / Elf32Convert.c.before-hilo-fixtures: 今回の変更差分と変更直前ソース
- observed/: 当時の生成物。user-boundary.efi はユーザーが生成したファイル
- results/: 保存時の再実行で生成した検査用成果物
- verification.log: 再ビルド・検査コマンド、結果、QEMUの実行結果
- *-status.txt / *-head.txt / *-diff.txt / *-submodules.txt: 保存前のGit状態（今回と無関係な既存変更を含む）
- manifest.json: 保存ファイルのSHA-256。manifest自体は対象外

親リポジトリとEDK IIチェックアウトには既存の未コミット変更がある。保存操作ではコミット・pushしていない。
