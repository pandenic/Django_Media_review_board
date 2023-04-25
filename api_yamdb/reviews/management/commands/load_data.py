"""Команда Django для загрузки данных в базу данных из CSV-файлов.

Пример использования:
python manage.py load_data
"""
import logging
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger.addHandler(ch)


class Command(BaseCommand):
    """Команда загружает данные для следующих моделей."""

    def handle(self, *args, **options):
        """Содержит код для загрузки в БД."""
        logger.info("Загружаю данные в базу...")

        for row in DictReader(
            open("./static/data/users.csv", encoding="utf-8"),
        ):
            user = User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                bio=row["bio"],
                role=row["role"],
            )
            user.save()
        for row in DictReader(
            open("./static/data/category.csv", encoding="utf-8"),
        ):
            category = Category(
                id=row["id"],
                name=row["name"],
                slug=row["slug"],
            )
            category.save()

        for row in DictReader(
            open("./static/data/genre.csv", encoding="utf-8"),
        ):
            genre = Genre(
                id=row["id"],
                name=row["name"],
                slug=row["slug"],
            )
            genre.save()

        for row in DictReader(
            open("./static/data/titles.csv", encoding="utf-8"),
        ):
            title = Title(
                id=row["id"],
                name=row["name"],
                year=row["year"],
                category_id=row["category"],
            )
            title.save()

        for row in DictReader(
            open("./static/data/genre_title.csv", encoding="utf-8"),
        ):
            title = Title.objects.get(id=row["title_id"])
            title.genre.add(row["genre_id"])
            title.save()

        for row in DictReader(
            open("./static/data/review.csv", encoding="utf-8"),
        ):
            review = Review(
                id=row["id"],
                title_id=row["title_id"],
                text=row["text"],
                author_id=row["author"],
                score=row["score"],
                pub_date=row["pub_date"],
            )
            review.save()

        for row in DictReader(
            open("./static/data/comments.csv", encoding="utf-8"),
        ):
            comment = Comment(
                id=row["id"],
                review_id=row["review_id"],
                text=row["text"],
                author_id=row["author"],
                pub_date=row["pub_date"],
            )
            comment.save()
        logger.info("Данные успешно загружены.")
