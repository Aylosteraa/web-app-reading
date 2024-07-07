from django.db import models

from user.models import CustomUser


class Chat(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	message_text = models.TextField()
	posting_date = models.TextField()