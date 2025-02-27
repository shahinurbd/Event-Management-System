from django.db.models.signals import post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.forms import Event

@receiver(m2m_changed, sender=Event.participants.through)
def notify_employee_on_task_creation(sender, instance,action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.participants.all()]

        send_mail(
            "Joined a new event",
            f"Congratulations!!... You have been joined to the event: {instance.Event_Name} on {instance.Date_and_Time} at {instance.location}",
            "shahinurislam728@gmail.com",
            assigned_emails,
        )