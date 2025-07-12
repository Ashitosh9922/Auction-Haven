from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BidViewSet, CommentViewSet, UserViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bids', BidViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
