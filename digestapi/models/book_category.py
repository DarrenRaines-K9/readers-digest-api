from django.db import models


class BookCategory(models.Model):
    book = models.ForeignKey(
        "Books", on_delete=models.CASCADE, related_name="bookcategory"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="bookcategory"
    )
    time_stamp = models.DateTimeField()
