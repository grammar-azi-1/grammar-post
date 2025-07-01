from django.urls import path
from grammars.views import grammarrules

urlpatterns = [
    path('grammarrules/', grammarrules, name='grammarrules')
]