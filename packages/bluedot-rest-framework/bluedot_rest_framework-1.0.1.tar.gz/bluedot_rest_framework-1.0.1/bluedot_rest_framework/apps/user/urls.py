from rest_framework.routers import DefaultRouter
from .views import UserView

router = DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, basename='user')

urlpatterns = router.urls
