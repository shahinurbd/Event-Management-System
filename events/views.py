from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventModelForm,ParticipantModelForm,CategoryModelForm,categoryModel
from events.models import Event,Category,Participant
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count,Q

# Create your views here.

def create_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)

        if event_form.is_valid():
            """for model data"""
            event_form.save()

            messages.success(request,"Event Created Successfully")
            return redirect('create-event')
        
    context = {
        'event_form': event_form,
    }
    return render(request,'event_form.html',context)

def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)

        if event_form.is_valid():
            """for model data"""
            event_form.save()

            messages.success(request,"Event Updated Successfully")
            return redirect('event-update',id)
        
    
    context = {"event_form":event_form}
    return render(request, "event_form.html", context)

def delete_event(request,id):
    if request.method == "POST":
        events = Event.objects.get(id=id)
        events.delete()
        messages.success(request, "Event Delete Successfully")
        return redirect('event-manage')
    else:
        messages.error(request,"Something went wrong!!")
        return redirect('event-manage')
        

def create_participant(request):
    participant_form = ParticipantModelForm()

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)

        if participant_form.is_valid():
            participant_form.save()

            messages.success(request,"Participant Created Successfully")
            return redirect('create-participant')
        
    context = {"participant_form": participant_form}
    return render(request, "participant_form.html", context)

def update_participant(request,id):
    participant = Participant.objects.get(id=id)
    participant_form = ParticipantModelForm(instance=participant)

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST,instance=participant)

        if participant_form.is_valid():
            participant_form.save()

            messages.success(request,"Participant Updated Successfully")
            return redirect('participant-update',id)
        
    context = {"participant_form": participant_form}
    return render(request, "participant_form.html", context)


def delete_participant(request,id):
    if request.method == "POST":
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.success(request, "Participant Delete Successfully")
        return redirect('event-manage')
    else:
        messages.error(request,"Something went wrong!!")
        return redirect('event-manage')


def create_category(request):
    category_form = CategoryModelForm()

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)

        if category_form.is_valid():
            category_form.save()

            messages.success(request,"Category Created Successfully")
            return redirect('create-category')
        
    

def update_category(request,id):
    category = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=category)

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST,instance=category)

        if category_form.is_valid():
            category_form.save()

            messages.success(request,"Category Updated Successfully")
            return redirect('category-update',id)
        
    context = {"category_form": category_form}
    return render(request, "category_form.html", context)

def delete_category(request,id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Category Delete Successfully")
        return redirect('event-manage')
    else:
        messages.error(request,"Something went wrong!!")
        return redirect('event-manage')

def Home(request):
    return render(request,'nav.html')

def Hero(request):
    cat = categoryModel()
    events = Event.objects.prefetch_related('participants').select_related('category').all()
    total_participant = Participant.objects.all().count()

    for event in events:
        event.participant_count=event.participants.count()

    context = {
        'events': events,
        'cat': cat
    }
    return render(request,'hero_section.html',context)



def event_card(request):
    return render(request,'event_card.html')

def event_details(request,id):
    events = Event.objects.get(id=id)
    event_date = events.Date_and_Time.date()
    event_time = events.Date_and_Time.time()
    participant = Participant.objects.filter(event=events).all()
    count_participant = participant.count()

    context = {
        'events': events,
        'participant': participant,
        'event_date': event_date,
        'event_time': event_time,
        'participant': participant,
        'count_participant': count_participant
    }

    return render(request,'event_details.html',context)

def dashboard(request):

    events = Event.objects.prefetch_related('participants').select_related('category').all()
    participant = Participant.objects.prefetch_related('event').all()

    upcoming_events = Event.objects.filter(Date_and_Time__gt=timezone.now()).order_by('Date_and_Time')
    past_events = Event.objects.filter(Date_and_Time__lt=timezone.now()).order_by('-Date_and_Time')
    today_events = Event.objects.filter(Date_and_Time__date=timezone.localdate()).order_by('Date_and_Time')


    #getting count
    total_event = events.count()
    total_participant = participant.count()
    total_upcoming_events = upcoming_events.count()
    total_past_events = past_events.count()

    #retrive event data
    type = request.GET.get('type', 'all')

    if type=='total_events':
        events = events
        messages.success(request,"Total Events")
    elif type=='upcoming_events':
        events = upcoming_events
        messages.success(request,"Upcoming Events")
    elif type=='past_events':
        events = past_events
        messages.success(request,"Past Events")
    elif type=='all':
        events = today_events
        messages.success(request,"Today's Events")
    

    for event in events:
        event.participant_count=event.participants.count()

    context = {
        'events': events,
        'total_event': total_event,
        'total_participant': total_participant,
        'total_upcoming_event': total_upcoming_events,
        'total_past_events': total_past_events,
        'today_events': today_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request,'dashboard.html',context)


def manage_event(request):
    events = Event.objects.select_related('category').all()
    participants = Participant.objects.prefetch_related('event').all()
    category = Category.objects.all()

    context = {
        'events': events,
        'participants': participants,
        'categorys': category
    }

    return render(request,'manage_event.html',context)


def search_events(request):
    query = request.GET.get('q', '') 
    events = Event.objects.select_related('category').filter(Event_Name__icontains=query) | Event.objects.select_related('category').filter(location__icontains=query)
    
    return render(request, 'hero_section.html', {'events': events, 'query': query})

def category(request):
    cat = categoryModel(request.GET)
    events = Event.objects.select_related('category').all()

    if cat.is_valid():
        category = cat.cleaned_data.get('category')
        if category:
            events = events.select_related('category').filter(category=category)

    context = {
        "cat": cat,
        "events": events
        }
    return render(request, "hero_section.html", context)

def date_filter(request):
    start_date = request.GET.get('sd','')
    end_date = request.GET.get('ed','')

    events = Event.objects.select_related('category').all()

    if start_date:
        events = events.filter(Date_and_Time__date__gte=start_date)
    if end_date:
        events = events.filter(Date_and_Time__date__lte=end_date)

    context ={
        'start_date': start_date,
        'end_date': end_date,
        'events': events
    }

    return render(request,'hero_section.html',context)






        





