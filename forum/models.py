from django.db import models
from books.models import Book
from user.models import CustomUser


class Message(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	message_text = models.TextField()
	posting_date = models.DateTimeField(null=True)
