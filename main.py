import logging
from app import create_app
from crawler.scheduler import CrawlerScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create Flask app
app = create_app()

# Initialize scheduler
scheduler = CrawlerScheduler(app)

@app.get("/")
def read_root():
    return {
        "message": "Crawler API is running",
        "version": "1.0.0",
        "status": "OK"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)