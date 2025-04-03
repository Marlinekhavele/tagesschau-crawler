import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from crawler.crawler import Crawler
logger = logging.getLogger(__name__)


class CrawlerScheduler:
	def __init__(self, app=None):
		self.app = app
		self.scheduler = BackgroundScheduler()

		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		"""
		Initialize with Flask app
		"""
		self.app = app

		# Set up the job
		crawler_interval = app.config.get('CRAWLER_INTERVAL', 60)  # Default: 60 minutes

		self.scheduler.add_job(
			func=self._run_crawler,
			trigger=IntervalTrigger(minutes=crawler_interval),
			id='crawler',
			name='Crawler',
			replace_existing=True
		)

		# Start the scheduler
		self.scheduler.start()
		logger.info(f"Crawler scheduler started. Interval: {crawler_interval} minutes")

		# Register shutdown function
		app.teardown_appcontext(self._shutdown_scheduler)

	def _run_crawler(self):
		"""
		Run the crawler with app context
		"""
		with self.app.app_context():
			logger.info("Running scheduled crawler job")
			crawler = Crawler()
			crawler.crawl_overview_page()

	def _shutdown_scheduler(self, exception=None):
		"""
		Shut down the scheduler when the app context ends
		"""
		if self.scheduler.running:
			self.scheduler.shutdown()