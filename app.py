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

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def check_smtp_login(email, password):
    """실제 SMTP 로그인으로 앱 비밀번호 검증"""
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(email, password)
        return True
    except smtplib.SMTPAuthenticationError:
        return False
    except Exception:
        return False

def send_email_loop(receiver_email, sender_email, sender_password):
    global is_running, send_status_list, recent_target
    count = 0
    recent_target = receiver_email
    try:
        while is_running:
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)

                    count += 1
                    msg = MIMEText(f"미안하다,아마나이.난지금널위해화를내는게아니야.나는아무도미워하지않아.지금은그저한없이이세계가유쾌하다. [...] {count}")
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = f"영역전개: 무량공처\n{count}"
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                send_status_list.append(f"{sender_email}: 전송 성공 ({count})")
            except Exception as e:
                send_status_list.append(f"{sender_email}: 전송 실패 ({e})")
            time.sleep(0.2)
    finally:
        is_running = False

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
    <label><input type="radio" name="mode" value="guest" required> 게스트 사용 (하루500통 제한,다른 사람이 사용한 것도 포함.안되면 개인게정)</label><br>
    <label><input type="radio" name="mode" value="personal" required> 개인계정 사용</label><br><br>
    <button type="submit" name="action" value="select_mode">선택</button>
</form>

{% elif step == 'personal_login' %}
<form method="POST">
    <input type="email" name="email1" placeholder="계정1 이메일" required value="{{ request.form.get('email1','') }}">
    <input type="password" name="pass1" placeholder="계정1 앱 비밀번호" required value="{{ request.form.get('pass1','') }}"><br>
    <input type="email" name="email2" placeholder="계정2 이메일 (선택)" value="{{ request.form.get('email2','') }}">
    <input type="password" name="pass2" placeholder="계정2 앱 비밀번호 (선택)" value="{{ request.form.get('pass2','') }}"><br>
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

    accounts = session.get('accounts', [])
    mode = session.get('mode', None)

    if request.method == 'POST':
        action = request.form['action']

        if action == 'select_mode':
            mode = request.form['mode']
            session['mode'] = mode
            if mode == 'guest':
                session['accounts'] = list(zip(GUEST_EMAILS, GUEST_PASSWORDS))
                step = 'email_sender'
            elif mode == 'personal':
                step = 'personal_login'

        elif action == 'login_personal':
            accounts = []
            for i in [1,2]:
                e = request.form.get(f'email{i}')
                p = request.form.get(f'pass{i}')
                if e and p:
                    if not is_valid_email(e):
                        login_error = f"{e} 이메일 형식 오류"
                        step = 'personal_login'
                        return render_template_string(html, step=step, login_error=login_error)
                    if not check_smtp_login(e, p):
                        login_error = f"{e} 로그인 실패: 앱 비밀번호 확인 필요"
                        step = 'personal_login'
                        return render_template_string(html, step=step, login_error=login_error)
                    accounts.append((e,p))
                elif e or p:
                    login_error = f"{e if e else '계정'+str(i)} 이메일과 앱 비밀번호 모두 입력 필요"
                    step = 'personal_login'
                    return render_template_string(html, step=step, login_error=login_error)

            if not accounts:
                login_error = "최소 1개 계정을 입력해야 합니다."
                step = 'personal_login'
            else:
                session['accounts'] = accounts
                step = 'email_sender'

        elif action == 'start':
            send_status_list = []
            target_email = request.form.get('target_email')
            if not is_valid_email(target_email):
                login_error = "대상 이메일 형식 오류"
                step = 'email_sender'
                return render_template_string(html, step=step, status=status, send_status_list=send_status_list, login_error=login_error, recent_target=recent_target)
            if not is_running:
                is_running = True
                for email,password in session['accounts']:
                    threading.Thread(target=send_email_loop, args=(target_email,email,password)).start()
            status = "전개중"
            step = 'email_sender'

        elif action == 'stop':
            is_running = False
            status = "해제됨"
            step = 'email_sender'

        elif action == 'logout':
            session.pop('accounts', None)
            session.pop('mode', None)
            is_running = False
            send_status_list = []
            recent_target = ""
            step = 'select_mode'

    return render_template_string(html, step=step, status=status, send_status_list=send_status_list, login_error=login_error, recent_target=recent_target)

if __name__ == '__main__':
    app.run(debug=True)
