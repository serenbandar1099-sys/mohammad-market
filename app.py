from flask import Flask, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

CORRECT_PHONE = "0786008481"
JSON_FILE = "numbers.json"

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>أسواق محمد الراعي</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: "Tahoma", Arial, sans-serif;
            background:
                radial-gradient(circle at top right, rgba(255, 215, 0, 0.20), transparent 30%),
                linear-gradient(135deg, #0f172a, #1e3a8a, #0f172a);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #111827;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 460px;
        }

        .brand {
            text-align: center;
            color: white;
            margin-bottom: 25px;
        }

        .brand h1 {
            margin: 0;
            font-size: 42px;
            font-weight: 900;
            letter-spacing: -1px;
        }

        .brand p {
            margin-top: 10px;
            font-size: 17px;
            color: #dbeafe;
        }

        .card {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 26px;
            padding: 30px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255,255,255,0.5);
        }

        .badge {
            width: fit-content;
            margin: 0 auto 18px;
            background: #fef3c7;
            color: #92400e;
            padding: 8px 16px;
            border-radius: 999px;
            font-weight: bold;
            font-size: 14px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-size: 17px;
            font-weight: bold;
            color: #1f2937;
        }

        .input-box {
            position: relative;
        }

        input {
            width: 100%;
            padding: 16px;
            font-size: 20px;
            border-radius: 16px;
            border: 2px solid #e5e7eb;
            outline: none;
            text-align: center;
            direction: ltr;
            transition: 0.25s;
        }

        input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
        }

        button {
            width: 100%;
            margin-top: 18px;
            padding: 16px;
            font-size: 19px;
            font-weight: bold;
            background: linear-gradient(135deg, #2563eb, #1e40af);
            color: white;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            transition: 0.25s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(37, 99, 235, 0.35);
        }

        .message {
            margin-top: 20px;
            padding: 16px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
        }

        .error {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }

        .success {
            background: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
            line-height: 2;
        }

        .result-card {
            margin-top: 18px;
            background: #f8fafc;
            border-radius: 18px;
            padding: 18px;
            border: 1px solid #e5e7eb;
        }

        .row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
            font-size: 18px;
        }

        .row:last-child {
            border-bottom: none;
        }

        .value {
            font-weight: 900;
            color: #1e40af;
        }

        .footer {
            margin-top: 18px;
            text-align: center;
            color: #6b7280;
            font-size: 13px;
        }

        @media (max-width: 500px) {
            .brand h1 {
                font-size: 32px;
            }

            .card {
                padding: 24px;
            }
        }
    </style>
</head>

<body>
    <div class="container">

        <div class="brand">
            <h1>أسواق محمد الراعي</h1>
            <p>نظام الاستعلام عن النقاط</p>
        </div>

        <div class="card">
            <div class="badge">برنامج النقاط</div>

            <form method="POST">
                <label>أدخل رقم الهاتف الأردني</label>

                <div class="input-box">
                    <input
                        type="text"
                        name="phone"
                        placeholder="07XXXXXXXX"
                        maxlength="10"
                        required
                    >
                </div>

                <button type="submit">استعلام الآن</button>
            </form>

            {% if error %}
                <div class="message error">
                    {{ error }}
                </div>
            {% endif %}

            {% if success %}
                <div class="message success">
                    تم العثور على الحساب بنجاح
                </div>

                <div class="result-card">
                    <div class="row">
                        <span>الاسم</span>
                        <span class="value">عمر الوريكات</span>
                    </div>

                    <div class="row">
                        <span>النقاط</span>
                        <span class="value">250 نقطة</span>
                    </div>

                    <div class="row">
                        <span>رقم الهاتف</span>
                        <span class="value">{{ phone }}</span>
                    </div>
                </div>
            {% endif %}

            <div class="footer">
                جميع الحقوق محفوظة © أسواق محمد الراعي
            </div>
        </div>

    </div>
</body>
</html>
"""

def save_number(phone):
    data = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    record = {
        "phone": phone,
        "name": "عمر الوريكات",
        "points": 250,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data.append(record)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    success = False
    phone = ""

    if request.method == "POST":
        phone = request.form.get("phone", "").strip()

        if phone == CORRECT_PHONE:
            save_number(phone)
            success = True
        else:
            error = "عذرًا، الرقم غير صحيح. تأكد من الرقم وحاول مرة أخرى."

    return render_template_string(
        HTML,
        error=error,
        success=success,
        phone=phone
    )


if __name__ == "__main__":
    app.run(debug=True)