import telebot
import requests

# Token Bot Telegram của bạn
API_TOKEN = '7980786326:AAGPL6OQEAhTQLuNKE9pK0ai4BA8LaCw6R8'
bot = telebot.TeleBot(API_TOKEN)

def check_token(token):
    # Gửi yêu cầu đến API Discord để lấy thông tin tài khoản
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("username", "Không xác định")
            discriminator = user_data.get("discriminator", "0000")
            user_id = user_data.get("id", "N/A")
            return f"✅ **Token LIVE**\n👤 User: `{username}#{discriminator}`\n🆔 ID: `{user_id}`"
        elif response.status_code == 401:
            return "❌ **Token DIE** (Sai hoặc đã bị khóa)"
        else:
            return f"⚠️ **Lỗi:** Discord trả về mã {response.status_code}"
    except Exception as e:
        return f"⚠️ **Lỗi kết nối:** {str(e)}"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(m):
    bot.reply_to(m, "Chào bạn! Hãy gửi cho mình dải **Token Discord** để mình check xem nó còn sống hay đã chết nhé.")

@bot.message_handler(func=lambda m: True)
def handle_token(m):
    # Lấy nội dung tin nhắn (giả định mỗi dòng là 1 token hoặc chỉ gửi 1 token)
    tokens = m.text.strip().split('\n')

    for t in tokens:
        t = t.strip()
        if len(t) < 20: # Kiểm tra độ dài cơ bản của token
            bot.reply_to(m, f"❓ `{t}`: Định dạng không giống Token Discord.")
            continue

        bot.reply_to(m, f"⏳ Đang check token: `{t[:15]}...`")
        result = check_token(t)
        bot.reply_to(m, result, parse_mode='Markdown')

print("Bot Check Token đang chạy...")
bot.infinity_polling()
