from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book, Chapter

# Create your models here.

class CustomUser(AbstractUser):
	avatar = models.ImageField(upload_to='static/img/avatar/')

class UserLibrary(models.Model):
	BOOK_CHOICES = [
			('F', 'Finished'),
			('IP', 'InProcess'),
			('GO', 'GiveOver'),
			('P', 'Planned'),
			('C', 'Created'),
		]

	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	start_date = models.DateTimeField(null=True)
	last_date = models.DateTimeField(null=True)
	choices = models.CharField(max_length=2, choices=BOOK_CHOICES)


class Review(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	textofreview = models.TextField()
	likes = models.IntegerField(null=True)
	rating = models.IntegerField(null=True)
	posting_date = models.DateTimeField(null=True)

class Comentary(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	chapter_number = models.ForeignKey(Chapter, on_delete=models.CASCADE)
	textofcomentary = models.TextField()
	posting_date = models.DateTimeField(null=True)

class Like(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	review_id = models.ForeignKey(Review, on_delete=models.CASCADE)