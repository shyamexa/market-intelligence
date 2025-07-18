# Market Intelligence Analyzer

A sophisticated web application that provides AI-powered market intelligence analysis using advanced search capabilities and GPT analysis. Get comprehensive market insights, competitive analysis, and strategic recommendations for your business.

## 🚀 Features

- **AI-Powered Search**: Uses Exa API for intelligent web search across business sources
- **Strategic Analysis**: GPT-4 powered analysis of market intelligence data  
- **Multiple Focus Areas**: Choose from competitive analysis, funding trends, market trends, sales & revenue, or regulatory insights
- **Flexible Timeframes**: From 1 week to 2 years of historical data
- **Custom News Sources**: Specify your preferred domains for targeted research
- **Modern UI**: Clean, responsive web interface inspired by professional tools
- **Rich Formatting**: Well-structured analysis with clickable source links
- **Real-time Processing**: Live analysis with progress indicators

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for:
  - [Exa API](https://exa.ai/) - For intelligent web search
  - [OpenAI API](https://openai.com/) - For AI analysis

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd market-intelligence

# Or download and extract the files to your project directory
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
EXA_API_KEY=your_exa_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Getting API Keys:**
- **Exa API**: Sign up at [exa.ai](https://exa.ai/) and get your API key from the dashboard
- **OpenAI API**: Visit [platform.openai.com](https://platform.openai.com/) and create an API key

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🎯 Usage

### 1. Basic Analysis

1. **Enter Company Name**: Input the company you want to analyze
2. **Select Focus Area**: Choose from:
   - General Market Intelligence
   - Competitive Analysis  
   - Funding & Investment
   - Market Trends
   - Sales & Revenue
   - Regulatory & Compliance

3. **Set Timeframe**: Select from 1 week to 2 years
4. **Optional - Custom Sources**: Add specific news domains (comma-separated)
5. **Generate Report**: Click to start analysis

### 2. Understanding Results

**Executive Summary**: High-level strategic insights and key findings

**Detailed Analysis**: In-depth analysis for each research question including:
- Strategic insights with proper formatting
- Clickable source links to original articles
- Publication dates for context
- Bold text highlighting for key points

### 3. Focus Area Details

**Competitive Analysis**
- Market share analysis
- Competitive landscape insights
- Top competitors identification
- New product launches

**Funding & Investment**
- Latest funding rounds
- Venture capital trends
- IPO activity

**Sales & Revenue**
- Revenue growth metrics
- Customer acquisition costs
- Sales performance benchmarks
- Customer retention analysis

**Market Trends**
- Emerging technology trends
- Consumer behavior changes
- Market size forecasts

**Regulatory & Compliance**
- Regulatory changes
- Government policy impacts
- Compliance requirements

## 🔧 Customization

### Adding New Focus Areas

Edit the `generate_market_questions` method in `market_intelligence.py`:

```python
"new_focus": [
    f"Your custom research question about {self.industry}",
    f"Another question for {self.industry} sector",
],
```

### Modifying Default News Sources

Update the `default_domains` list in the `search_market_intelligence` method:

```python
default_domains = ["your-domain.com", "another-source.com"]
```

### Adjusting Analysis Style

Modify the system prompt in the `analyze_market_intelligence` method to change the analysis focus and tone.

## 📁 Project Structure

```
├── app.py                 # Flask web application
├── market_intelligence.py # Core market intelligence logic
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .env                 # API keys (create this)
```

## 🔍 Default News Sources

The application searches across trusted business sources:
- TechCrunch
- Bloomberg  
- Reuters
- Wall Street Journal
- Forbes
- Crunchbase
- VentureBeat
- Business Insider

You can override these with custom domains in the web interface.

## ⚡ Performance Notes

- Analysis typically takes 2-5 minutes depending on scope
- More specific timeframes yield faster results
- Custom domain lists can improve relevance
- The application respects API rate limits

## 🐛 Troubleshooting

### Common Issues

**API Key Errors**
- Ensure your `.env` file exists with valid API keys
- Check that API keys have sufficient credits/quota

**Import Errors**  
- Run `pip install -r requirements.txt`
- Verify Python version is 3.8+

**Port Conflicts**
- Change the port in `app.py`: `app.run(port=5001)`

**Slow Performance**
- Reduce the number of search results in `market_intelligence.py`
- Use more specific timeframes
- Limit custom domains to most relevant sources

### Error Messages

**"Industry detection failed"**
- The AI couldn't determine the industry from the company name
- Default "technology" industry will be used
- Ensure company name is spelled correctly

**"No search results found"**
- Try a broader timeframe
- Check if custom domains are accessible
- Verify network connectivity

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep API keys secure and rotate them regularly
- The application doesn't store or transmit personal data
- All analysis is performed server-side

## 📄 License

This project is for educational and business use. Please ensure compliance with:
- Exa API Terms of Service
- OpenAI API Terms of Service  
- Respect robots.txt and rate limits of news sources

## 🤝 Contributing

Feel free to customize and extend this application for your specific needs. Some ideas:
- Add more focus areas
- Integrate additional data sources
- Implement user authentication
- Add report export functionality
- Create scheduling for regular analysis

## 📞 Support

For issues with the application:
1. Check the troubleshooting section
2. Review API documentation for Exa and OpenAI
3. Ensure all dependencies are correctly installed

For API-specific issues:
- **Exa API**: Visit [exa.ai/docs](https://docs.exa.ai/)
- **OpenAI API**: Visit [platform.openai.com/docs](https://platform.openai.com/docs) 