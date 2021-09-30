from rest_framework.routers import SimpleRouter

from django.urls import path, include

from review.views import *


router = SimpleRouter()
router.register('review', ReviewViewSet, 'review')

urlpatterns = [
    path('', include(router.urls))
]
