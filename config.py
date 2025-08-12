import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-openai-key')
    AVIATIONSTACK_API_KEY = os.environ.get('AVIATIONSTACK_API_KEY', 'your-aviationstack-key')
    
    # Data sources
    AVIATIONSTACK_BASE_URL = 'http://api.aviationstack.com/v1'
    SCRAPE_OPS_URL = 'https://proxy.scrapeops.io/v1'
    SCRAPE_OPS_API_KEY = os.environ.get('SCRAPE_OPS_API_KEY', 'your-scrapeops-key')
    
    # Cache settings
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300