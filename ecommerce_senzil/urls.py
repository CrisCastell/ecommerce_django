from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from usuarios.views import registro_cliente
from productos.urls import urlpatterns as productos_urls
from django.conf import settings
from django.conf.urls.static import static
from productos.admin import custom_admin_site 
urlpatterns = []


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('registro/', registro_cliente, name='registro_cliente'),
    path('api/', include(productos_urls)),
    path('', custom_admin_site.urls),
    # path('', admin.site.urls),

]

