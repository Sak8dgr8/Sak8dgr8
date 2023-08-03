from django.db import models
from django.contrib.auth.models import User
from .validators import file_size
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .constants import STATES_CHOICES
from .constants import DAYS_CHOICES
# Create your models here.




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    profile_pic = models.ImageField(null=True, blank=True)
    cropped_image_data = models.ImageField(null=True, blank=True)
    bio = models.CharField(null=True, blank=True, max_length=500)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribers',)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Project.objects.create(user=instance)

class Project(models.Model):
    STATUS_CHOICES = (
        ('nonee', 'None'),
        ('draft', 'Draft'),
        ('live', 'Live'),
        ('funds_withdrawn', 'Funds Withdrawn'),
        ('completed', 'Completed'),
    )
    VERIFICATION_STATUS = (
        ('not_verified', 'Not Verified'),
        ('email_sent', 'Email Sent'),
        ('verified', 'Verified'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="project")
    state = models.CharField(null=True,max_length=3, choices=STATES_CHOICES)
    city = models.CharField(null=True, max_length=100)
    project_title = models.CharField(null=True, max_length=400)
    funding_goal = models.IntegerField(null=True)
    target_date = models.CharField(null=True, choices=DAYS_CHOICES, max_length=3)
    project_description = models.TextField(null=True)
    project_thumbnail = models.ImageField(null=True, blank=True)
    project_video = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp4','avi','mov'])], null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nonee')
    verification_status = models.CharField(max_length=30, choices=VERIFICATION_STATUS, default='not_verified')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    
    @property
    def total_donations(self):
        return self.donations.filter(status='completed').aggregate(total=Sum('donation_amount')).get('total', 0) or 0

    


    @total_donations.setter
    def total_donations(self, value):
        # Optional: Implement custom logic if needed
        pass

class Update(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    update_title = models.CharField(max_length=100)
    update_description = models.TextField()
    update_video = models.FileField(upload_to="video/%y", validators=[FileExtensionValidator(allowed_extensions=['mp4','avi','mov'])], null=True, blank=True)
    update_thumbnail = models.ImageField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.update_title} - {self.project}"


class Comment(models.Model):
      project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
      user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='throatgoat')
      body = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return '%s - %s' % (self.project.project_title, self.user)
            
class UpdateComment(models.Model):
      update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='updatecomments')
      user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='updatethroatgoat')
      body = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return '%s - %s' % (self.update.update_title, self.user)


from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
import uuid


class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    donation_amount = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(50000)])
    donation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ), default='Pending')
    donor_email = models.EmailField(blank=True, null=True)
    platform_donation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50000)], null=True, blank=True)
    donation_id = models.UUIDField(default=uuid.uuid4, editable=False, null=True)


    def __str__(self):
        return f"Donation #{self.id} - Project: {self.project.project_title} - Donor: {self.get_donor_name()}"

    def get_donor_name(self):
        if self.donor:
            return self.donor.username
        return f"{self.first_name} {self.last_name}"