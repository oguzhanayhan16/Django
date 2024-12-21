from django.contrib import admin
from .models import Blog,Writer
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    readonly_fields=('slug',)

admin.site.register(Blog,BlogAdmin)
admin.site.register(Writer,BlogAdmin)