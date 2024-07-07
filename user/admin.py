from django.contrib import admin
from .models import CustomUser, UserLibrary, Review, Comentary, Like

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserLibrary)
admin.site.register(Review)
admin.site.register(Comentary)
admin.site.register(Like)
