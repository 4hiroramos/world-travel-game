@app.route('/travel')
def travel():
    """ランダムな旅行先と同行者を表示"""
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
    
    # ランダムな同行者を選択
    all_companions = COMPANIONS['duo'] + COMPANIONS['group']
    companion = random.choice(all_companions)
    
    # テンプレートに渡すデータ
    location = {
        'name': location_name,
        'event': event_description,
        'item': item_name
    }
    
    companion_data = {
        'name': companion['name'],
        'type': companion['personality']
    }
    
    return render_template(
        'travel.html',
        location=location,
        companion=companion_data
    )

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
