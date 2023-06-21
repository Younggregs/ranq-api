from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailToken, Poll, Contestant

class UserAdmin(BaseUserAdmin):
  list_display = ['email', 'first_name']
  search_fields = ('email', 'first_name')
  ordering = ('email', )
  
admin.site.register(User, UserAdmin)

class EmailTokenAdmin(admin.ModelAdmin):
  list_display = ['email', 'type']
  search_fields = ('email', 'type')
  ordering = ('email',)
  
admin.site.register(EmailToken, EmailTokenAdmin)

class PollAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ('title', 'description')
    ordering = ('title',)
    
admin.site.register(Poll, PollAdmin)


class ContestantAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)
    ordering = ('name',)
    
admin.site.register(Contestant, ContestantAdmin)