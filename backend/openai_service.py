# OpenAI GPT-4o integration for cost insights
import os
import openai

def generate_insight_summary(data):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    prompt = f"""
    You are an Azure cost optimization assistant. Given the following data, summarize the key cost-saving opportunities in plain language for a business user.\n\nData: {data}\n\nSummary:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message["content"].strip()
