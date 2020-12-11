
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.dispatch import receiver


from .models import Customer



@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user = instance,
            name = instance.username,
            email = instance.email,
        )

        print('Profile Created!')
    
#post_save.connect(customer_profile, sender=User)


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):

    if created == False:
        instance.customer.save()
        print('profile updated')



