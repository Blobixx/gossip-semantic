import factory
from datetime import datetime
from uuid import uuid4
from app.models.Articles import Articles


class ArticleFactory(factory.alchemy.SQLAlchemyModelFactory):
    uuid = factory.Faker("uuid4")
    site_name = "Test Site"
    author = "Some Author"
    url = factory.Sequence(lambda n: f"https://vsd.fr/{n}")
    title = factory.Sequence(lambda n: f"Title {n}")
    published_at = factory.LazyFunction(datetime.now)
    content = "Content"
    description = "Description"
    embeddings = None

    class Meta:
        model = Articles
        sqlalchemy_session_persistence = "commit"
