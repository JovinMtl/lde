from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_nested.routers import NestedSimpleRouter


from .views import show_person, apiRoot
from .users import injira, check_user_authenticated,\
      userTime
from .operations.view1 import UserMan, UserViewSet
from .operations.view2 import RequeWithdrwawViewSet, ManageUser


# user_list = UserViewSet.as_view({'get': 'list'})
# user_detail = UserViewSet.as_view({'get': 'retrieve'})

router = DefaultRouter()
router.register(r'api/users/', UserViewSet, basename='userrr')
router.register(r'api/reque', RequeWithdrwawViewSet, basename='req')
# router.register(r'api/reque/', RequeViewSet, basename='reque' )

urlpatterns = [
	path('', include(router.urls)),
    path('api/', apiRoot),
    path('api/test/', ManageUser.as_view()),
    path('api/lo/', injira),
    path('api/check/', check_user_authenticated),
    path('api/time/', userTime),
    # path('api/fund/', addFund),
    path('api/user/', ManageUser.as_view()),
    # path('api/users/', user_list),
    # path('api/approve/', Approve.as_view())

]
# urlpatterns += router.urls

print(f"################ROUTES###############:\n{router.urls}")
# ^api/reque//(?P<pk>[^/.]+)/approve/$