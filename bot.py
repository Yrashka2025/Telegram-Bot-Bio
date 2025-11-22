import telebot
import requests
from telebot import types

TOKEN = "" #Here you bot Token from @DotFather
bot = telebot.TeleBot(TOKEN)

def get_github_stats(username):
    try:
        # Get user basic info
        user_response = requests.get(f"https://api.github.com/users/{username}")
        if user_response.status_code != 200:
            return None

        user_data = user_response.json()
        public_repos = user_data.get('public_repos', 0)
        followers = user_data.get('followers', 0)
        following = user_data.get('following', 0)
        created_at = user_data.get('created_at', "Unknown")

        # Get public repositories to find top repo and total stars
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&type=public&sort=updated"
        repos_response = requests.get(repos_url)
        total_stars = 0
        top_repo = None
        max_stars = -1
        languages = {}

        if repos_response.status_code == 200:
            repos = repos_response.json()
            for repo in repos:
                stars = repo.get('stargazers_count', 0)
                total_stars += stars
                if stars > max_stars:
                    max_stars = stars
                    top_repo = {
                        'name': repo.get('name', 'Unknown'),
                        'stars': stars,
                        'url': repo.get('html_url', '')
                    }
                # Fetch languages for each repo (if few repos to avoid rate limits)
                if len(repos) <= 10:
                    lang_url = repo.get('languages_url')
                    if lang_url:
                        lang_resp = requests.get(lang_url)
                        if lang_resp.status_code == 200:
                            repo_langs = lang_resp.json()
                            for lang, bytes_count in repo_langs.items():
                                languages[lang] = languages.get(lang, 0) + bytes_count

        # Get top languages
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3] if languages else []

        return {
            'username': user_data.get('login', username),
            'repos': public_repos,
            'followers': followers,
            'following': following,
            'created_at': created_at,
            'total_stars': total_stars,
            'top_repo': top_repo,
            'top_languages': top_languages
        }
    except Exception as e:
        return None


@bot.message_handler(commands=['start']) 
def send_welcome(message):  
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("projects", callback_data="projects"))
    markup.add(types.InlineKeyboardButton("About me", callback_data="about_me"))
    markup.add(types.InlineKeyboardButton("Sourse Code", callback_data= "sourse_code"))
    markup.add(types.InlineKeyboardButton("Social Links", callback_data="social_test"))

    bot.send_message(message.chat.id, "Select one button:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'about_me':
        bot.answer_callback_query(call.id, "About me:\nName: Yrashka\nAge: 16 y.0\nProgramming languages: Python, HTML, СSS (styding now) ")
    if call.data == 'sourse_code':
        try:
            with open('bot.py', 'rb') as script_file:
                bot.send_document(
                    call.message.chat.id,
                    document=script_file,
                    caption="Here's your file! 📁"
                )
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, "I don't see file!")
        bot.answer_callback_query(call.id)

    if call.data == 'social_test':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Insta", "https://www.instagram.com/yrashka200"))
        markup.add(types.InlineKeyboardButton("Bluesky", "https://bsky.app/profile/yrashka.bsky.social"))
        markup.add(types.InlineKeyboardButton("Github Profile", "https://github.com/Yrashka2025"))
        markup.add(types.InlineKeyboardButton("Github Stats", callback_data="github_stats"))

        bot.send_message(call.message.chat.id, "Here's links:", reply_markup=markup)
        bot.answer_callback_query(call.id)

    if call.data == 'projects':
        bot.answer_callback_query(call.id, "1. https://github.com/Yrashka2025/Web-Portfolio - Web Portfolio\n2. This bot-potfolio (Sourse code in start menu buttons) ")

    if call.data == 'github_stats':
        stats = get_github_stats("")  # Your Github username 
    
    if stats:
        top_repo_str = ""
        if stats.get('top_repo'):
            top_repo = stats['top_repo']
            top_repo_str = f"\n*🔥 Most starred repo:*\n[{top_repo['name']}]({top_repo['url']}) (⭐ {top_repo['stars']})"
        else:
            top_repo_str = "\n*🔥 Most starred repo:* None"

        lang_str = ""
        if stats.get('top_languages'):
            langs = [lang for lang, _ in stats['top_languages']]
            lang_str = f"\n*💻 Top Languages:* {', '.join(langs)}"
        else:
            lang_str = "\n*💻 Top Languages:* None"

        stats_text = f"""
📊 *GitHub Statistics

User: {stats['username']}
📁 Public Repositories:* {stats['repos']}
Followers:* {stats['followers']}
Following:* {stats['following']}
✨ Total Stars:* {stats['total_stars']}{lang_str}
📅 Profile created:* {stats['created_at']}{top_repo_str}
"""
    else:
        stats_text = "❌ Couldn't fetch GitHub data at the moment"

    # Кнопка для обновления статистики
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Refresh Stats", callback_data="github_stats"))
    markup.add(types.InlineKeyboardButton("← Back", callback_data="social_test"))

    bot.send_message(call.message.chat.id, stats_text,
                    reply_markup=markup, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

if __name__ == '__main__':
    print("🤖 Bot is runing....")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Eror: {e}")
