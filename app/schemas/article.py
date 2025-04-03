from marshmallow import Schema, fields

class ArticleVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    headline = fields.Str(required=True)
    subheadline = fields.Str(allow_none=True)
    content = fields.Str(required=True)
    published_at = fields.DateTime(allow_none=True)
    last_updated_at = fields.DateTime(allow_none=True)
    crawled_at = fields.DateTime(dump_only=True)


class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    versions = fields.List(fields.Nested(ArticleVersionSchema), dump_only=True)


class ArticleWithLatestVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    latest_version = fields.Nested(ArticleVersionSchema, attribute="versions[0]")