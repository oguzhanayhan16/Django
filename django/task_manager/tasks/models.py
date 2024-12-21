from django.db import models
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
# Create your models here.

class Writer(models.Model):
    WriterName = models.CharField(max_length=50, unique=True)
    
    WriterMail = models.EmailField(max_length=200, unique=True)
    WriterPassword = models.CharField(max_length=128)
    WriterAbout = models.CharField(max_length=250,null=True)
    WriterImage=models.ImageField(upload_to="writer",null=True)
    WriterStatus = models.BooleanField(default=True)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.WriterName)
            self.WriterPassword = make_password(self.WriterPassword)
        super(Writer, self).save(*args, **kwargs)
    def __str__(self):
        return self.WriterName   
    @property
    def is_authenticated(self):
        return True

    def check_password(self, password):
       
        return check_password(password, self.WriterPassword)   
      



class Blog(models.Model):
        
    BlogTitle = models.CharField(max_length=50)
    BlogContent = models.CharField(max_length=200)
    BlogImage =  models.ImageField(upload_to="blogs")
    BlogCreateDate = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    writer = models.ForeignKey(Writer,null=True,on_delete=models.SET_NULL)

    def save(self, *args,**kwargs):
        self.slug=slugify(self.BlogTitle)
        super().save(*args,**kwargs)




   
 