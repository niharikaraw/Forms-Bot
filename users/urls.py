
from django.urls import path
#from formsBotBackend.users.views import ContactUsView, FeedbackView, ResponseView

from users.views import BotsView, CampaignView, CreateUserView, ProfileView,ResponseView,ContactUsView,FeedbackView

urlpatterns = [
    path ('user-view/', CreateUserView.as_view(), name='user-view'),
    path ('user-profile/', ProfileView.as_view(), name='user-profile'),
    path('campaign-view/', CampaignView.as_view(), name='campaign-view'),
    path('bot-view/', BotsView.as_view(), name='bot-view'),
    path('response-view/', ResponseView.as_view(), name='response-view'),
    path('contactus-view/', ContactUsView.as_view(), name='contactus-view'),
    path('feedback-view/', FeedbackView.as_view(), name='feedback-view'),
    
]