# 今からどこいく？World Travel - 旅みくじ

「今からどこいく？World Travel」は、ボタン一つでランダムな旅先と同行者を提案する「旅みくじ」アプリケーションです。旅行先、イベント、お土産、同行者がランダムに組み合わされ、新しい旅のアイデアを提供します。

# Where to Next? World Travel - Travel Lottery

"Where to Next? World Travel" is a "Travel Lottery" application that suggests random travel destinations and companions with just one click. Travel destinations, events, souvenirs, and companions are randomly combined to provide new travel ideas.

## 特徴 / Features

### 日本語
- ボタン一つで旅みくじを引ける簡単操作
- 世界中の魅力的な場所をランダムに提案
- 各場所に関連したイベントとお土産を表示
- ランダムな同行者（ユウキ、アキラ、ミカ）を提案
- 場所に合わせた背景画像を自動表示
- モバイルフレンドリーなレスポンシブデザイン

### English
- Simple operation to draw a travel lottery with just one button
- Random suggestions of attractive places around the world
- Display of events and souvenirs related to each location
- Suggestion of random companions (Yuki, Akira, Mika)
- Automatic display of background images matching the location
- Mobile-friendly responsive design

## 必要条件 / Requirements

### 日本語
- Python 3.6以上
- Flask
- インターネット接続（画像表示のため）

### English
- Python 3.6 or higher
- Flask
- Internet connection (for displaying images)

## インストール方法 / Installation

### 日本語
1. リポジトリをクローンまたはダウンロードします
2. 必要なパッケージをインストールします：
   ```
   pip install flask
   ```
3. アプリケーションを実行します：
   ```
   python app.py
   ```
4. ブラウザで `http://localhost:5000` にアクセスします

### English
1. Clone or download the repository
2. Install the required packages:
   ```
   pip install flask
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access `http://localhost:5000` in your browser

## プロジェクト構造 / Project Structure

```
world_travel_web/
├── app.py              # Flaskアプリケーションのメインファイル / Main Flask application file
├── game_data.json      # ゲームデータ（場所、イベントなど） / Game data (locations, events, etc.)
├── static/
│   ├── css/
│   │   └── style.css   # CSSスタイルシート / CSS stylesheet
│   └── images/         # 画像ディレクトリ / Image directory
└── templates/          # HTMLテンプレート / HTML templates
    ├── index.html      # トップページ / Top page
    └── travel.html     # 旅みくじ結果ページ / Travel lottery result page
```

## 使い方 / How to Use

### 日本語
1. トップページの「🎲 旅みくじを引く」ボタンをクリック
2. ランダムな旅先、イベント、お土産、同行者が表示されます
3. 「もう一度旅みくじを引く」ボタンで新しい組み合わせを表示
4. 「ホームに戻る」ボタンでトップページに戻る

### English
1. Click the "🎲 Draw Travel Lottery" button on the top page
2. Random travel destination, event, souvenir, and companion will be displayed
3. Click "Draw Again" button to display a new combination
4. Click "Return to Home" button to go back to the top page

## デプロイ方法 / Deployment

### 日本語
本番環境にデプロイする場合は、以下のようなサービスを利用できます：

- Vercel
- PythonAnywhere
- AWS Elastic Beanstalk
- Google Cloud Run

デプロイ前に、`app.secret_key` を環境変数から取得するように変更し、`debug=False` に設定することをお勧めします。

### English
For deploying to a production environment, you can use services such as:

- Vercel
- PythonAnywhere
- AWS Elastic Beanstalk
- Google Cloud Run

Before deployment, it is recommended to change `app.secret_key` to be retrieved from environment variables and set `debug=False`.

## ライセンス / License

このプロジェクトは MIT ライセンスの下で公開されています。

This project is released under the MIT license.

## 作者 / Author

Hiro Ramos

---

楽しい旅のアイデアを見つけてください！🌍✈️

Find exciting travel ideas! 🌍✈️
