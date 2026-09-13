from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from courses.models import Course


@registry.register_document
class CourseDocument(Document):
    """
    Elasticsearch document for Course model.
    Maps model fields to Elasticsearch field types for optimal search.
    """

    # Keyword fields for filtering and aggregations
    category = fields.KeywordField(attr="category")

    class Index:
        name = "courses"

        # Index settings for analysis and performance
        settings = {
            "analysis": {
                "filter": {
                    "shingle": {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 3,
                    }
                },
                "analyzer": {
                    "default": {
                        "type": "standard",
                        "stopwords": "_english_",
                    },
                    "trigram": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "shingle"],
                    },
                },
            },
        }

    class Django:
        model = Course

        fields = [
            "id",
            "slug",
            "is_active",
            "title",
            # "thumbnail",
            "description",
            "price",
        ]

        ignore_signals = False
        auto_refresh = True

        # Only index active products
        queryset_pagination = 1000  # Batch size for indexing
