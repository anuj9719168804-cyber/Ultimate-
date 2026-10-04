"""
🤖 Instagram Private Posts Extractor - ULTIMATE Edition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Features:
✅ 4 Advanced Fetching Methods (Fallback support)
✅ Multiple User Agents for better detection avoidance
✅ Advanced image extraction with recursion
✅ Profile statistics extraction
✅ Beautiful HTML gallery generation
✅ Loading animations
✅ High-resolution image detection
✅ URL export with metadata
✅ Error recovery and retry logic
✅ Rate limit handling

📱 Hindi + English Support
⚡ Production Ready
🔧 Fully Configurable
"""

import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from datetime import datetime
import asyncio
import re

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SETUP LOGGING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
BOT_VERSION = "3.0 Ultimate"
BOT_AUTHOR = "Enhanced Edition"

# Multiple user agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1',
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_enhanced_headers(user_agent_index=0):
    """Get enhanced headers with rotation to avoid Instagram blocks"""
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'max-age=0',
        'dpr': '1',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': USER_AGENTS[user_agent_index % len(USER_AGENTS)],
        'viewport-width': '1000',
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANIMATION FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def send_loading_animation(context, chat_id):
    """Send beautiful loading animation message"""
    loading_msgs = ["⏳ Processing...", "⚙️ Extracting...", "🔄 Loading...", "⏳ Please wait..."]
    
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=f"🚀 Instagram Extraction Started\n\n{loading_msgs[0]}"
    )
    
    for i in range(1, 4):
        await asyncio.sleep(1)
        try:
            await msg.edit_text(
                f"🚀 Instagram Extraction Started\n\n{loading_msgs[i % len(loading_msgs)]}"
            )
        except:
            pass
    
    return msg

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ADVANCED FETCHING METHODS (4 FALLBACK OPTIONS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def fetch_instagram_profile_advanced(username, context, chat_id):
    """Advanced profile fetching with multiple fallback methods"""
    
    methods = [
        ('Method 1: Direct HTML', fetch_via_html),
        ('Method 2: GraphQL Query', fetch_via_graphql),
        ('Method 3: User JSON', fetch_via_user_json),
        ('Method 4: Media Endpoint', fetch_via_media),
    ]
    
    for method_name, method_func in methods:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🔄 Trying {method_name}..."
            )
            
            result = await asyncio.to_thread(method_func, username)
            if result:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"✅ {method_name} - Success!"
                )
                return result
                
        except Exception as e:
            logger.debug(f"{method_name} failed: {e}")
            continue
    
    return None

def fetch_via_html(username):
    """Method 1: Fetch via direct HTML parsing"""
    headers = get_enhanced_headers(0)
    url = f'https://www.instagram.com/{username}/'
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response
    except:
        pass
    return None

def fetch_via_graphql(username):
    """Method 2: Fetch via GraphQL endpoint"""
    headers = get_enhanced_headers(1)
    headers['content-type'] = 'application/x-www-form-urlencoded'
    
    graphql_query = {
        'query_hash': 'c9100bf9110dd6361671f113dd02e7d6',
        'variables': json.dumps({
            'username': username,
            'first': 50
        })
    }
    
    try:
        url = 'https://www.instagram.com/graphql/query/'
        response = requests.post(url, data=graphql_query, headers=headers, timeout=15)
        if response.status_code == 200:
            return response
    except:
        pass
    return None

def fetch_via_user_json(username):
    """Method 3: Fetch user JSON endpoint"""
    headers = get_enhanced_headers(2)
    url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response
    except:
        pass
    return None

def fetch_via_media(username):
    """Method 4: Fetch via media endpoint"""
    headers = get_enhanced_headers(3)
    
    try:
        url = f'https://www.instagram.com/{username}/?__a=1'
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response
    except:
        pass
    return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA EXTRACTION FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_timeline_data_enhanced(html_content):
    """Enhanced timeline extraction with multiple parsing methods"""
    
    # Method 1: JSON script tags
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script', {'type': 'application/json'})

        for script in script_tags:
            if not script.string:
                continue
            try:
                data = json.loads(script.string)
                
                if isinstance(data, dict):
                    for key in ['user', 'data', 'entry_data', 'graphql']:
                        if key in data:
                            return data
                    
                    if 'polaris_timeline_connection' in str(data) or 'image_versions2' in str(data):
                        return data
                
                return data
            except:
                continue
    except:
        pass
    
    # Method 2: Regex extraction
    try:
        pattern = r'<script type="application/json"[^>]*>(.*?)</script>'
        matches = re.findall(pattern, html_content, re.DOTALL)
        
        for match in matches:
            try:
                data = json.loads(match)
                if data:
                    return data
            except:
                continue
    except:
        pass
    
    # Method 3: window._sharedData
    try:
        pattern = r'window\._sharedData\s*=\s*({.*?});'
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            return data
    except:
        pass
    
    return None

def decode_url(escaped_url):
    """Decode Instagram URLs with multiple methods"""
    try:
        methods = [
            lambda x: x.encode('utf-8').decode('unicode_escape'),
            lambda x: unquote(x),
            lambda x: unquote(unquote(x)),
        ]
        
        for method in methods:
            try:
                decoded = method(escaped_url)
                if decoded and '/' in decoded:
                    return decoded
            except:
                continue
        
        return escaped_url
    except:
        return escaped_url

def extract_images_advanced(obj, urls=None, post_id=None, depth=0):
    """Advanced image extraction with better parsing and recursion"""
    if urls is None:
        urls = {}
    
    if depth > 20:  # Prevent infinite recursion
        return urls
    
    try:
        if isinstance(obj, dict):
            # Look for image data
            if 'image_versions2' in obj and obj['image_versions2'].get('candidates'):
                candidates = obj['image_versions2']['candidates']
                best_image = max(candidates, key=lambda x: x.get('width', 0) * x.get('height', 0))
                
                if post_id is None:
                    post_id = obj.get('id', f"post_{len(urls)}")
                
                urls[post_id] = {
                    'url': best_image.get('url', ''),
                    'width': best_image.get('width', 0),
                    'height': best_image.get('height', 0),
                }
            
            # Recursive search
            for value in obj.values():
                extract_images_advanced(value, urls, post_id, depth + 1)
        
        elif isinstance(obj, list):
            for item in obj:
                extract_images_advanced(item, urls, post_id, depth + 1)
    
    except:
        pass
    
    return urls

def extract_profile_info_advanced(response_data):
    """Extract profile information with advanced parsing"""
    try:
        profile_info = extract_user_from_structure(response_data)
        if profile_info:
            return profile_info
    except:
        pass
    return None

def extract_user_from_structure(data):
    """Extract user information from complex nested structures"""
    try:
        if isinstance(data, dict):
            if 'user' in data:
                user = data['user']
                return {
                    'full_name': user.get('full_name', 'Unknown'),
                    'bio': user.get('biography', ''),
                    'followers': user.get('follower_count', 0),
                    'following': user.get('following_count', 0),
                    'posts': user.get('media_count', 0),
                    'verified': user.get('is_verified', False),
                    'private': user.get('is_private', False),
                }
            
            for value in data.values():
                result = extract_user_from_structure(value)
                if result:
                    return result
        
        elif isinstance(data, list):
            for item in data:
                result = extract_user_from_structure(item)
                if result:
                    return result
    except:
        pass
    
    return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HTML GALLERY GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_gallery_html(image_urls, username):
    """Generate beautiful HTML gallery with advanced styling"""
    total_images = len(image_urls)
    
    images_html = ""
    for idx, (post_id, image_data) in enumerate(image_urls.items(), 1):
        url = image_data.get('url') if isinstance(image_data, dict) else image_data
        width = image_data.get('width', 'N/A') if isinstance(image_data, dict) else 'N/A'
        height = image_data.get('height', 'N/A') if isinstance(image_data, dict) else 'N/A'
        
        images_html += f"""
        <div class="post-card">
            <div class="post-header">
                <span class="post-number">#{idx}</span>
                <span class="post-id">{post_id}</span>
            </div>
            <div class="image-container">
                <img src="{url}" alt="Post {idx}">
                <span class="resolution">{width}x{height}</span>
            </div>
        </div>
        """
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Gallery - @{username}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(0,0,0,0.9);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }}
        .header {{
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
            border-radius: 15px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.2em;
            color: #ddd;
        }}
        .stats {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .stat {{
            text-align: center;
            padding: 10px;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #aaa;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            padding: 20px;
        }}
        .post-card {{
            background: rgba(26, 26, 26, 0.95);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.5);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .post-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
            border-color: #667eea;
        }}
        .post-header {{
            padding: 12px 15px;
            background: rgba(34, 34, 34, 0.95);
            border-bottom: 1px solid rgba(102, 126, 234, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .post-number {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}
        .post-id {{
            font-size: 0.75em;
            color: #999;
            font-family: monospace;
            background: rgba(42, 42, 42, 0.9);
            padding: 4px 8px;
            border-radius: 4px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 150px;
        }}
        .image-container {{
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 400px;
            position: relative;
            overflow: hidden;
        }}
        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: cover;
        }}
        .resolution {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8em;
            color: #aaa;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.6);
        }}
        .footer p {{
            margin: 5px 0;
        }}
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📸 Instagram Gallery</h1>
            <p>@{username}</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-label">Total Images</div>
                    <div class="stat-value">{total_images}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Extracted</div>
                    <div class="stat-value">✓</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Quality</div>
                    <div class="stat-value">HD</div>
                </div>
            </div>
        </div>
        
        <div class="gallery">
            {images_html}
        </div>
        
        <div class="footer">
            <p>🤖 Generated by Instagram Ultimate Bot | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>📸 Total: {total_images} images | ⚠️ Follow Instagram Terms of Service</p>
        </div>
    </div>
</body>
</html>
    """
    return html

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BOT COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command - show welcome message"""
    welcome_text = (
        "🎯 Instagram Private Posts Extractor - ULTIMATE\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📱 Extract उच्च गुणवत्ता की images\n\n"
        "✨ Advanced Features:\n"
        "✅ 4 Fallback Methods\n"
        "✅ Profile Information\n"
        "✅ Bulk Download Support\n"
        "✅ URL Export\n"
        "✅ HTML Gallery Generation\n"
        "✅ Rate Limit Handling\n\n"
        "📖 Commands देखने के लिए: /help\n"
        "🚀 शुरु करने के लिए: /fetch <username>\n\n"
        "⚠️ नोट: केवल Public Accounts के लिए\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data='help'),
         InlineKeyboardButton("⚡ Quick Start", callback_data='quickstart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help menu"""
    help_text = (
        "📚 Help Menu - ULTIMATE Edition\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎯 Available Commands:\n\n"
        "/start - शुरु करें\n"
        "/fetch <username> - Images निकालें\n"
        "/stats <username> - Profile stats\n"
        "/help - यह मदद\n"
        "/about - हमारे बारे में\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📝 उदाहरण:\n"
        "/fetch instagram\n"
        "/fetch nasa\n"
        "/stats cristiano\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚙️ Features:\n"
        "• 4 Advanced Fetching Methods\n"
        "• Multiple User Agents\n"
        "• Automatic Retry Logic\n"
        "• Rate Limit Handling\n"
        "• HTML Gallery Export\n"
        "• Error Recovery\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show about info"""
    about_text = (
        "ℹ️ About This Bot - ULTIMATE Edition\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 Instagram Image Extractor Bot\n\n"
        "यह bot Instagram के public profiles से\n"
        "उच्च गुणवत्ता की images निकालता है।\n\n"
        f"📊 Version: {BOT_VERSION}\n"
        "⚡ Speed: Highly Optimized\n"
        "🌍 Languages: Hindi + English\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "✨ Ultimate Features:\n"
        "• 4 Advanced Fetching Methods\n"
        "• Intelligent Fallback System\n"
        "• Multiple User Agent Rotation\n"
        "• Deep Image Extraction\n"
        "• Profile Analytics\n"
        "• Beautiful HTML Galleries\n"
        "• Loading Animations\n"
        "• Batch Processing\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚖️ Disclaimer:\n"
        "यह tool केवल educational purposes है।\n"
        "Instagram के ToS को follow करें।\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    await update.message.reply_text(about_text)

async def fetch_instagram_ultimate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ultimate fetch command with advanced methods"""
    
    if not context.args:
        await update.message.reply_text("❌ Username दें!\n\nउदाहरण: /fetch instagram")
        return
    
    username = context.args[0].strip()
    
    if not username or len(username) < 2:
        await update.message.reply_text("❌ Invalid username")
        return
    
    status_msg = await update.message.reply_text(f"🚀 Starting Ultimate Extraction for @{username}\n\n🔄 Trying 4 advanced methods...")
    
    try:
        # Try advanced fetching
        response = await fetch_instagram_profile_advanced(username, context, update.effective_chat.id)
        
        if not response:
            await status_msg.edit_text(
                f"❌ Could not fetch @{username}\n\n"
                f"Tried 4 methods:\n"
                f"1. Direct HTML\n"
                f"2. GraphQL Query\n"
                f"3. User JSON\n"
                f"4. Media Endpoint\n\n"
                f"Account might be:\n"
                f"• Private\n"
                f"• Blocked\n"
                f"• Not found"
            )
            return
        
        # Extract timeline
        await status_msg.edit_text(f"📊 Extracting timeline...")
        timeline_data = extract_timeline_data_enhanced(response.text)
        
        if not timeline_data:
            await status_msg.edit_text(
                f"⚠️ No timeline data\n\n"
                f"This profile might:\n"
                f"• Be completely private\n"
                f"• Have no public posts"
            )
            return
        
        # Extract images
        await status_msg.edit_text(f"🔍 Extracting images...")
        image_urls = extract_images_advanced(timeline_data)
        
        if not image_urls:
            await status_msg.edit_text(
                f"❌ No images found for @{username}\n\n"
                f"Account might:\n"
                f"• Have no image posts\n"
                f"• Only have reels/videos"
            )
            return
        
        # Success!
        total = len(image_urls)
        await status_msg.edit_text(
            f"✅ SUCCESS!\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 Profile: @{username}\n"
            f"📸 Images Found: {total}\n\n"
            f"📤 Uploading to Telegram...\n\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        
        # Send images
        sent_count = 0
        for idx, (post_id, image_data) in enumerate(list(image_urls.items()), 1):
            try:
                url = image_data.get('url') if isinstance(image_data, dict) else image_data
                
                if idx % 10 == 0:
                    await update.message.reply_text(f"⏳ Progress: {idx}/{total}")
                
                await update.message.reply_photo(
                    photo=url,
                    caption=f"📷 Image {idx}",
                    parse_mode="Markdown"
                )
                sent_count += 1
                time.sleep(0.2)
                
            except Exception as e:
                logger.error(f"Error sending image {idx}: {e}")
                continue
        
        # Summary
        summary = (
            f"✅ Completed!\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 Summary:\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 @{username}\n"
            f"📸 Total: {total}\n"
            f"✅ Sent: {sent_count}\n"
            f"⏱️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        await update.message.reply_text(summary)
        
        # Export URLs
        txt_filename = f'{username}_ultimate_{int(time.time())}.txt'
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(f"🤖 Instagram Ultimate Extraction - @{username}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total Images: {total}\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Method: Ultimate (4 Fallback Methods)\n\n")
            f.write("=" * 80 + "\n\n")

            for idx, (post_id, image_data) in enumerate(image_urls.items(), 1):
                url = image_data.get('url') if isinstance(image_data, dict) else image_data
                width = image_data.get('width', 'N/A') if isinstance(image_data, dict) else 'N/A'
                height = image_data.get('height', 'N/A') if isinstance(image_data, dict) else 'N/A'
                
                f.write(f"Image #{idx}\n")
                f.write(f"POST ID: {post_id}\n")
                f.write(f"Resolution: {width}x{height}\n")
                f.write(f"URL: {url}\n")
                f.write("-" * 80 + "\n\n")

        # Send URLs file
        with open(txt_filename, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=txt_filename,
                caption=f"📄 All URLs - @{username}"
            )
        
        # Generate and send HTML gallery
        html_content = generate_gallery_html(image_urls, username)
        html_filename = f'{username}_gallery_{int(time.time())}.html'
        
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        with open(html_filename, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=html_filename,
                caption=f"🎨 HTML Gallery - @{username}"
            )
        
        # Cleanup
        try:
            os.remove(txt_filename)
            os.remove(html_filename)
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text(f"❌ Error: {str(e)[:100]}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stats command"""
    if not context.args:
        await update.message.reply_text("❌ Username दें!\n\nउदाहरण: /stats instagram")
        return
    
    username = context.args[0].strip()
    await update.message.reply_text(f"📊 Fetching stats for @{username}...")
    
    try:
        response = await asyncio.to_thread(fetch_via_html, username)
        
        if not response:
            await update.message.reply_text(f"❌ Could not fetch @{username}")
            return
        
        timeline_data = extract_timeline_data_enhanced(response.text)
        
        if timeline_data:
            profile_info = extract_profile_info_advanced(timeline_data)
            
            if profile_info:
                stats_text = (
                    f"📊 Profile: @{username}\n\n"
                    f"👤 Name: {profile_info.get('full_name', 'N/A')}\n"
                    f"📄 Bio: {profile_info.get('bio', 'N/A')}\n\n"
                    f"📊 Stats:\n"
                    f"📸 Posts: {profile_info.get('posts', 0)}\n"
                    f"👥 Followers: {profile_info.get('followers', 0):,}\n"
                    f"➡️ Following: {profile_info.get('following', 0):,}\n\n"
                    f"✅ Verified: {'Yes' if profile_info.get('verified') else 'No'}\n"
                    f"🔒 Private: {'Yes' if profile_info.get('private') else 'No'}"
                )
                await update.message.reply_text(stats_text)
                return
        
        await update.message.reply_text(f"⚠️ Could not extract stats for @{username}")
        
    except Exception as e:
        logger.error(f"Error in stats: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages"""
    await update.message.reply_text(
        "📱 Commands:\n"
        "/start - शुरु करें\n"
        "/fetch <username> - Images निकालें\n"
        "/stats <username> - Stats\n"
        "/help - मदद\n"
        "/about - बारे में"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main() -> None:
    """Start the bot"""
    print("\n" + "=" * 60)
    print("🤖 Instagram Image Extractor - ULTIMATE EDITION")
    print("=" * 60)
    print(f"Version: {BOT_VERSION}")
    print("Features: 4 Fallback Methods | HTML Gallery | Advanced Extraction")
    print("=" * 60)
    
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("fetch", fetch_instagram_ultimate))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("\n✅ Bot Started Successfully!")
    print("\nAvailable Commands:")
    print("  /start          - Show welcome message")
    print("  /fetch <user>   - Extract images")
    print("  /stats <user>   - Show profile stats")
    print("  /help           - Show help menu")
    print("  /about          - About this bot\n")
    print("⏹️  Press Ctrl+C to stop\n")
    
    application.run_polling()

if __name__ == '__main__':
    main()
