### زبان: Python ###
from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
import requests  # این کتابخانه برای پروکسی ضروری است

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_webgis'

# دیتابیس موقت کاربران (برای تست)
users = {'mary': '123456'}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('map_view'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('map_view'))
        else:
            return "نام کاربری یا رمز عبور اشتباه است", 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "این نام کاربری قبلاً گرفته شده است", 400
        users[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/map')
def map_view():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('map.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# ---------------------------------------------------------
# بخش حیاتی: پروکسی سرور برای دور زدن محدودیت‌های مرورگر
# ---------------------------------------------------------
@app.route('/proxy_wms')
def proxy_wms():
    # آدرس اصلی سرور خارجی GeoServer
    target_url = "https://ahocevar.com/geoserver/wms"
    
    # تمام پارامترهای دریافتی از نقشه (مثل زوم، مختصات و ...) را می‌گیریم
    params = request.args.to_dict()
    
    try:
        # درخواست را از طریق پایتون ارسال می‌کنیم
        # نکته: اگر VPN روی سیستم دارید، پایتون معمولا از آن استفاده می‌کند
        resp = requests.get(target_url, params=params, timeout=10)
        
        # پاسخ سرور خارجی را دقیقاً به مرورگر برمی‌گردانیم
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
