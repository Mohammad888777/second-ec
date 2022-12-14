from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path('admin/', admin.site.urls),
    path("store/",include("store.urls")),
    path("carts/",include("carts.urls")),
    path("accounts/",include("accounts.urls")),
    # path("category/",include("category.urls")),
    

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
