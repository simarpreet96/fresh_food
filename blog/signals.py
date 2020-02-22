from django.db.models import signals
from django.dispatch import receiver
from .models import Post


#pre_save method signal
@receiver(signals.pre_save, sender=Post)
def check_product_description(sender, instance, **kwargs):
	if not instance.text:
		instance.text = 'This is Default Description'

#post_save method
@receiver(signals.post_save, sender=Post)
def create_product(sender, instance, created, **kwargs):
	print("Save method is called")
