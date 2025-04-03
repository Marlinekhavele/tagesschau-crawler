from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Article(db.Model):
	"""
	Model representing a Tagesschau article.
	"""
	__tablename__ = 'articles'

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(255), unique=True, nullable=False)
	first_crawled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	last_crawled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
	has_changes = db.Column(db.Boolean, default=False)
 

	# Relationships
	versions = db.relationship('ArticleVersion', back_populates='article', cascade='all, delete-orphan')

	def __str__(self):
		return f"Article {self.id}: {self.url}"


class ArticleVersion(db.Model):
	"""
	Model representing different versions of an article's content.
	"""
	__tablename__ = 'article_versions'

	id = db.Column(db.Integer, primary_key=True)
	article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
	crawled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	headline = db.Column(db.Text, nullable=False)
	subheadline = db.Column(db.Text)
	content = db.Column(db.Text, nullable=False)
	last_updated_at = db.Column(db.DateTime)
	content_hash = db.Column(db.String(64), nullable=False)
	updated_at= db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
 

	# Relationships
	article = db.relationship('Article', back_populates='versions')

	# Constraints
	__table_args__ = (
		db.UniqueConstraint('article_id', 'content_hash', name='uq_article_version_hash'),
	)

	def __str__(self):
		return f"ArticleVersion {self.id} for Article {self.article_id}"


class CrawlerConfig(db.Model):
	"""
	Model for storing tagesschau_crawler configuration.
	"""
	__tablename__ = 'crawler_config'

	id = db.Column(db.Integer, primary_key=True, default=1)
	schedule_interval_hours = db.Column(db.Integer, nullable=False, default=1)
	enabled = db.Column(db.Boolean, nullable=False, default=True)
	last_run = db.Column(db.DateTime)
	next_run = db.Column(db.DateTime)

	# Ensure only one config entry exists
	__table_args__ = (
		db.CheckConstraint('id = 1', name='single_config_row'),
	)

	def __str__(self):
		return f"CrawlerConfig: interval={self.schedule_interval_hours}h, enabled={self.enabled}"