from django.urls import path
from events.views import create_event,create_category,Hero,event_card,event_details,dashboard,manage_event,update_event,update_category,delete_event,delete_category,delete_participant,join_event,manage_user,admin_dashboard,organizer_dashboard,user_dashboard,about,contact

urlpatterns = [
    path('event-form/', create_event, name="create-event"),
    path('category-form/', create_category, name="create-category"),
    path('hero/',Hero,name="hero"),
    path('event-card',event_card),
    path('event-details/<int:event_id>/',event_details, name='event-details'),
    path('dashboard/',dashboard, name='dashboard'),
    path('event-manage/',manage_event,name='event-manage'),
    path('event-update/<int:id>/',update_event,name='event-update'),
    path('event-delete/<int:id>/',delete_event,name='event-delete'),
    path('category-update/<int:id>/',update_category,name='category-update'),
    path('category-delete/<int:id>/',delete_category,name='category-delete'),
    path('participant-delete/<int:id>/',delete_participant,name='participant-delete'),
    path('join-event/<int:event_id>/',join_event,name='join-event'),
    path('manage-user/',manage_user,name='manage-user'),
    path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
    path('organizer-dashboard/',organizer_dashboard,name='organizer-dashboard'),
    path('user-dashboard/',user_dashboard,name='user-dashboard'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
]
