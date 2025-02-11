from django.urls import path
from events.views import create_event,create_participant,create_category,Home,Hero,event_card,event_details,dashboard,manage_event,update_event,update_participant,update_category,delete_event,delete_category,delete_participant,search_events,category,date_filter

urlpatterns = [
    path('',Hero),
    path('event-form/', create_event, name="create-event"),
    path('participant-form/', create_participant, name="create-participant"),
    path('category-form/', create_category, name="create-category"),
    path('home/',Home),
    path('hero/',Hero,name="home"),
    path('event-card',event_card),
    path('event-details/<int:id>/',event_details, name='event-details'),
    path('dashboard/',dashboard, name='dashboard'),
    path('event-manage/',manage_event,name='event-manage'),
    path('event-update/<int:id>/',update_event,name='event-update'),
    path('participant-update/<int:id>/',update_participant,name='participant-update'),
    path('category-update/<int:id>/',update_category,name='category-update'),
    path('event-delete/<int:id>/',delete_event,name='event-delete'),
    path('participant-delete/<int:id>/',delete_participant,name='participant-delete'),
    path('category-delete/<int:id>/',delete_category,name='category-delete'),
    path('search/', search_events, name='search_events'),
    path('category/', category, name='category'),
    path('date/', date_filter, name='date_filter'),
]
