import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template_string, session
import threading, time, re

app = Flask(__name__)
app.secret_key = "무량공처_secret"  # 세션 사용 필수

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# 등록된 게스트 계정
GUEST_EMAILS = ["blahblahblahaa11@gmail.com", "gihoyeon78@gmail.com"]
GUEST_PASSWORDS = ["oovu clin ujlr zngg", "xnll gvua vaxy yclt"]

is_running = False
send_status_list = []
recent_target = ""

# 이메일 형식 검증
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# SMTP 로그인 확인
def check_smtp_login(email, password):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(email, password)
        return True
    except Exception:
        return False

# 이메일 전송 루프
def send_email_loop(receiver_email, accounts_with_pw):
    global is_running, send_status_list, recent_target
    count = 0
    recent_target = receiver_email
    try:
        while is_running:
            for email, password in accounts_with_pw:
                try:
                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                        server.starttls()
                        server.login(email, password)
                        count += 1
                        msg = MIMEText(f"미안하다, 아마나이. 난 지금 널 위해 화를 내는게 아니야. 나는 아무도 미워하지 않아. 지금은 그저 한없이 이 세계가 유쾌하다. [천상천하, 유아독존!] 대대로 전해 내려오는 전수 술식의 이점은 선대가 미리 구축해놓은 술식의 취급설명서가 있다는 것. 단점은 술식의 정보가 쉽게 새어나간다는 것. 당신, 젠인 가의 사람이지? 그러니 '창'과 '혁' 그리고 무하한 주술에 대한 것도 잘 아는 거겠지. 하지만 이건, 고죠 가문 안에사도 극히 일부의 인간만 아는 것이다. 순전과 반전. 각각의 무한을 충돌시킴으로써 생성되고, 가상의 질량을 밀어내는 허식(虚式), 자(紫); 🫸🔵 🔴🫷 🫴🟣 [{count}]")
                        msg['From'] = email
                        msg['To'] = receiver_email
                        msg['Subject'] = f"영역전개: 무량공처 [{count}]"
                        server.sendmail(email, receiver_email, msg.as_string())
                    send_status_list.append(f"{email}: 전송 성공 ({count})")
                except Exception as e:
                    send_status_list.append(f"{email}: 전송 실패 ({e})")
                time.sleep(0.2)
    finally:
        is_running = False

# HTML UI
html = ''' 
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>무량공처</title>
<style>
body { background: linear-gradient(135deg, #0f0f0f, #1a1a2e); font-family: 'Segoe UI', sans-serif; color:white; }
.container { background: rgba(255,255,255,0.05); backdrop-filter: blur(15px); padding: 40px; border-radius:20px; box-shadow:0 0 40px rgba(128,0,255,0.4); width:400px; margin:auto; margin-top:80px; }
h1 { margin-bottom:25px; font-weight:600; letter-spacing:2px; text-align:center; }
input[type="email"], input[type="password"] { width:100%; padding:12px; border-radius:10px; border:none; outline:none; margin-bottom:10px; background: rgba(255,255,255,0.1); color:white; }
button { width:100%; padding:12px; border-radius:10px; border:none; font-size:14px; cursor:pointer; margin-top:10px; transition:0.2s; }
button:hover { transform: scale(1.05); }
.status { margin-top:20px; font-size:14px; opacity:0.9; color:#ff6b6b; }
ul { padding-left:20px; max-height:150px; overflow-y:auto; }
li { font-size:13px; margin-bottom:3px; }
.target { margin-top:10px; font-size:13px; color:#c77dff; }
</style>
</head>
<body>
<div class="container">
<h1>무량공처</h1>

{% if step == 'select_mode' %}
<form method="POST">
    <label><input type="radio" name="mode" value="guest" required> 게스트 사용 (하루500통 제한)</label><br>
    <label><input type="radio" name="mode" value="personal" required> 개인계정 사용</label><br><br>
    <button type="submit" name="action" value="select_mode">선택</button>
</form>

{% elif step == 'personal_login' %}
<form method="POST">
    <input type="email" name="email1" placeholder="계정1 이메일" required value="{{ request.form.get('email1','') }}">
    <input type="password" name="pass1" placeholder="계정1 앱 비밀번호" required><br>
    <input type="email" name="email2" placeholder="계정2 이메일 (선택)" value="{{ request.form.get('email2','') }}">
    <input type="password" name="pass2" placeholder="계정2 앱 비밀번호 (선택)"><br>
    <button type="submit" name="action" value="login_personal">로그인 및 시작</button>
</form>
{% if login_error %}
<div class="status">{{login_error}}</div>
{% endif %}

{% elif step == 'email_sender' %}
<form method="POST">
    <input type="email" name="target_email" placeholder="대상 이메일" required>
    <button type="submit" name="action" value="start">영역 전개</button>
    <button type="submit" name="action" value="stop">영역 해제</button>
</form>
<form method="POST">
    <button type="submit" name="action" value="logout">계정 재선택</button>
</form>
<div class="status">영역 {{status}}</div>
{% if recent_target %}
<div class="target">최근 술식 대상: {{recent_target}}</div>
{% endif %}
{% if send_status_list %}
<ul>
{% for s in send_status_list %}
    <li>{{s}}</li>
{% endfor %}
</ul>
{% endif %}

{% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET','POST'])
def index():
    global is_running, send_status_list, recent_target
    status = "준비중"
    login_error = ""
    step = 'select_mode'

    mode = session.get('mode', None)
    accounts = session.get('accounts', [])

    if request.method == 'POST':
        action = request.form['action']

        if action == 'select_mode':
            mode = request.form['mode']
            session['mode'] = mode
            if mode == 'guest':
                # 게스트 계정은 미리 비밀번호 포함
                session['accounts'] = list(zip(GUEST_EMAILS, GUEST_PASSWORDS))
                step = 'email_sender'
            else:
                step = 'personal_login'

        elif action == 'login_personal':
            accounts_with_pw = []
            for i in [1,2]:
                email = request.form.get(f'email{i}')
                password = request.form.get(f'pass{i}')
                if email and password:
                    if not is_valid_email(email):
                        login_error = f"{email} 이메일 형식 오류"
                        step = 'personal_login'
                        return render_template_string(html, step=step, login_error=login_error)
                    if not check_smtp_login(email, password):
                        login_error = f"{email} 로그인 실패"
                        step = 'personal_login'
                        return render_template_string(html, step=step, login_error=login_error)
                    accounts_with_pw.append((email, password))
                elif email or password:
                    login_error = f"{email if email else '계정'+str(i)} 이메일과 비밀번호 모두 입력 필요"
                    step = 'personal_login'
                    return render_template_string(html, step=step, login_error=login_error)

            if not accounts_with_pw:
                login_error = "최소 1개 계정을 입력해야 합니다."
                step = 'personal_login'
            else:
                # 이메일만 세션 저장, 비밀번호는 즉시 사용
                session['accounts'] = [email for email, _ in accounts_with_pw]
                session['accounts_with_pw'] = accounts_with_pw
                step = 'email_sender'

        elif action == 'start':
            target_email = request.form.get('target_email')
            if not is_valid_email(target_email):
                login_error = "대상 이메일 형식 오류"
                step = 'email_sender'
                return render_template_string(html, step=step, status=status, send_status_list=send_status_list, login_error=login_error, recent_target=recent_target)

            if not is_running:
                is_running = True
                accounts_with_pw = session.get('accounts_with_pw', [])
                threading.Thread(target=send_email_loop, args=(target_email, accounts_with_pw)).start()
            status = "전개중"
            step = 'email_sender'

        elif action == 'stop':
            is_running = False
            status = "해제됨"
            step = 'email_sender'

        elif action == 'logout':
            session.pop('accounts', None)
            session.pop('accounts_with_pw', None)
            session.pop('mode', None)
            is_running = False
            send_status_list = []
            recent_target = ""
            step = 'select_mode'

    return render_template_string(html, step=step, status=status, send_status_list=send_status_list, login_error=login_error, recent_target=recent_target)

if __name__ == '__main__':
    app.run(debug=True)
