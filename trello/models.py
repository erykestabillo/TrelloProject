from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def publish(self):
        self.date_created = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class BoardList(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class ListCard(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    board_list = models.ForeignKey(BoardList, on_delete=models.CASCADE, null=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class TrelloUserManager(BaseUserManager):

    def create_user(self,name,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            name=name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,name, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class TrelloUser(AbstractBaseUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = TrelloUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

