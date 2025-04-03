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
    Retrieve all articles with pagination.

    Retrieves a paginated list of all articles from the database.

    Args:
        page (int): The page number to retrieve. Defaults to 1.
        per_page (int): The number of articles per page. Defaults to 20.

    Returns:
        Response: A JSON response containing the articles and pagination metadata.
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
    Retrieve the latest version of each article with pagination.

    Args:
        page (int): The page number to retrieve. Defaults to 1.
        per_page (int): The number of articles per page. Defaults to 20.

    Returns:
        Response: A JSON response containing the latest articles and pagination metadata.
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
    Retrieve a single article by its ID.

    Args:
        article_id (int): The ID of the article to retrieve.

    Returns:
        Response: A JSON response containing the article data.
    """
    article = ArticleService.get_article_by_id(article_id)
    return jsonify(article_schema.dump(article)), 200


@api_bp.route('/articles/<int:article_id>/versions', methods=['GET'])
def get_article_versions(article_id):
    """
    Retrieve all versions of a specific article with pagination.

    Args:
        article_id (int): The ID of the article.
        page (int): The page number to retrieve. Defaults to 1.
        per_page (int): The number of versions per page. Defaults to 10.

    Returns:
        Response: A JSON response containing the versions and pagination metadata.
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
    Manually trigger the web crawler to scrape articles.

    Returns:
        Response: A JSON response indicating the success of the crawl and the number of URLs processed.
    """
    crawler = Crawler()
    article_links = crawler.crawl_overview_page()

    return jsonify({
        'status': 'success',
        'message': f'Crawler job completed. Processed {len(article_links)} article URLs.'
    }), 200


def register_routes(app):
    """
    Register all blueprints to the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(api_bp)
