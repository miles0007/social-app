from django.urls import path
from post import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'post'
urlpatterns = [
		path('',views.post_list,name='post_list_view'),
		path('like/',views.like_post,name='like_post'),
		path('post/<int:id>/',views.post_detail,name='post_detail'),
		path('my_post/',views.my_post,name='my_post'),
		path('edit_post/<int:id>/',views.post_edit,name='post_edit'),
		# path('delete/',views.del_view,name='del_view'),
		path('delete/<int:id>',views.post_delete,name='del_post'),
]
