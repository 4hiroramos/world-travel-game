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
            "image": "tokyo.jpg",
            "special_events": []
        }
    }}

def get_location_image_filename(location_name):
    """場所の名前から画像ファイル名を生成する"""
    # 日本語名を英語名に変換するマッピング
    name_mapping = {
        "東京": "tokyo",
        "京都": "kyoto",
        "バンコク": "bangkok",
        "ニューヨーク": "newyork",
        "パリ": "paris",
        "バリ島": "bali",
        "カイロ": "cairo",
        "リオデジャネイロ": "rio",
        "シドニー": "sydney",
        "ローマ": "rome",
        "サントリーニ": "santorini",
        "マチュピチュ": "machupicchu",
        "サファリパーク": "safari"
    }
    
    # マッピングにある場合はそれを使用、なければ名前をローマ字化して小文字に
    filename = name_mapping.get(location_name, location_name.lower())
    # スペースや特殊文字を除去
    filename = ''.join(c for c in filename if c.isalnum())
    return f"{filename}.jpg"

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
        
        # ランダムなアイテム名を生成
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
            image_filename = get_location_image_filename(location_name)
            # 画像ファイルが存在するかチェック
            image_path = os.path.join(os.path.dirname(__file__), f'static/images/locations/{image_filename}')
            if os.path.exists(image_path):
                image_url = url_for('static', filename=f'images/locations/{image_filename}')
            else:
                # 画像が存在しない場合はUnsplashから直接取得
                image_url = f"https://source.unsplash.com/800x450/?landmark,{location_name.lower()}"
        except Exception as e:
            print(f"Error generating image URL: {e}")
            # エラー時はデフォルト画像を使用
            image_url = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&h=450&q=80"
        
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
