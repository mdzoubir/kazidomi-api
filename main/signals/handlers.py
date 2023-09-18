from django.conf import settings
from django.db.models.signals import post_save

from django.dispatch import receiver
from main.models import Customer


# django call this method when every user is created (listen to the post method in user model)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])
