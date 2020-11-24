from django.contrib import admin

# Register your models here.
from .models import Items, Payment, Users, UserItem

admin.site.register(Items)
admin.site.register(Payment)
admin.site.register(Users)
admin.site.register(UserItem)