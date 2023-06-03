from django.urls import path
from . views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('signup',signup,name='signup'),
    path('',getRoutes,name='routes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_snippet',create_snippet,name='create_snippet'),
    path('overview/', overview, name='overview'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('update_snippet/<int:pk>',update_snippet,name='update_snippet'),
    path('delete_snippet/<int:pk>',delete_snippet,name='delete_snippet'),
    path('list_tags',list_tags,name='list_tags'),
    path('snippet_tag/<int:pk>',snippet_tag,name='snippet_tag')
]