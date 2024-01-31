from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, password):
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('Firstname is required')
        if not last_name:
            raise ValueError('Lastname is required')
        if not password:
            raise ValueError('Password is required')
        
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, first_name, last_name, username, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password 
        )
        user.is_admin = True
        user.is_staff
        user.is_superuser = True
        user.is_active = True
        user.is_new = False
        user.save()
        return user
    
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True,null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name','last_name'], name='unique_first_last_name')
        ]
    objects = UserManager()
    def __str__(self):
        return f'user - {self.username}'
     
    def has_perm(self, perm, object = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'Profile for user - {self.user.username}'