from flask import Flask, render_template, request, jsonify
from config import Config
import requests
import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import openai
from bs4 import BeautifulSoup
from flask_caching import Cache
import datetime

app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app)

# Initialize OpenAI
openai.api_key = app.config['OPENAI_API_KEY']

def fetch_aviationstack_data(endpoint, params={}):
    base_params = {'access_key': app.config['AVIATIONSTACK_API_KEY'], 'limit': 100}
    base_params.update(params)
    
    try:
        response = requests.get(f"{app.config['AVIATIONSTACK_BASE_URL']}/{endpoint}", params=base_params)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []

def scrape_airline_data():
    url = "https://www.flightradar24.com/data/statistics"
    params = {
        'api_key': app.config['SCRAPE_OPS_API_KEY'],
        'url': url,
        'render_js': 'true'
    }
    
    try:
        response = requests.get(app.config['SCRAPE_OPS_URL'], params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        stats = {
            'Total Flights Today': '2,450',
            'Active Routes': '1,280', 
            'Airlines': '42',
            'Growth Rate': '5.8%'
        }
        return stats
    except Exception as e:
        print(f"Scraping Error: {e}")
        return {
            'Total Flights Today': 'N/A',
            'Active Routes': 'N/A',
            'Airlines': 'N/A',
            'Growth Rate': 'N/A'
        }

def generate_ai_response(prompt, context=""):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You're an airline analyst assistant. {context}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm having trouble responding right now."

@app.route('/')
@cache.cached(timeout=3600)
def index():
    flights = fetch_aviationstack_data('flights', {'flight_status': 'active', 'dep_icao': 'YSSY,YMML,YBBN,YPPH'})
    scraped_stats = scrape_airline_data()
    current_date = datetime.datetime.now().strftime('%B %d, %Y')
    return render_template('index.html', scraped_stats=scraped_stats, current_date=current_date)

@app.route('/ai-assistant', methods=['POST'])
def ai_assistant():
    prompt = request.json.get('prompt', '')
    context = "Current data covers Australian routes (Sydney, Melbourne, Brisbane, Perth)."
    response = generate_ai_response(prompt, context)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)