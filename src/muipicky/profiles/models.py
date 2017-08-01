from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save 
from django.core.urlresolvers import reverse
from .utils import code_generator

User = settings.AUTH_USER_MODEL

class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, user_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=user_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all(): 
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

class Profile(models.Model):
    user            = models.OneToOneField(User)  # the main user's (their profile), models.ForeignKey = default  
    followers       = models.ManyToManyField(User, related_name='is_following', blank=True)  # these followers and following will be unique for each user  
    # following       = models.ManyToManyField(User, related_name='following', blank=True)
    activation_key  = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False) # default=false means that the profile is not activated by default
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        print("Activation")
        if not self.activated:
            self.activation_key = code_generator()  # generate key
            self.save()
            path_ = reverse('activate', kwargs={"code": self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: { path_ }'
            recipient_list = [self.user.email]   # the email of the person we want to send to
            html_message = f'<p>Activate your account here: { path_ }</p>'
            print(html_message)
            # sent_mail = send_mail(       # send some email here and return that object (sent_mail)
            #                 subject, 
            #                 message, 
            #                 from_email, 
            #                 recipient_list, 
            #                 fail_silently=False, 
            #                 html_message=html_message)      
            sent_mail = False
            return sent_mail

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    # after user is saved or created, want to make sure the profile exists
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get(user__id=1) #because we are creating these profiles by default, we dont need to 
        #  do get_or_create and do zero, because it returns back a tuple
        # can add the instance (sender/user that was created in this receiever function) to the followers of this user
        default_user_profile.followers.add(instance) # the good thing with manytomany is that you can just add things and remove without 
        # needing to write a save code
        # default_user_profile.followers.remove(instance)
        # default_user_profile.save() 
        profile.followers.add(default_user_profile.user)
        profile.followers.add(2)


post_save.connect(post_save_user_receiver, sender=User) # sender is the user model or can be settings.AUTH_USER_MODEL  