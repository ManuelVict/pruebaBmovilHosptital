from rest_framework.routers import DefaultRouter
from  chat.views import RoomViewSet,MessaggeViewSet

router =DefaultRouter()

router.register(r'rooms',RoomViewSet,basename="room")
router.register(r'messagges',MessaggeViewSet,basename="message")



urlpatterns =router.urls