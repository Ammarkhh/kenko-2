"""URLs Configuration"""
from django.contrib import admin
from django.urls import path, include

import auths.urls
import fitness.urls
import forefront.urls
import nutrition.urls
import trainer.urls

urlpatterns = []

# Admin
admin.site.site_header = "Kenko"
admin.site.index_title = "Dashboard"
admin.site.site_title = "Kenko Administration"

urlpatterns += [
    path("admin/", admin.site.urls),
]

# APIs
urlpatterns += [
    path("", include(forefront.urls.urlpatterns)),
    path("auths/", include(auths.urls.urlpatterns)),
    path("nutrition/", include(nutrition.urls.urlpatterns)),
    path("fitness/", include(fitness.urls.urlpatterns)),
    path("trainer/", include(trainer.urls.urlpatterns)),
]
