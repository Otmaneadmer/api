
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    # for amphitheatres
    path('api/', include('amphitheatres.urls')),
    # for admin side
    path('admin/', admin.site.urls),
]