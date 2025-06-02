from flask import Flask, render_template, url_for
import random
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))  # 環境変数から取得、なければランダム生成

# ゲームデータの読み込み
try:
    game_data_path = os.path.join(os.path.dirname(__file__), 'game_data.json')
    with open(game_data_path, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
except Exception as e:
    print(f"Error loading game data: {e}")
    # エラー時のフォールバックデータ
    game_data = {"locations": {
        "東京": {
            "name": "東京",
            "description": "現代的な超高層ビルと伝統的な寺社が共存する日本の首都。",
            "options": ["京都", "バンコク", "ニューヨーク"],
            "image_filename": "tokyo.jpg",
            "special_events": []
        }
    }}

@app.route('/')
def index():
    """トップページ表示"""
    return render_template('index.html')

@app.route('/travel')
def travel():
    """ランダムな旅行先と同行者を表示"""
    try:
        # ランダムな場所を選択
        location_name = random.choice(list(game_data['locations'].keys()))
        location_data = game_data['locations'][location_name]
        
        # ランダムなイベントを選択
        event = None
        if location_data['special_events']:
            event = random.choice(location_data['special_events'])
            event_description = event['description']
        else:
            event_description = "特別なイベントはありません"
        
        # 旅先ごとのお土産リスト
        souvenirs = {
            "東京": ["東京バナナ", "スカイツリーの模型", "浅草の雷おこし", "招き猫の置物", "江戸切子のグラス"],
            "京都": ["八つ橋", "京扇子", "清水焼の茶碗", "西陣織のポーチ", "抹茶スイーツセット"],
            "バンコク": ["象のお守り", "タイシルクのストール", "トムヤムクンの調味料セット", "パクチーせんべい", "ムエタイのミニグローブ"],
            "ニューヨーク": ["自由の女神の置物", "I♥NYTシャツ", "ブロードウェイのチケットの半券", "NYヤンキースの帽子", "マンハッタンのジオラマ"],
            "パリ": ["エッフェル塔のミニチュア", "マカロン詰め合わせ", "ベレー帽", "フランス産チーズセット", "高級ワイン"],
            "バリ島": ["バティック織物", "木彫りの仮面", "アロマオイルセット", "南国フルーツのドライフルーツ", "ガムランの楽器"],
            "カイロ": ["パピルスの絵画", "スフィンクスの置物", "エジプト綿のタオル", "砂漠のサンドアート", "ナツメヤシのお菓子"],
            "リオデジャネイロ": ["カーニバルの羽飾り", "サンバCDコレクション", "ブラジルコーヒー豆", "ハバイアナスのビーチサンダル", "サッカーボール"],
            "シドニー": ["コアラのぬいぐるみ", "ブーメラン", "オーストラリアンワイン", "UGGブーツのミニチュア", "オパールのアクセサリー"],
            "ローマ": ["コロッセオの模型", "本格パスタセット", "バチカン美術館の図録", "イタリアンレザーの小物", "ローマ帝国のコイン（レプリカ）"],
            "サントリーニ": ["青と白の陶器", "地中海の塩", "ギリシャオリーブオイル", "ワインボトル", "エーゲ海の写真集"],
            "マチュピチュ": ["アルパカのセーター", "インカ帝国の地図", "ペルー産チョコレート", "民族楽器のケーナ", "カラフルな織物"],
            "サファリパーク": ["動物フィギュアセット", "サファリハット", "野生動物の写真集", "アフリカンドラムのミニチュア", "マサイ族のビーズアクセサリー"]
        }
        
        # 選択された場所に対応するお土産リストからランダムに選択
        if location_name in souvenirs:
            item_name = random.choice(souvenirs[location_name])
        else:
            # リストにない場所の場合はデフォルト
            item_name = f"{location_name}のお土産"
        
        # 同行者データを定義
        companions = [
            {"name": "ユウキ", "type": "写真好き"},
            {"name": "アキラ", "type": "冒険好き"},
            {"name": "ミカ", "type": "グルメ好き"}
        ]
        
        # ランダムな同行者を選択
        companion = random.choice(companions)
        
        # 場所の画像URLを生成
        try:
            # game_data.jsonから直接image_filenameを取得
            image_filename = location_data['image_filename']
            # 絶対URLを生成
            image_url = f"/static/images/locations/{image_filename}"
            print(f"Generated image URL: {image_url} for location: {location_name}")
        except Exception as e:
            print(f"Error generating image URL: {e}")
            # エラー時はデフォルト画像を使用
            image_url = "/static/images/locations/default.jpg"
        
        # テンプレートに渡すデータ
        location = {
            'name': location_name,
            'event': event_description,
            'item': item_name
        }
        
        return render_template(
            'travel.html',
            location=location,
            companion=companion,
            image_url=image_url
        )
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 500

if __name__ == '__main__':
    # 開発環境ではdebug=True、本番環境ではFalseに
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
