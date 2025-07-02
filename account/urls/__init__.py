from django.urls import include, path

urlpatterns = [
    path("", include("account.urls.auth")),
    path("", include("account.urls.password")),
    path("", include("account.urls.verfication")),
    path("", include("account.urls.user"))
]