from pyngrok import ngrok
import os

# ایجاد تونل ngrok روی پورت 8000
public_url = ngrok.connect(8000)
print("🔗 لینک مشتری:", public_url)

# اجرای سرور جنگو روی پورت 8000
os.system("python manage.py runserver 8000")