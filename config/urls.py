from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path("products/", include("products.urls")),
    path("cart/", include("cart.urls")),


    # Rosetta
    path('rosetta/', include('rosetta.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
