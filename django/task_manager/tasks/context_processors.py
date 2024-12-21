from .models import Blog

def last_3_blogs(request):
    blogs = Blog.objects.all().order_by('-BlogCreateDate')[:3]
    return {'last_3_blogs': blogs}