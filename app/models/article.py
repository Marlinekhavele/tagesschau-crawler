from datetime import datetime
from app.database.db import db


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
	updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 

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
 

	article = db.relationship('Article', back_populates='versions')

	__table_args__ = (
		db.UniqueConstraint('article_id', 'content_hash', name='uq_article_version_hash'),
	)

	def __str__(self):
		return f"ArticleVersion {self.id} for Article {self.article_id}"

