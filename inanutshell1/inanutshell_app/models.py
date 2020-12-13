from django.db import models
from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login

@receiver(pre_social_login)
def populate_profile(request, sociallogin, **kwargs):    
     if sociallogin.account.provider == 'google':
        print(sociallogin.account.extra_data) 
        # username = sociallogin.account.extra_data['given_name']
                  
        # request.session['username']=username
        request.session.set_expiry(1000)



# Create your models here.
class files(models.Model):
    username=models.CharField(max_length=100,unique=False, default='no user')
    user_email=models.CharField(max_length=200, unique=False, default='no email')
    filename=models.CharField(max_length=100,unique=True)
    docs=models.FileField( unique=True)
    tag=models.CharField(max_length=100,unique=False, default='OTHER')
    summary=models.CharField(max_length=3000,unique=False, default='No Summary')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str(self):
        return self.filename
