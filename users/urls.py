from django.urls import path
from users.views import sign_up,sign_in,sign_out,assign_role,create_group,group_list,active_user,delete_group

urlpatterns = [
    path('sign-up/',sign_up, name='sign-up'),
    path('sign-in/',sign_in, name='sign-in'),
    path('sign-out/',sign_out, name='sign-out'),
    path('admin/<int:user_id>/assign-role',assign_role, name='assign-role'),
    path('admin/create-group/',create_group, name='create-group'),
    path('delete-group/<int:id>',delete_group, name='delete-group'),
    path('admin/group-list/',group_list, name='group-list'),
    path('activate/<int:user_id>/<str:token>/',active_user),
]
