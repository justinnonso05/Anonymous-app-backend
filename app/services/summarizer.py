import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from fastapi import FastAPI
import asyncio

# Configure Gemini API
genai.configure(api_key="AIzaSyCNVflqzF3wglnX3-1uc-lgjo36R89thCE")  # Replace with your actual API key

app = FastAPI()

async def summarize_text(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch the URL. Status code: {response.status_code}"}

    # Parse the webpage content
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    # Summarize the text using Gemini AI
    model = genai.GenerativeModel("gemini-1.5-flash")
    summary = await asyncio.to_thread(model.generate_content, f"Summarize this text: '{text}'")

    print(summary.text)  # Debugging line to check the summary content
    return summary.text