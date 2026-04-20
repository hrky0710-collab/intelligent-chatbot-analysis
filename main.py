import os
from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# あなたの環境で確実に動くモデルを自動選択
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
    model = genai.GenerativeModel(target_model)
except Exception as e:
    model = genai.GenerativeModel('gemini-pro')

app = FastAPI()

@app.get("/")
def home():
    return {"status": "AI Ready!", "model_in_use": target_model}

@app.get("/chat")
def chat(query: str):
    try:
        # ここが「完璧なプレゼン」のためのカンペ指示（プロンプト）です
        prompt = f"""
        あなたは優秀なカスタマーサクセス担当です。
        ユーザーの問いに対して丁寧に応答し、最後に以下の形式で必ず分析結果を添えてください。
        
        【回答】: (ユーザーへの返答)
        【感情分析】: (Positive / Negative / Neutral)
        【ニーズ抽出】: (ユーザーが真に求めていること)
        【緊急度】: (高 / 中 / 低)
        
        ユーザーの問い: {query}
        """
        response = model.generate_content(prompt)
        return {"ai_response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))