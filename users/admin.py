from django.contrib import admin
from .models import ProfileModel
from blog.models import Messages

# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(Messages)
