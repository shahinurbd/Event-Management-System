from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm,categoryModel
from events.models import Event,Category
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count,Q
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from django.contrib.auth.models import User,Group
from django.db.models import Prefetch
from users.views import is_admin
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect


User = get_user_model()



# Create your views here.

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()

@login_required
@permission_required('events.add_event', login_url='no-permission')
def create_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)

        if event_form.is_valid():
            """for model data"""
            event_form.save()

            messages.success(request,"Event Created Successfully")
            return redirect('create-event')
        
    context = {
        'event_form': event_form,
    }
    return render(request,'event_form.html',context)

@login_required
@permission_required('events.change_event', login_url='no-permission')
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

@login_required
@permission_required('events.delete_event', login_url='no-permission')
def delete_event(request,id):
    if request.method == "POST":
        events = Event.objects.get(id=id)
        events.delete()
        messages.success(request, "Event Delete Successfully")
        return redirect('admin-dashboard')
    else:
        messages.error(request,"Something went wrong!!")
        return redirect('admin-dashboard')
        



@login_required
@permission_required('events.delete_participant', login_url='no-permission')
def delete_participant(request,id):
    if request.method == "POST":
        participant = User.objects.get(id=id)
        participant.delete()
        messages.success(request, "User Delete Successfully")
        return redirect('manage-user')
    else:
        messages.error(request,"Something went wrong!!")
        return redirect('manage-user')

@login_required
@permission_required('events.add_category', login_url='no-permission')
def create_category(request):
    category_form = CategoryModelForm()

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)

        if category_form.is_valid():
            category_form.save()

            messages.success(request,"Category Created Successfully")
            return redirect('create-category')
        
    context = {'category_form': category_form}
    
    return render(request,'category_form.html',context)
        
    
@login_required
@permission_required('events.change_category', login_url='no-permission')
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

@login_required
@permission_required('events.delete_category', login_url='no-permission')
def delete_category(request,id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Category Delete Successfully")
        return redirect('admin-dashboard')
    else:
        messages.error(request,"Something went wrong!!")
        return redirect('admin-dashboard')

def Home(request):
    return render(request,'nav.html')

@login_required
@permission_required('events.view_event', login_url='no-permission')
def Hero(request):
    cat = categoryModel(request.GET)
    query = request.GET.get('q', '')
    events = Event.objects.prefetch_related('participants').select_related('category').all()
    events = Event.objects.select_related('category').filter(Event_Name__icontains=query) | Event.objects.select_related('category').filter(location__icontains=query)
    start_date = request.GET.get('sd','')
    end_date = request.GET.get('ed','')
    if start_date:
        events = events.filter(Date_and_Time__date__gte=start_date)
    if end_date:
        events = events.filter(Date_and_Time__date__lte=end_date)

    if cat.is_valid():
        category = cat.cleaned_data.get('category')
        if category:
            events = events.select_related('category').filter(category=category)

    for event in events:
        event.participant_count=event.participants.count()

    context = {
        'events': events,
        'cat': cat,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request,'hero_section.html',context)



def event_card(request):
    return render(request,'event_card.html')

@login_required
@permission_required('events.view_event', login_url='no-permission')
def event_details(request,event_id):
    events = Event.objects.get(id=event_id)
    event_date = events.Date_and_Time.date()
    event_time = events.Date_and_Time.time()
    participants = events.participants.all()

    context = {
        'events': events,
        'participants': participants,
        'event_date': event_date,
        'event_time': event_time,
        
    }

    return render(request,'event_details.html',context)


# @login_required
# @permission_required('events.view_event', login_url='no-permission')
# def dashboard(request):

#     events = Event.objects.prefetch_related('participants').select_related('category').all()
#     participant = User.objects.all()

#     upcoming_events = Event.objects.filter(Date_and_Time__gt=timezone.now()).order_by('Date_and_Time')
#     past_events = Event.objects.filter(Date_and_Time__lt=timezone.now()).order_by('-Date_and_Time')
#     today_events = Event.objects.filter(Date_and_Time__date=timezone.localdate()).order_by('Date_and_Time')


#     #getting count
#     total_event = events.count()
#     total_participant = participant.count()
#     total_upcoming_events = upcoming_events.count()
#     total_past_events = past_events.count()

    # #retrive event data
    # type = request.GET.get('type', 'all')

    # if type=='total_events':
    #     events = events
    #     messages.success(request,"Total Events")
    # elif type=='upcoming_events':
    #     events = upcoming_events
    #     messages.success(request,"Upcoming Events")
    # elif type=='past_events':
    #     events = past_events
    #     messages.success(request,"Past Events")
    # elif type=='all':
    #     events = today_events
    #     messages.success(request,"Today's Events")
    

    # for event in events:
    #     event.participant_count=event.participants.count()

    # context = {
    #     'events': events,
    #     'total_event': total_event,
    #     'total_participant': total_participant,
    #     'total_upcoming_event': total_upcoming_events,
    #     'total_past_events': total_past_events,
    #     'today_events': today_events,
    #     'upcoming_events': upcoming_events,
    #     'past_events': past_events,
    # }
    # return render(request,'dashboard.html',context)

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    events = Event.objects.select_related('category').all()
    participants = User.objects.all()
    category = Category.objects.all()

    context = {
        'events': events,
        'participants': participants,
        'categorys': category
    }

    return render(request,'dashboard/admin_dashboard.html',context)

@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    events = Event.objects.select_related('category').all()
    participants = User.objects.all()
    category = Category.objects.all()

    context = {
        'events': events,
        'participants': participants,
        'categorys': category
    }

    return render(request,'dashboard/organizer_dashboard.html',context)

@login_required
def user_dashboard(request):
    events = request.user.rsvp_event.all()
    return render(request, 'dashboard/user_dashboard.html', {'events': events})
   

@login_required
@permission_required('events.change_event', login_url='no-permission')
def manage_event(request):
    events = Event.objects.select_related('category').all()
    participants = User.objects.all()
    category = Category.objects.all()

    context = {
        'events': events,
        'participants': participants,
        'categorys': category
    }

    return render(request,'manage_event.html',context)

@user_passes_test(is_admin, login_url='no-permission')
def manage_user(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assigned"

    return render(request,'manage_user.html',{"users": users})



@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.participants.add(request.user)
    messages.success(request, "Congratulations!! 🎉 You have successfully joined this event. ")
    return redirect('event-details', event_id=event.id)

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_user(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_mail(
                subject=contact.subject,
                message=contact.message,
                from_email=contact.email,
                recipient_list=['shahinurislam728@gmail.com'],
            )
            messages.success(request, "Your message has been sent successfully!")

            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})












        





