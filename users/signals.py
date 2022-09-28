from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from .models import Profile


def user_created_reciever(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email
        )

def profile_delete_receiver(sender,instance,**kwargs):
    try:
        user_record=instance.user
        user_record.delete()
    except:
        pass


post_save.connect(user_created_reciever,sender=User)
post_delete.connect(profile_delete_receiver,sender=Profile)
