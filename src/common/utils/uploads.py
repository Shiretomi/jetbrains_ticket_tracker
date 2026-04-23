import aiohttp
from .config import config

PASTEBIN_API_KEY = config['pastebin_api_key']

async def upload_to_pastebin(title, content):
    url = "https://pastebin.com/api/api_post.php"
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': content,
        'api_paste_name': title,
        'api_paste_format': 'bash',
        'api_paste_expire_date': '1H',
        'api_paste_private': '1',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None