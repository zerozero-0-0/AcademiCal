# AcademiCal
課題の管理をCLI的に行うためのツール
Google Calendar apiを利用したdiscord bot

以下の機能を搭載する。
1. 課題の登録
各授業の終了後、discord channelに課題を登録するかどうかの通知を送る．
- 課題は課題名，課題内容，締め切り日時を持つ。
- 課題内容以外は空欄を認めない。
- 1日の終わり(21:00頃を想定)に今日出た課題と締め切りが近い課題が完了したかどうかの確認を行う。

課題の登録は上記の自動追加機能とともにコマンドでも登録できるようにする。流れは上記と同じ。


2. Google Calendarとの連携
課題の締切日をGoogle Calendarに登録する。
この機能を有効利用することで試験にも対応させる．

やりたいこと
sqlite3の導入
授業の時間割をデータで持つ。
授業後に通知を行う処理の追加。
課題の登録をコマンドで行えるようにする。



以下，実装済み機能
discord botの立ち上げ、チャンネルとの接続(07/08)
