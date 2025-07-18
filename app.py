from flask import Flask, render_template, request, jsonify
from market_intelligence import MarketIntelligenceBot
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        company_name = data.get('company_name', '')
        domains = data.get('domains', '').split(',') if data.get('domains') else []
        focus_area = data.get('focus_area', 'general')
        timeframe = data.get('timeframe', '1M')
        
        # Clean up domains list
        domains = [domain.strip() for domain in domains if domain.strip()]
        
        # Initialize the market intelligence bot (industry will be auto-detected)
        bot = MarketIntelligenceBot(
            company_name=company_name,
            industry="",  # Will be auto-detected from company name
            domains=domains
        )
        
        # Run the analysis
        report = bot.run_market_intelligence(focus_area=focus_area, timeframe=timeframe)
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 