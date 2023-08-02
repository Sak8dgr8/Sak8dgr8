from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import EditProjectView
from .views import AddSubscriber
from .views import RemoveSubscriber
# from .views import PaypalFormView


urlpatterns = [
   
  # path('loda', PaypalFormView.as_view(), name='bigloda'),
   path('payment_completed', views.payment_completed_view, name='payment_completed'),
   path('payment_failed', views.payment_failed_view, name='payment_failed'),
  # path('loda', views.bigloda, name='bigloda'),
   path('login', views.login_user, name='login_user'),
   path('logout_user', views.logout_user, name='logout'),
   path('register_user', views.register_user, name='register_user'),

   path('user_channel/<str:username>/subscribers/add', AddSubscriber.as_view(), name='add_subscriber'),
   path('user_channel/<str:username>/subscribers/remove', RemoveSubscriber.as_view(), name='remove_subscriber'),

   path('user_channel/<str:username>/', views.user_channel, name='user_channel'),
   path('completed_channel/<str:username>/<int:project_id>', views.completed_channel, name='completed_channel'),
   path('no_project', views.no_project, name='no_project'),
   path('channel_customization', views.channel_customization, name='channel_customization'),
   path('funding_info', views.funding_info, name='funding_info'),

   path('edit_project/<int:pk>/', EditProjectView.as_view(), name='edit_project'),
   path('funding_now/', views.FundingNowView.as_view(), name='funding_now'),
   path('go_live/<int:project_id>/', views.go_live, name='go_live'),
   
   path('search/', views.ProjectSearchView.as_view(), name='search_projects'),
   path('donation_history', views.donation_history, name='donation_history'),
   path('donate/<int:project_id>/', views.donation_landing_page, name='donation_landing_page'),
   path('payment_info/', views.payment_info, name='payment_info'),

   

   path('update/<int:project_id>/', views.update_project, name='project_update'),
   path('project/<int:project_id>/update/<int:update_id>/', views.update_detail, name='update-detail'),

   path('project/<int:project_id>/complete/', views.complete_project, name='complete_project'),
   path('user/<str:username>/completed_projects/', views.completed_projects, name='completed_projects'),
]
