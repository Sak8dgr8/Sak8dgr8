from django.contrib import admin
from .models import Profile
from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Project, Donation
from django.contrib.auth.models import User
from .models import Comment, Update, Withdrawl

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Project



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class ProjectInline(admin.StackedInline):
    model = Project
    can_delete = False
    verbose_name_plural = 'Project'





class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, ProjectInline)




admin.site.register(Update)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Withdrawl)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('project', 'donor', 'name', 'donation_amount', 'donation_date', 'status', 'donor_email', 'platform_donation', 'donation_id')
