import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from keep_alive import keep_alive

app = Flask(__name__)
app.secret_key = 'super_secret_pos_key_render_2026'

# 簡易インメモリデータベース (初期ユーザー)
users_db = {
    "1001": {
        "username": "店長しゅん",
        "pin": "1234"
    }
}

@app.route('/')
def home():
    if 'staff_id' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        pin = request.form.get('pin')
        loylo_bypass = request.form.get('loylo_bypass')
        stealth_mode = request.form.get('stealth_mode')

        user = users_db.get(staff_id)

        if user and user['pin'] == pin:
            session['staff_id'] = staff_id
            session['username'] = user['username']
            session['loylo_status'] = "🛡️ ロイロ貫通" if loylo_bypass else "🟢 ロイロ通常"
            session['stealth_status'] = "🥷 授業中隠れモード" if stealth_mode else "通常動作"

            flash('ログインに成功しました！', 'success')
            return redirect(url_for('index'))
        else:
            flash('店員IDまたは店員PINが正しくありません。', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        username = request.form.get('username')
        pin = request.form.get('pin')

        if not staff_id or not username or not pin:
            flash('すべての項目を入力してください。', 'warning')
        elif staff_id in users_db:
            flash('この店員IDは既に登録されています。', 'danger')
        else:
            users_db[staff_id] = {
                "username": username,
                "pin": pin
            }
            flash(f'アカウント「{username}」(ID: {staff_id}) の作成が完了しました！ログインしてください。', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/index')
def index():
    if 'staff_id' not in session:
        flash('ログインしてください。', 'warning')
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('login'))

# Renderでの起動設定とKeep Alive開始
if __name__ == '__main__':
    keep_alive()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
