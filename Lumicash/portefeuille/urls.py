from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import Power, ViewReque, checki
from .login import LogUser
# from rest_framework.permissions import IsAdminOrIsSelf
# from portefeuille.permissions import IsAdminOrIsSelf


router = DefaultRouter()
router.register(r"", Power, basename='powr')

urlpatterns = router.urls
urlpatterns += [
    path('log/', LogUser.as_view(), name='authentification'),
    path('home/', ViewReque.as_view(), name='home'),
    # path('ch/', checki, name='check'),
]

print(f"The URL CONF (PORTEFEUILLE):\n{urlpatterns}")