# Starscope
starscopeは星を眺めることが好きな方々向けのブログです。  
コメント、写真の投稿、好きな場所をリストにセーブする機能、レビュー機能を実装しております。


# URL
https://starscope.ga


# 使用技術
- プロントエンド
  - HTML/CSS
  - Javascipt(翻訳機能)
  - Django templates



- バックエンド
  - Python 3.9.1
  - Django 2.2.5

- インフラ
  - Docker / Docker swarm
  - AWS (EC2 / RDS(MySQL) / S3 / VPC / IAM / Route53 / ACM / ALB)
  - Nginx
  - Gunicorn

# ER図
# AWS構成図
<img src="https://user-images.githubusercontent.com/66953834/135719247-82fa40e1-a904-427b-b981-c9301e40b219.png" />

# 機能一覧

- 基本機能
  - 新規会員登録　・　ログイン機能
  - ソーシャルログイン機能(Github, Line, Kakao talk)
  - プロフィール機能(名前、国、性別、自己紹介、生年月日、カレンシー編集可能、自分が生成した場所のリスト一覧)

- 投稿機能
  - 場所の名前、説明、位置(国、都市、住所)、写真の登録、編集、削除

- 検索機能

- レビュー機能

- メッセージ機能(投稿者と会話)

- お気に入り機能(気に入った場所をリストに追加)

- 翻訳機能(日本語、英語選択可能)

# 今後の修正計画
- google map機能追加
- 天体観測API追加
- AWS public, private subnet 分離
- 検索機能修正
- イメージ追加方法変更
- 再コメント機能追加
- Circle CI投入