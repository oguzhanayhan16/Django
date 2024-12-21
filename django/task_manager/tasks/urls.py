#http://127.0.0.1:8000

from django.urls import path
from . import views
urlpatterns=[
    path("",views.index ,name="blog"),
    path("index",views.index),
    path("about_us",views.aboutUs,name="aboutUs"),
    path("writers",views.writers,name="writers"),
    path("blogRead/<int:id>",views.blogs),
    path("login",views.login_request,name="login"),
    path("logout",views.logout_request,name="logout"),
    path("register",views.register,name="register"),
    path("create_blog",views.createBlog,name="createBlog"),
    path("writer_blogs",views.writerBlogs,name="writerBlogs"),
    path("edit_blog/<slug:slug>",views.editBlog,name="editBlog"),
    path("edit_writer/<slug:slug>",views.editWriter,name="editWriter"),
    path("writer_page/<slug:slug>",views.writerPage,name="writerPage"),
    path("delete_blog/<slug:slug>",views.deleteBlog,name="deleteBlog"),
    path('search/', views.search_view, name='search'),
    path("blogDetails/<slug:slug>",views.blog_details,name="blog_details")
]