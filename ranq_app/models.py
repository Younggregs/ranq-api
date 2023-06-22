import uuid
from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class TypeEnum(Enum):
    public = 'public'
    private = 'private'
    
TYPES = tuple((item.value, item.name) for item in list(TypeEnum))

class StatusEnum(Enum):
    ongoing = 'ongoing'
    completed = 'completed'
    
STATUSES = tuple((item.value, item.name) for item in list(StatusEnum))

class EmailTypeEnum(Enum):
    signup_email = 'signup_email'
    vote_email = 'vote_email'
    forgot_password = 'forgot_password'
    
    
EMAIL_TYPES = tuple((item.value, item.name) for item in list(EmailTypeEnum))

class BaseModel(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    is_deleted = models.BooleanField(default = False)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

class User(AbstractUser):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(_('email address'), unique = True)
    is_verified = models.BooleanField(default = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']
    def __str__(self):
        return "{}".format(self.email)
  
class EmailToken(BaseModel):
  email = models.EmailField(_('email address'), unique = True)
  type = models.CharField(max_length = 50, choices = EMAIL_TYPES, default = EmailTypeEnum.signup_email.value)
  token = models.CharField(max_length = 100)
  expiry_date = models.DateField(default = timezone.now)
  
  def __str__(self):
      return "{}".format(self.email)

class Poll(BaseModel):
  title = models.CharField(max_length = 50)
  description = models.TextField()
  contestants = ArrayField(
            models.CharField(max_length=150, blank=True)
        )
  voters = ArrayField(models.CharField(max_length=150, blank=True))
  duration = models.CharField(max_length = 50)
  type = models.CharField(max_length = 50, choices = TYPES, default = TypeEnum.public.value)
  status = models.CharField(max_length = 50, choices = STATUSES, default = StatusEnum.ongoing.value)
  token = models.CharField(max_length = 100, blank=True)
  start_date =  models.DateTimeField(default=timezone.now)
  end_date =  models.DateTimeField(default=timezone.now)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
  
  def __str__(self):
      return "{}".format(self.title)
  
  class Meta:
        ordering = ['-created_at']
  
class Contestant(BaseModel):  
    poll_id = models.ForeignKey(Poll, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return "{}".format(self.name)
    
class PrivateVoter(BaseModel):  
    poll_id = models.ForeignKey(Poll, on_delete = models.CASCADE)
    email = models.EmailField(_('email address'))
    token = models.CharField(max_length = 100, blank=True)
    
    def __str__(self):
        return "{}".format(self.email)
    
class Voter(BaseModel):
    poll_id = models.ForeignKey(Poll, on_delete = models.CASCADE, default = "8a6e5a52-1fb2-4c78-bfad-2d6def278c79")
    email = models.EmailField(_('email address'))
    token = models.CharField(max_length = 100, blank=True)
    voted = models.BooleanField(default = False)
    
    def __str__(self):
        return "{}".format(self.email)
    
class Vote(BaseModel):
    poll_id = models.ForeignKey(Poll, on_delete = models.CASCADE)
    voter_id = models.ForeignKey(Voter, on_delete = models.PROTECT)
    contestant_id = models.ForeignKey(Contestant, on_delete = models.PROTECT)
    rank_value = models.IntegerField()
    
    def __str__(self):
        return "{}".format(self.poll.title)
    
    
class Result(BaseModel):
    poll_id = models.ForeignKey(Poll, on_delete = models.CASCADE)
    rank_raise_bar = models.TextField()
    popular_vote = models.TextField()
    
    def __str__(self):
        return "{}".format(self.poll.title)
    
    