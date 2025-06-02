from flask import Flask, render_template, request, session, redirect, url_for
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

# 同行者データ
COMPANIONS = {
    'duo': [
        {
            "name": "ユウキ",
            "personality": "冒険好き",
            "personality_type": "adventure",
            "icon": "hiking",
            "description": "新しい体験を求める冒険家。危険を顧みず、常に刺激を求めています。",
            "favorite_places": ["マチュピチュ", "サファリパーク", "リオデジャネイロ"],
            "relationship": 50,
            "suggestions": ["サファリパーク", "マチュピチュ"]
        }
    ],
    'group': [
        {
            "name": "ユウキ",
            "personality": "冒険好き",
            "personality_type": "adventure",
            "icon": "hiking",
            "description": "新しい体験を求める冒険家。危険を顧みず、常に刺激を求めています。",
            "favorite_places": ["マチュピチュ", "サファリパーク", "リオデジャネイロ"],
            "relationship": 50,
            "suggestions": ["サファリパーク", "マチュピチュ"]
        },
        {
            "name": "アキラ",
            "personality": "写真好き",
            "personality_type": "photo",
            "icon": "camera",
            "description": "一瞬の美しさを写真に収めるのが得意。風景や建築物の写真を撮るのが大好きです。",
            "favorite_places": ["サントリーニ", "京都", "パリ"],
            "relationship": 50,
            "suggestions": ["サントリーニ", "京都"]
        },
        {
            "name": "ミカ",
            "personality": "グルメ好き",
            "personality_type": "food",
            "icon": "utensils",
            "description": "世界中の美食を探求する食通。地元の料理を試すことで文化を理解しようとします。",
            "favorite_places": ["バンコク", "ローマ", "東京"],
            "relationship": 50,
            "suggestions": ["バンコク", "ローマ"]
        }
    ]
}

@app.route('/')
def index():
    """トップページ表示"""
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    """ゲーム開始処理"""
    player_name = request.form.get('player_name', 'ゲスト')
    travel_type = request.form.get('travel_type', 'solo')
    
    # 旅の種類に応じて同行者を設定
    companions = []
    if travel_type == 'duo':
        companions = COMPANIONS['duo']
    elif travel_type == 'group':
        companions = COMPANIONS['group']
    
    # セッションの初期化
    session['player'] = {
        'name': player_name,
        'visited': ['東京'],  # 最初は東京からスタート
        'items': [],
        'photos': []
    }
    session['travel_type'] = travel_type
    session['companions'] = companions
    session['current_location'] = '東京'
    session['event_shown'] = False  # イベント表示フラグ
    session['suggestions_shown'] = False  # 提案表示フラグ
    
    return redirect(url_for('location'))

@app.route('/location')
def location():
    """現在地の表示"""
    if 'player' not in session:
        return redirect(url_for('index'))
    
    current = session['current_location']
    location_data = game_data['locations'][current]
    travel_type = session.get('travel_type', 'solo')
    companions = session.get('companions', [])
    
    # 同行者の提案を処理
    companion_suggestions = []
    if travel_type != 'solo' and not session.get('suggestions_shown', False):
        for companion in companions:
            # 現在地が同行者のお気に入りの場所なら関係性を向上
            if current in companion['favorite_places']:
                companion['relationship'] = min(100, companion['relationship'] + 10)
                companion_suggestions.append({
                    'name': companion['name'],
                    'message': f"「{current}は私のお気に入りの場所です！ありがとう！」"
                })
            
            # ランダムで提案を表示
            if random.random() < 0.3 and companion['suggestions']:
                suggestion = random.choice(companion['suggestions'])
                if suggestion not in location_data['options'] and suggestion != current:
                    # 提案を選択肢に追加
                    location_data['options'].append(suggestion)
                    companion_suggestions.append({
                        'name': companion['name'],
                        'message': f"「{suggestion}に行ってみませんか？面白そうですよ！」"
                    })
        
        if companion_suggestions:
            session['suggestions_shown'] = True
    
    # イベント発生判定
    event = None
    if not session.get('event_shown', False) and location_data['special_events']:
        # 旅の種類に応じたイベントを選択
        suitable_events = []
        for e in location_data['special_events']:
            # イベントに適合条件がなければ全ての旅タイプで使用可能
            if 'suitable_for' not in e:
                suitable_events.append(e)
            # 適合条件があれば、現在の旅タイプが含まれているか確認
            elif travel_type in e.get('suitable_for', []):
                suitable_events.append(e)
        
        if suitable_events and random.random() < 0.7:
            event = random.choice(suitable_events)
            
            # 旅の種類に応じてイベント内容を調整
            if travel_type != 'solo':
                # 同行者をランダムに選択
                companion = random.choice(companions)
                
                # イベント説明文の中の{{companion}}を同行者の名前に置き換え
                if '{{companion}}' in event['description']:
                    event['description'] = event['description'].replace('{{companion}}', companion['name'])
                
                # 同行者の性格に応じた選択肢を追加
                personality = companion['personality_type']
                if f"{personality}_choice" in event and f"{personality}_outcome" in event:
                    event['choices'].append(event[f"{personality}_choice"])
                    event['outcomes'].append(event[f"{personality}_outcome"])
                    event['companion_choice'] = True
                    event['companion_name'] = companion['name']
                    event['companion_personality'] = personality
            
            session['current_event'] = event
            session['event_shown'] = True
    
    # 同行者の情報をセッションに保存
    if travel_type != 'solo':
        session['companions'] = companions
    
    return render_template(
        'location.html',
        location=location_data,
        current=current,
        player=session['player'],
        travel_type=travel_type,
        companions=companions,
        event=event,
        options=location_data['options'],
        companion_suggestions=companion_suggestions
    )

@app.route('/event_choice', methods=['POST'])
def event_choice():
    """イベントの選択処理"""
    if 'current_event' not in session:
        return redirect(url_for('location'))
    
    choice_idx = int(request.form.get('choice', 0))
    event = session['current_event']
    outcome = event['outcomes'][choice_idx]
    
    # 同行者の関係性を更新
    travel_type = session.get('travel_type', 'solo')
    if travel_type != 'solo' and 'companion_choice' in event and choice_idx == len(event['choices']) - 1:
        companions = session.get('companions', [])
        for companion in companions:
            if companion['name'] == event.get('companion_name'):
                # 同行者の提案を選んだ場合、関係性が向上
                companion['relationship'] = min(100, companion['relationship'] + 15)
                break
        session['companions'] = companions
    
    # イベント結果に応じてアイテムや写真を追加
    if "写真" in outcome:
        photo = f"{session['current_location']}の写真"
        session['player']['photos'].append(photo)
    
    if "お土産" in outcome or "特別な" in outcome:
        item = f"{session['current_location']}のお土産"
        session['player']['items'].append(item)
    
    # イベント完了フラグをリセット
    session['event_shown'] = False
    del session['current_event']
    
    return render_template(
        'event_result.html', 
        outcome=outcome, 
        current=session['current_location'],
        travel_type=travel_type,
        companions=session.get('companions', [])
    )

@app.route('/move', methods=['POST'])
def move():
    """移動処理"""
    if 'player' not in session:
        return redirect(url_for('index'))
    
    destination = request.form.get('destination')
    
    # 有効な移動先かチェック
    current = session['current_location']
    if destination in game_data['locations'][current]['options'] or destination in [s for c in session.get('companions', []) for s in c.get('suggestions', [])]:
        session['current_location'] = destination
        
        # 訪問リストに追加（重複なし）
        if destination not in session['player']['visited']:
            session['player']['visited'].append(destination)
        
        # イベントフラグとサジェスションフラグをリセット
        session['event_shown'] = False
        session['suggestions_shown'] = False
    
    return redirect(url_for('location'))

@app.route('/inventory')
def inventory():
    """持ち物リスト表示"""
    if 'player' not in session:
        return redirect(url_for('index'))
    
    return render_template(
        'inventory.html', 
        player=session['player'],
        travel_type=session.get('travel_type', 'solo'),
        companions=session.get('companions', [])
    )

@app.route('/visited')
def visited():
    """訪問場所リスト表示"""
    if 'player' not in session:
        return redirect(url_for('index'))
    
    completion = len(session['player']['visited']) / len(game_data['locations']) * 100
    
    return render_template(
        'visited.html', 
        player=session['player'],
        completion=completion,
        travel_type=session.get('travel_type', 'solo'),
        companions=session.get('companions', [])
    )

@app.route('/companions')
def companions():
    """同行者情報表示"""
    if 'player' not in session or session.get('travel_type', 'solo') == 'solo':
        return redirect(url_for('location'))
    
    return render_template(
        'companions.html',
        player=session['player'],
        travel_type=session.get('travel_type', 'solo'),
        companions=session.get('companions', [])
    )

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
        
        # テンプレートに渡すデータ
        location = {
            'name': location_name,
            'event': event_description,
            'item': item_name
        }
        
        return render_template(
            'travel.html',
            location=location,
            companion=companion
        )
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 500

@app.route('/end_game')
def end_game():
    """ゲーム終了処理"""
    if 'player' not in session:
        return redirect(url_for('index'))
    
    player_data = session['player']
    completion = len(player_data['visited']) / len(game_data['locations']) * 100
    
    # 同行者情報を取得
    travel_type = session.get('travel_type', 'solo')
    companions = session.get('companions', [])
    
    # セッションをクリア
    session.clear()
    
    return render_template(
        'end_game.html', 
        player=player_data, 
        completion=completion,
        travel_type=travel_type,
        companions=companions
    )

if __name__ == '__main__':
    # 開発環境ではdebug=True、本番環境ではFalseに
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
