#!pip install exa_py
#!pip install python-dotenv
#!pip install openai
#!pip install pandas
#!pip install datetime

from exa_py import Exa
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import pandas as pd
from datetime import datetime, timedelta
import re

# Load environment variables
load_dotenv()
EXA_API_KEY = os.environ.get("EXA_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize APIs
exa = Exa(api_key=EXA_API_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

class MarketIntelligenceBot:
    def __init__(self, company_name="", industry="", competitors=None, domains=None):
        self.company_name = company_name
        self.industry = industry or self._detect_industry(company_name)
        self.competitors = competitors or []
        self.domains = domains or []
    
    def _detect_industry(self, company_name):
        """Auto-detect industry from company name using AI"""
        if not company_name:
            return "technology"  # Default industry
        
        try:
            prompt = f"""Based on the company name "{company_name}", what industry does this company operate in? 
            
            Provide a concise industry classification (1-3 words). Examples:
            - "artificial intelligence"
            - "fintech" 
            - "healthcare"
            - "e-commerce"
            - "automotive"
            - "software"
            - "biotechnology"
            
            Only respond with the industry name, nothing else."""
            
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=20
            )
            
            detected_industry = completion.choices[0].message.content
            if detected_industry:
                detected_industry = detected_industry.strip().lower()
            else:
                detected_industry = "technology"
            return detected_industry
            
        except Exception as e:
            print(f"Error detecting industry: {e}")
            return "technology"  # Fallback to technology
        
    def generate_market_questions(self, focus_area="general"):
        """Generate targeted market intelligence questions"""
        
        base_questions = {
            "funding": [
                f"Latest funding rounds and investments in {self.industry} startups 2024",
                f"Venture capital trends {self.industry} sector",
                f"IPO activity {self.industry} companies recent",
            ],
            "competitive": [
                f"Market share analysis {self.industry}",
                f"Competitive landscape {self.industry} disruption",
                f"Top competitors in {self.industry} sector 2024",
                f"New product launches {self.industry} industry",
            ],
            "regulatory": [
                f"Regulatory changes affecting {self.industry} companies",
                f"Government policy {self.industry} sector",
                f"Compliance requirements {self.industry} 2024",
            ],
            "trends": [
                f"Emerging trends {self.industry} technology",
                f"Consumer behavior changes {self.industry}",
                f"Market size growth {self.industry} forecast",
            ],
            "sales": [
                f"{self.industry} companies revenue growth 2024",
                f"Customer acquisition costs {self.industry} sector",
                f"Sales performance metrics {self.industry} businesses",
                f"Customer retention rates {self.industry} companies",
                f"Average deal size {self.industry} market",
                f"Sales cycle length {self.industry} industry",
                f"Customer lifetime value {self.industry} sector",
            ],
            "general": [
                f"Latest news {self.industry} companies",
                f"Major partnerships {self.industry} sector",
                f"Industry conference insights {self.industry}",
            ]
        }
        
        return base_questions.get(focus_area, base_questions["general"])
    
    def search_market_intelligence(self, questions, timeframe="1M"):
        """
        Search for market intelligence using EXA's highlights endpoint and domain filtering
        
        KEY FEATURES:
        1. HIGHLIGHTS ENDPOINT: Extracts only relevant sentences (not full articles)
        2. DOMAIN FILTERING: Restricts search to trusted financial sources
        3. DATE FILTERING: Ensures recency of information
        
        Args:
            questions: List of research questions
            timeframe: How far back to search (1W, 1M, 3M, 6M, 1Y, 2Y)
        
        Returns:
            Structured results with highlights and source attribution
        """
        
        # 🎯 HIGHLIGHTS CONFIGURATION
        # This is what makes our system superior to traditional web scraping
        # Note: Exa automatically optimizes highlight length and number per URL
        # We get precise, relevant excerpts instead of full article content
        
        # 📅 DATE FILTERING FOR RECENCY
        timeframe_days = {
            "1W": 7,   "2W": 14,  "1M": 30,   "2M": 60,
            "3M": 90,  "6M": 180, "1Y": 365,  "2Y": 730
        }
        
        days = timeframe_days.get(timeframe, 30)  # Default to 1 month
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        all_results = []
        
        # 🏦 TRUSTED FINANCIAL DOMAINS
        # These are institutional-grade sources for financial compliance
        default_domains = [
            "bloomberg.com",         # Financial news and data
            "reuters.com",           # International news and markets  
            "wsj.com",              # Wall Street Journal
            "forbes.com",           # Business and finance
            "ft.com",               # Financial Times
            "cnbc.com",             # Financial television
            "techcrunch.com",       # Technology and startups
            "crunchbase.com",       # Company and funding data
            "venturebeat.com",      # Technology trends
            "businessinsider.com",  # Business news
            "sec.gov",              # SEC filings and regulatory
            "federalreserve.gov"    # Federal Reserve data
        ]
        
        # 🛡️ DOMAIN FILTERING: Use custom domains if provided, otherwise use trusted defaults
        search_domains = self.domains if self.domains else default_domains
        
        print(f"🔍 Searching across {len(search_domains)} trusted domains:")
        print(f"   Domain filtering: {', '.join(search_domains[:3])}{'...' if len(search_domains) > 3 else ''}")
        
        for question in questions:
            try:
                print(f"📊 Processing: {question}")
                
                # 🚀 EXA NEURAL SEARCH with HIGHLIGHTS
                # This is the core differentiator - highlights endpoint + domain filtering
                search_response = exa.search_and_contents(
                    question, 
                    type="neural",                    # Neural search for semantic understanding
                    highlights=True,                  # 🎯 KEY: Use highlights instead of full content
                    num_results=5,                    # Get multiple sources for comprehensive view
                    start_published_date=start_date,  # 📅 Recent information only
                    include_domains=search_domains    # 🏦 KEY: Trusted domains only
                )
                
                # 📋 STRUCTURE RESULTS WITH HIGHLIGHTS
                question_results = {
                    "question": question,
                    "results": []
                }
                
                # Extract highlights (not full content) for precise analysis
                for result in search_response.results:
                    if result.highlights:  # Only process if highlights exist
                        for highlight in result.highlights:
                            question_results["results"].append({
                                "title": result.title,
                                "url": result.url,
                                "highlight": highlight,  # 🎯 This is the key - precise excerpts
                                "published_date": getattr(result, 'published_date', None),
                                "domain": result.url.split('/')[2] if '/' in result.url else "unknown"
                            })
                
                all_results.append(question_results)
                print(f"   ✅ Found {len(question_results['results'])} relevant highlights")
                
            except Exception as e:
                print(f"❌ Error searching for '{question}': {e}")
                continue
        
        print(f"\n🎯 HIGHLIGHTS SUMMARY:")
        print(f"   Total highlights extracted: {sum(len(r['results']) for r in all_results)}")
        print(f"   Sources used: {len(set(r['domain'] for result in all_results for r in result['results']))}")
        
        return all_results
    
    def analyze_market_intelligence(self, search_results):
        """Use GPT to analyze and synthesize market intelligence"""
        
        analyses = []
        
        for result in search_results:
            if not result["results"]:
                continue
                
            # Enhanced system prompt for market analysis
            system_prompt = """You are a senior market intelligence analyst. 
            Analyze the provided information and give strategic insights focusing on:
            1. Key market trends and implications
            2. Competitive dynamics and opportunities
            3. Financial and business impact
            4. Strategic recommendations
            
            Provide concise, actionable insights suitable for executive briefings.
            Format your response with clear sections and bullet points where appropriate."""
            
            # Combine all highlights for comprehensive analysis
            context = "\n\n".join([f"Source: {item['title']}\nURL: {item['url']}\nContent: {item['highlight']}" 
                                 for item in result["results"]])
            
            user_prompt = f"""
            Research Question: {result["question"]}
            
            Market Intelligence Sources:
            {context}
            
            Provide a strategic analysis with key insights and recommendations.
            """
            
            try:
                completion = openai.chat.completions.create(
                    model="gpt-4",  # Use GPT-4 for better analysis
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.3  # Lower temperature for more focused analysis
                )
                
                analysis = {
                    "question": result["question"],
                    "analysis": completion.choices[0].message.content,
                    "sources": result["results"],
                    "timestamp": datetime.now().isoformat()
                }
                
                analyses.append(analysis)
                
            except Exception as e:
                print(f"Error analyzing '{result['question']}': {e}")
                continue
        
        return analyses
    
    def generate_market_report(self, analyses, focus_area="general"):
        """Generate a comprehensive market intelligence report"""
        
        report = {
            "company": self.company_name,
            "industry": self.industry,
            "focus_area": focus_area,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": "",
            "key_findings": [],
            "strategic_recommendations": [],
            "detailed_analysis": analyses
        }
        
        # Generate executive summary
        all_insights = "\n\n".join([a["analysis"] for a in analyses])
        
        summary_prompt = f"""
        Based on the following market intelligence analysis for {self.company_name} in the {self.industry} industry,
        create a concise executive summary highlighting the most critical insights and strategic implications:
        
        {all_insights}
        
        Focus on actionable insights for leadership decision-making.
        """
        
        try:
            summary_completion = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst creating executive summaries."},
                    {"role": "user", "content": summary_prompt},
                ],
                temperature=0.3
            )
            
            report["executive_summary"] = summary_completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating executive summary: {e}")
            report["executive_summary"] = "Executive summary generation failed."
        
        return report
    
    def run_market_intelligence(self, focus_area="general", timeframe="1M"):
        """Main method to run complete market intelligence analysis"""
        
        print(f"🔍 Running Market Intelligence Analysis...")
        print(f"Company: {self.company_name}")
        print(f"Industry: {self.industry}")
        print(f"Focus Area: {focus_area}")
        print(f"Timeframe: {timeframe}")
        print("-" * 50)
        
        # Generate questions
        questions = self.generate_market_questions(focus_area)
        print(f"Generated {len(questions)} research questions")
        
        # Search for information
        search_results = self.search_market_intelligence(questions, timeframe)
        print(f"Completed search across {len(search_results)} topics")
        
        # Analyze results
        analyses = self.analyze_market_intelligence(search_results)
        print(f"Generated {len(analyses)} strategic analyses")
        
        # Generate comprehensive report
        report = self.generate_market_report(analyses, focus_area)
        
        return report

# Example usage
if __name__ == "__main__":
    # Configure for your specific use case
    bot = MarketIntelligenceBot(
        company_name="TechCorp",
        industry="artificial intelligence",
        competitors=["OpenAI", "Anthropic", "Google DeepMind", "Microsoft"]
    )
    
    # Run different types of analysis
    focus_areas = ["competitive", "funding", "trends", "sales", "regulatory"]
    
    for focus in focus_areas:
        print(f"\n{'='*60}")
        print(f"MARKET INTELLIGENCE REPORT - {focus.upper()}")
        print(f"{'='*60}")
        
        report = bot.run_market_intelligence(focus_area=focus, timeframe="1M")
        
        print(f"\nEXECUTIVE SUMMARY:")
        print(report["executive_summary"])
        
        print(f"\nDETAILED FINDINGS:")
        for analysis in report["detailed_analysis"]:
            print(f"\n📊 {analysis['question']}")
            print(f"Analysis: {analysis['analysis']}")
            print(f"Sources: {', '.join(analysis['sources'][:3])}")  # Show first 3 sources
        
        # Save report to file
        with open(f"market_intelligence_{focus}_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        # print(f"\n✅ Report saved to market_intelligence_{focus}_{datetime.now().strftime('%Y%m%d')}.json")