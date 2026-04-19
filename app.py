from flask import Flask, redirect, render_template, request, jsonify, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────
YOUR_EMAIL        = "jaimin.tailor123@gmail.com"          # your Gmail
YOUR_EMAIL_PASS   = "thph gyye kaxn smej"    # Gmail App Password (not your login password)


def send_email_alert(name, email, service, message):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚀 New Ingesify Lead: {name}"
    msg["From"]    = YOUR_EMAIL
    msg["To"]      = YOUR_EMAIL

    html = f"""
    <html><body style="font-family:sans-serif;color:#0f172a;">
      <h2 style="color:#1a56db;">New Contact Form Submission</h2>
      <table style="border-collapse:collapse;width:100%">
        <tr><td style="padding:8px;font-weight:600;width:120px">Name</td><td style="padding:8px">{name}</td></tr>
        <tr style="background:#f8faff"><td style="padding:8px;font-weight:600">Email</td><td style="padding:8px">{email}</td></tr>
        <tr><td style="padding:8px;font-weight:600">Service</td><td style="padding:8px">{service}</td></tr>
        <tr style="background:#f8faff"><td style="padding:8px;font-weight:600">Message</td><td style="padding:8px">{message}</td></tr>
      </table>
    </body></html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, YOUR_EMAIL_PASS)
        server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg.as_string())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    service = data.get('service', '')
    message = data.get('message', '')
    try:
        send_email_alert(name, email, service, message)
    except Exception as e:
        print(f"Email error: {e}")
        return redirect(url_for('admin'))
    # Here you would normally send an email or save to DB
    return jsonify({'status': 'success', 'message': f'Thanks {name}, we\'ll be in touch!'})

if __name__ == '__main__':
    app.run(debug=True)
