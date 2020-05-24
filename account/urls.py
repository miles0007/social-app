from django.urls import path
from django.contrib.auth import views as auth_views
from account import views
from django.conf import settings
from django.conf.urls.static import static
from post.views import *

urlpatterns = [
      # path('login/',auth_views.LoginView.as_view(),name='login'),
      path('login/',views.user_login,name='login'),
      path('logout/',views.logout_function,name='logout'),
      path('register/',views.register,name='register'),
      path('',views.post_list,name='dashboard'),
      path('profile/',views.edit,name='edit'),
      path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
      path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),

]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)