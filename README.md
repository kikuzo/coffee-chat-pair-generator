# coffee-chat-pair-generator
Coffee Chat用のランダムペア作成ツールです

## 環境変数
NOTION_API_TOKEN : Notionのページアクセス用のトークン

SLACK_CHANNEL : 結果をSlackに出力する場合の出力先チャネル

SLACK_HOOK_URL : 結果をSlackに出力する場合の出力先Webhook URL

## コマンドライン引数
Coffee Chatに参加する参加者が登録されているNotion Page idをコマンドライン引数で指定する

Slackへの出力したくない場合は該当コードをコメントアウトしてください(デフォルト:出力する)
