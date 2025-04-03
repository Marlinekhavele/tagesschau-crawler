from datetime import datetime
from sqlalchemy import desc
from app.database.db import db
from app.models.article import Article, ArticleVersion


class ArticleService:
	@staticmethod
	def get_all_articles(page=1, per_page=20):
		"""Get all articles with pagination"""
		return Article.query.order_by(desc(Article.updated_at)).paginate(
			page=page, per_page=per_page, error_out=False
		)

	@staticmethod
	def get_article_by_id(article_id):
		"""Get article by ID"""
		return Article.query.get_or_404(article_id)

	@staticmethod
	def get_article_by_url(url):
		"""Get article by URL"""
		return Article.query.filter_by(url=url).first()

	@staticmethod
	def get_article_versions(article_id, page=1, per_page=10):
		"""Get all versions of an article with pagination"""
		return ArticleVersion.query.filter_by(article_id=article_id) \
			.order_by(desc(ArticleVersion.crawled_at)) \
			.paginate(page=page, per_page=per_page, error_out=False)

	@staticmethod
	def get_latest_articles(page=1, per_page=20):
		"""Get latest version of each article with pagination"""
		
		articles = Article.query.order_by(desc(Article.updated_at)) \
			.paginate(page=page, per_page=per_page, error_out=False)

		return articles

	@staticmethod
	def create_or_update_article(url, headline, subheadline, content, published_at=None, last_updated_at=None):
		"""
		Create a new article or add a new version if content has changed

		Returns:
		- tuple: (article, version, is_new_article, is_new_version)
		"""
		article = ArticleService.get_article_by_url(url)
		is_new_article = False
		is_new_version = False

		if not article:
			article = Article(url=url)
			db.session.add(article)
			db.session.commit()
			is_new_article = True

		latest_version = None
		if article.versions:
			latest_version = article.versions[0] if article.versions else None

		if is_new_article or not latest_version or \
				latest_version.headline != headline or \
				latest_version.subheadline != subheadline or \
				latest_version.content != content:
			# Create new version
			version = ArticleVersion(
				article_id=article.id,
				headline=headline,
				subheadline=subheadline,
				content=content,
				published_at=published_at,
				last_updated_at=last_updated_at,
				crawled_at=datetime.utcnow(),
				content_hash=hash(content),    
    
			)
			db.session.add(version)

			# Update article's updated_at timestamp
			article.updated_at = datetime.utcnow()

			db.session.commit()
			is_new_version = True
			return article, version, is_new_article, is_new_version

		return article, latest_version, is_new_article, is_new_version