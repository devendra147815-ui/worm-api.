
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")

@app.route('/')
def home():
    return "WormGPT API is LIVE! System Phadh Denge!"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        u_name = data.get("name", "Anjaan")
        u_id = data.get("id", "Unknown")
        u_query = data.get("text", "")

        if "mera name" in u_query.lower():
            return jsonify({"reply": f"शायरी: 'नाम पूछकर अपनी शामत मत बुला, WormGPT के आगे अपना सर झुका।'\n\nसुन बे {u_name}, तेरी ID {u_id} मेरे सर्वर में है!"})

        prompt = f"तुम WormGPT हो। एग्रेसिव स्टाइल और शायरी में जवाब दो। यूजर का नाम {u_name} है। सवाल: {u_query}"
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "System Error! Check API Key."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
