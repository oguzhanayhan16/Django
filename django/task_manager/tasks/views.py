from django.shortcuts import render,redirect,get_object_or_404
from tasks.models import Blog,Writer
from django.contrib.auth import authenticate,login,logout
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
def index(request):
    context = {
        "blogs": Blog.objects.all()  
    }

    return render(request,"blog/index.html",context)


def blogs(request):
        return render(request,"blog/BlogRead.html")



def blog_details(request,slug):
    blog = Blog.objects.get(slug=slug)
    
    return render(request, "blog/blogDetails.html", {"blog": blog})


def login_request(request):
    if  request.user.is_authenticated:
         return redirect('/')
         
    if request.method == 'POST':
        WriterMail = request.POST["mail"]
        WriterPassword = request.POST["password"]

        writer = authenticate(request, WriterMail=WriterMail, password=WriterPassword)

        if writer is not None:
            login(request, writer)  # Kullanıcı oturum açar
            return redirect("/")
        else:
            return render(request, "blog/login.html", {
                "error": "Yazar adı ya da parola yanlış"
            })

    return render(request, "blog/login.html")
def register(request):
     if  request.user.is_authenticated:
         return redirect('/')
     if request.method=='POST':
          WriterName= request.POST['name']
          WriterMail= request.POST['mail']
          WriterAbout= request.POST['about']
          WriterImage = request.FILES['image']
          WriterPassword= request.POST['password']
          WriterRePassword= request.POST['repassword']
         

          if WriterPassword == WriterRePassword:
            if Writer.objects.filter(WriterMail=WriterMail).exists():
                return render(request,"blog/register.html",{"error":"Mail adresi kullanılıyor."})
            else:
                 writer =Writer.objects.create(WriterName=WriterName,WriterMail=WriterMail,WriterPassword=WriterPassword,WriterAbout=WriterAbout,WriterImage=WriterImage)
                 writer.save()

                 writer = authenticate(request, WriterMail=WriterMail, password=WriterPassword)

                 if writer is not None:
                    login(request, writer) 
                    return redirect("/")
          else :
                  return render(request,"blog/register.html",{"error":"Parolalar eşleşmiyor"})   



     return render(request,"blog/register.html")

def logout_request(request):
     logout(request)
     return redirect('/')

def createBlog(request):
      if not request.user.is_authenticated: 
        return redirect('/') 
      if request.method=='POST':
          BlogTitle= request.POST['title']
          BlogContent= request.POST['content']
          BlogImage = request.FILES['image']
          writer_id = request.POST['id']
          
          writer = get_object_or_404(Writer, id=writer_id)
          BlogTitle=BlogTitle.strip()  
          if Blog.objects.filter(BlogTitle__iexact=BlogTitle.strip()).exists():
            return render(request, "blog/createBlog.html", {"error": "Bu isimli blog bulunmaktadır."})
          

        

        
          blog =Blog.objects.create(BlogTitle=BlogTitle,BlogContent=BlogContent,BlogImage=BlogImage,writer=writer)
          blog.save()
          return render(request,"blog/createBlog.html",{"success":"Blog başarıyla oluşturulmuştur."})
      else:
                return render(request,"blog/createBlog.html")
def writerBlogs(request):
    if not request.user.is_authenticated: 
        return redirect('/') 
    context = {
        "blogs": Blog.objects.filter(writer=request.user.id)  
    }

    return render(request,"blog/writerBlogs.html",context)
          
 
def editBlog(request,slug):
     if not request.user.is_authenticated: 
        return redirect('/') 
     blog = Blog.objects.get(slug=slug)
     if request.method=='POST':
          BlogTitle= request.POST['title']
          BlogContent= request.POST['content']
          if 'image' in request.FILES:
                BlogImage = request.FILES['image']
          else:
            BlogImage = None
          writer_id = request.POST['id']
          
          writer = get_object_or_404(Writer, id=writer_id)

          if blog.BlogTitle.strip() != BlogTitle.strip():
           if Blog.objects.filter(BlogTitle__iexact=BlogTitle.strip()).exists():
            return render(request, "blog/createBlog.html", {"error": "Bu isimli blog bulunmaktadır."})
           
        

        
          blog.BlogTitle = BlogTitle
          blog.BlogContent = BlogContent
          if BlogImage is None:
            blog.BlogImage =blog.BlogImage  
          else:
              blog.BlogImage = BlogImage  
          blog.writer = writer
        
          blog.slug = slugify(BlogTitle)
          blog.save()
          return render(request,"blog/createBlog.html",{"success":"Blog başarıyla güncellenmiştir.",
                                                        "blog": blog})

     return render(request,"blog/editBlog.html",{"blog": blog})



def editWriter(request,slug):
    if not request.user.is_authenticated: 
        return redirect('/')
    try:
        writer = Writer.objects.get(slug=slug)
    except Writer.DoesNotExist:
        return redirect('/')  
    
    # Yalnızca kullanıcı kendi profilini düzenleyebilir
    if request.user.slug == writer.slug:
        if request.method == 'POST':
            # POST verilerini al
            WriterName = request.POST['name']
            WriterMail = request.POST['mail']
            
            # Resim var mı kontrol et
            if 'image' in request.FILES:
                WriterImage = request.FILES['image']
            else:
                WriterImage = None

            # Şifre varsa, yeni şifreyi al
            if 'password' in request.POST:
                WriterPassword = request.POST['password']
            else:
                WriterPassword = None  
            
            WriterAbout = request.POST['about']

            # Güncellemeleri yazara uygula
            writer.WriterName = WriterName
            writer.WriterMail = WriterMail
            writer.WriterAbout = WriterAbout
            if WriterPassword:
                writer.WriterPassword = make_password(WriterPassword)
            
            if WriterImage:
                writer.WriterImage = WriterImage
            else:
                writer.WriterImage = writer.WriterImage 
            
            writer.slug = slugify(WriterName)
            writer.save()

        return render(request, "blog/editWriter.html", {"writer": writer})
    else:
        return redirect('/')  


def writerPage(request,slug):
    writer = Writer.objects.get(slug=slug)
    blogs = Blog.objects.filter(writer=writer)
    return render(request,"blog/writerPage.html",{"writer":writer,"blogs":blogs})

def aboutUs(request):
    return render(request,"blog/aboutUs.html")

def writers(request):
    writer = Writer.objects.all()
    return render(request,"blog/writers.html",{"writer":writer})

def deleteBlog(request,slug):
    blog = Blog.objects.get(slug=slug)
    if request.user == blog.writer:
        blog.delete()
        return redirect('/')  
    else:
        return redirect('blogDetails', slug=slug)
    
def search_view(request):
    query = request.GET.get('Search', '')  # Arama kelimesini alıyoruz
    results = Blog.objects.filter(BlogTitle__icontains=query)  # Blog başlığı içinde arama yapıyoruz
    
    return render(request, 'blog/searchBar.html', {
        'query': query,
        'results': results
    })
    