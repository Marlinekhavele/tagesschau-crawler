from flask import Blueprint, jsonify, request
from app.service.article import ArticleService
from app.schemas.article import ArticleSchema, ArticleVersionSchema, ArticleWithLatestVersionSchema
from crawler.crawler import Crawler

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize schemas
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
article_version_schema = ArticleVersionSchema()
article_versions_schema = ArticleVersionSchema(many=True)
article_with_latest_schema = ArticleWithLatestVersionSchema()
articles_with_latest_schema = ArticleWithLatestVersionSchema(many=True)


# Routes
@api_bp.route('/articles', methods=['GET'])
def get_articles():
	"""
	Get all articles with pagination
	"""
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page', 20, type=int)

	paginated_articles = ArticleService.get_all_articles(page, per_page)

	return jsonify({
		'articles': articles_schema.dump(paginated_articles.items),
		'pagination': {
			'page': paginated_articles.page,
			'per_page': paginated_articles.per_page,
			'total_pages': paginated_articles.pages,
			'total_items': paginated_articles.total
		}
	}), 200


@api_bp.route('/articles/latest', methods=['GET'])
def get_latest_articles():
	"""
	Get latest version of each article with pagination
	"""
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page', 20, type=int)

	paginated_articles = ArticleService.get_latest_articles(page, per_page)

	return jsonify({
		'articles': articles_with_latest_schema.dump(paginated_articles.items),
		'pagination': {
			'page': paginated_articles.page,
			'per_page': paginated_articles.per_page,
			'total_pages': paginated_articles.pages,
			'total_items': paginated_articles.total
		}
	}), 200


@api_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
	"""
	Get article by ID
	"""
	article = ArticleService.get_article_by_id(article_id)
	return jsonify(article_schema.dump(article)), 200


@api_bp.route('/articles/<int:article_id>/versions', methods=['GET'])
def get_article_versions(article_id):
	"""
	Get all versions of an article with pagination
	"""
	page = request.args.get('page', 1, type=int)
	per_page = request.args.get('per_page', 10, type=int)

	paginated_versions = ArticleService.get_article_versions(article_id, page, per_page)

	return jsonify({
		'article_id': article_id,
		'versions': article_versions_schema.dump(paginated_versions.items),
		'pagination': {
			'page': paginated_versions.page,
			'per_page': paginated_versions.per_page,
			'total_pages': paginated_versions.pages,
			'total_items': paginated_versions.total
		}
	}), 200


@api_bp.route('/crawler/run', methods=['POST'])
def run_crawler():
	"""
	Manually trigger crawler to run
	"""
	crawler = Crawler()
	article_links = crawler.crawl_overview_page()

	return jsonify({
		'status': 'success',
		'message': f'Crawler job completed. Processed {len(article_links)} article URLs.'
	}), 200


def register_routes(app):
	"""
	Register all blueprints
	"""
	app.register_blueprint(api_bp)