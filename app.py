import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import httpx

app = Flask(__name__)
CORS(app)

cache = {}
CACHE_TTL = 86400  

client = httpx.Client(
    headers={
        "x-ig-app-id": "936619743392459",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

@app.route('/user', methods=['GET'])
def instagram_user():
    """Faz scraping dos dados de um usuário do Instagram e retorna o número de seguidores"""
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400

    if username in cache:
        cached_data, timestamp = cache[username]
        if time.time() - timestamp < CACHE_TTL:
            return jsonify(cached_data)

    try:
        result = client.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}")
        data = json.loads(result.content)
        if result.status_code != 200:
            return jsonify({"error": f"Unexpected status code {result.status_code}"}), 500
        
        data = result.json()  
        user = data.get("data", {}).get("user", {})
        followers_count = user.get("edge_followed_by", {}).get("count", "N/A")
        profile_picture_url = user.get("profile_pic_url_hd", "N/A")
        full_name = user.get("full_name", "N/A")

        response_data = {
            "followers_count": followers_count,
            "profile_picture_url": profile_picture_url,
            "full_name": full_name
        }

        cache[username] = (response_data, time.time())

        return jsonify(response_data)
    except httpx.RequestError as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON response"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)