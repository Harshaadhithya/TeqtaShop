from django.db.models.signals import post_save,post_delete,pre_save
from django.contrib.auth.models import User
from .models import Profile
from inventory.models import ProductVariant


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


# from barcode import EAN13
import barcode
  
# import ImageWriter to generate an image file
from barcode.writer import ImageWriter
from teqta import settings


def save_barcode_reciever(sender,instance,created,**kwargs):
    if created:
        print("post save")
        unique_code = 'NAW00042L'

        # Now, let's create an object of EAN13 class and 
        # pass the number with the ImageWriter() as the 
        # writer
        EAN = barcode.get_barcode_class('code128')
        
        my_code = EAN(unique_code, writer=ImageWriter())
        
        # Our barcode is ready. Let's save it.
        img_name = f'{instance.id}'
        my_code.save(settings.MEDIA_ROOT + '/product_bar_code/' + img_name)
        instance.bar_code=f'product_bar_code/{img_name}.png'
        instance.save()
        

post_save.connect(save_barcode_reciever,sender=ProductVariant)


post_save.connect(user_created_reciever,sender=User)
post_delete.connect(profile_delete_receiver,sender=Profile)
