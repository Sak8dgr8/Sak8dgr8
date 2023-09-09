from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from django.contrib.auth.forms import UserCreationForm
from .forms import ChannelCustomizationForm
from .forms import ProjectForm
from .models import Project
from .models import Profile
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from .models import Donation
from django.db.models import Max
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import UpdateForm
from .models import Update
from .forms import UpdateCommentForm
from .models import UpdateComment
from django.core.files.base import ContentFile
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm        
from django.http import HttpResponse       

class EditProjectView(UpdateView):
     
     model = Project
     form_class = ProjectForm
     template_name = 'projects/edit_project.html'
     def get_success_url(self):
         username = self.request.user.username
         return reverse_lazy('user_channel', kwargs={'username': username})
     def form_valid(self, form):
        # Get the project instance being updated
        project = form.instance

        # Set the status to 'draft'
        project.status = 'draft'

        # Save the project instance
        project.save()

        return super().form_valid(form)


def go_live(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)

    # Check if all required fields are filled
    if not project.project_title or not project.project_description or not project.project_thumbnail or not project.project_video or not project.funding_goal:
        messages.error(request, 'Please fill in all required project details before going live.')
        return redirect('user_channel', username=request.user.username)

    # Update the project status to "Live"
    project.status = 'live'
    project.save()

    # Add success message
    messages.success(request, f'Project: "{project.project_title}" is now live!')

    return redirect('user_channel', username=request.user.username)

from django.db.models import F, Sum

class FundingNowView(ListView):
    model = Project
    template_name = 'projects/funding_now.html'
    context_object_name = 'live_projects'
    queryset = Project.objects.filter(status='live')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate progress percentage for each project
        for project in context['live_projects']:
            total_donations = project.donations.filter(status='completed').aggregate(total=Sum('donation_amount')).get('total', 0) or 0
            progress_percentage = (total_donations / project.funding_goal) * 100
            project.progress_percentage = round(progress_percentage, 2)
        
        return context

   
class ProjectSearchView(ListView):

     template_name = 'projects/funding_now.html'
     context_object_name = 'live_projects'

     def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            projects = Project.objects.filter(
                Q(project_title__icontains=query, status='live') |
                Q(user__username__icontains=query, status='live') |
                Q(project_description__icontains=query, status='live' )
            )
            return projects
        else:
            return Project.objects.filter(status='live'), User.objects.none()

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = context['live_projects']

        # Calculate the percentage achieved for each project
        for project in projects:
            total_donations = project.donations.filter(status='completed').aggregate(total=Sum('donation_amount')).get('total', 0) or 0
            if project.funding_goal > 0:
                progress_percentage = (total_donations / project.funding_goal) * 100
                project.progress_percentage = round(progress_percentage, 2)
            else:
                project.progress_percentage = 0
        context['search_query'] = self.request.GET.get('q')
        return context

from django.core.mail import send_mail
from django.core.mail import EmailMessage

def send_update_emails(update, project):
    subject = f"{project.user} posted a new update in {project.project_title}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [donation.donor_email for donation in project.donations.filter(status='completed')] + [subscriber.email for subscriber in project.user.profile.subscribers.all()]

    context = {
        'project':project,
        'update': update,
     }
    email_body = render_to_string('projects/update_notification_email.html', context)
    email = EmailMessage(subject, email_body, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()
               
 

    

     
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, status='live')

    if request.user.is_authenticated and request.user == project.user:
        if request.method == 'POST':
            form = UpdateForm(request.POST, request.FILES)
            if form.is_valid():
                update = form.save(commit=False)
                update.project = project
                update.save()
                send_update_emails(update, project)
                # Redirect to the project detail page after successfully creating the update
                return redirect('user_channel', username=request.user.username)
        else:
            form = UpdateForm()

        return render(request, 'projects/project_update.html', {'project': project, 'form': form})
    else:
        return redirect('home')
                


def funding_info(request):
    if request.user.is_authenticated:
        active_project = Project.objects.filter(user=request.user, status__in=['live', 'draft']).first()
        if active_project:
            username = request.user.username
            messages.error(request, "You can only start one project at a time. Complete your current project before starting a new one!")
            return redirect(reverse('user_channel', kwargs={'username': username}))

        try:
            project = Project.objects.get(user=request.user, status='none')
        except Project.DoesNotExist:
            project = None

        if request.method == 'POST':
            form = ProjectForm(request.POST, files=request.FILES, instance=project)
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user
                project.status = 'draft'


                project.save()
                return redirect('user_channel', username=request.user.username)
        else:
            form = ProjectForm(instance=project)

        return render(request, 'projects/fundinginfo.html', {'form': form})
    else:
        return redirect('login_user')

from django.db.models import Sum

def user_channel(request, username, error_message=None):

    user = get_object_or_404(User, username=username)
    completed_projects = Project.objects.filter(user=user, status='completed')

    completed_projects_count = completed_projects.count()
    data2 = Profile.objects.get(user=user)
    subscribers = data2.subscribers.all()
    number_of_subscribers = len(subscribers)
    is_subscribed = False
    for subscriber in subscribers:
        if subscriber == request.user:
            is_subscribed = True
            break
    is_subscribed = request.user in subscribers

    context={
        'completed_projects_count':completed_projects_count,
        'completed_projects':completed_projects,
        'data2':data2,
        'number_of_subscribers': number_of_subscribers,
        'is_subscribed': is_subscribed,
    }
   
    # Get the active project for the user (assuming there's only one active project)
    try:
        project = Project.objects.get(user=user, status__in=['draft', 'live', 'funds_withdrawn'])
    except Project.DoesNotExist:
        project = None

    context.update({
        'user': user,
        'project': project,
        'error_message': error_message,
    })

    if project:
        
        comment_form = CommentForm()

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.project = project
                comment.user = request.user
                comment.save()
                # Redirect or perform any other desired action after saving the comment
                return redirect('user_channel', username=username)

        comment_count = project.comments.annotate(total_comments=Count('id')).count()
        
        comments = project.comments.order_by('created_at')

        project.views += 1
        project.save()



        for comment in comments:
            # Calculate the elapsed time since the comment was created
            elapsed_time = humanize.naturaltime(timezone.now() - comment.created_at)
            comment.elapsed_time = elapsed_time

        profile_id = request.user.profile.id if request.user.is_authenticated else None
        total_donations = project.total_donations or 0
        funding_goal = project.funding_goal or 1
        percentage = (total_donations / funding_goal) * 100

        channel_owner = User.objects.get(username=username)
        all_donations = Donation.objects.filter(project=project, status='completed').order_by('-donation_amount')
        highest_donation = Donation.objects.filter(project=project, status='completed').order_by('-donation_amount').first()
        most_recent_donation = Donation.objects.filter(project=project, status='completed').order_by('-donation_date').first()
        channel_owner_donation = Donation.objects.filter(project=project, donor=channel_owner, status='completed').first()
        completed_donation_count = project.donations.filter(status='completed').count()
        updates = Update.objects.filter(project=project)

        context.update({
            'data2': data2,
            'comment_form': comment_form,
            'comment_count': comment_count,
            'comments': comments,
            'profile_id': profile_id,

            'percentage': percentage,
            'channel_owner': channel_owner,
            'highest_donation': highest_donation,
            'most_recent_donation': most_recent_donation,
            'channel_owner_donation': channel_owner_donation,
            'updates': updates,
            'completed_projects_count':completed_projects_count,
            'completed_donation_count': completed_donation_count,
            'all_donations': all_donations,
            'logo_image_url': "{% static 'Our-TubeLogo.svg' %}",
        })

        if not request.user.is_authenticated:
            return render(request, 'Channel/userchannel.html', context)

    return render(request, 'Channel/userchannel.html', context)



def update_detail(request, project_id, update_id):
    project = get_object_or_404(Project, id=project_id)
    all_donations = Donation.objects.filter(project=project, status='completed').order_by('-donation_amount')
    update = get_object_or_404(Update, id=update_id, project=project)
    update.views += 1
    update.save()
    update_number = project.updates.order_by('updated_at').filter(updated_at__lte=update.updated_at).count()
    data2 = Profile.objects.get(user__username=project.user)
    subscribers = data2.subscribers.all()
    number_of_subscribers = len(subscribers)
    is_subscribed = False
    for subscriber in subscribers:
            if subscriber == request.user:
                is_subscribed = True
                break
    total_donations = project.total_donations or 0
    funding_goal = project.funding_goal or 1
    percentage = (total_donations / funding_goal) * 100

    comment_form = UpdateCommentForm()
    comment_count = update.updatecomments.annotate(total_comments=Count('id')).count()
    comments = update.updatecomments.order_by('created_at')


    channel_owner = User.objects.get(username=project.user)
    highest_donation = Donation.objects.filter(project__user=channel_owner, status='completed').order_by('-donation_amount').first()
    most_recent_donation = Donation.objects.filter(project__user=channel_owner, status='completed').order_by('-donation_date').first()
    channel_owner_donation = Donation.objects.filter(project__user=channel_owner, donor=channel_owner, status='completed').first()
    completed_donation_count = project.donations.filter(status='completed').count()
    context = {
        'project': project,
        'update': update,
        'update_number': update_number,
        'number_of_subscribers': number_of_subscribers,
        'is_subscribed': is_subscribed,
        'percentage' : percentage,
        'channel_owner': channel_owner,
        'highest_donation': highest_donation,
        'most_recent_donation': most_recent_donation,
        'channel_owner_donation': channel_owner_donation,
        'comment_count': comment_count,
        'comments' : comments,       
        'comment_form':comment_form, 
        'completed_donation_count':completed_donation_count,
        'all_donations': all_donations,
    }

    if request.method == 'POST':
            comment_form = UpdateCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.update = update
                comment.user = request.user
                comment.save()
                # Redirect or perform any other desired action after saving the comment
                return redirect('update-detail', project_id=project.pk, update_id=update.pk)
            


    return render(request, 'projects/update_detail.html', context)

def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    user = request.user
    if request.method == 'POST':
        # Update the project status to "completed"
        project.status = 'completed'
        project.save()
        
        return redirect(reverse('completed_projects', kwargs={'username': request.user.username}))  # Redirect to the completed projects template

    return render(request, 'Channel/complete_project.html', {'project': project, 'user':user})


def completed_projects(request, username):
    # Get the user with the given username
    user = get_object_or_404(User, username=username)

    # Get the completed projects of the user
    completed_projects = Project.objects.filter(user=user, status='completed')

    data2 = Profile.objects.get(user__username=username)

    subscribers = data2.subscribers.all()
    number_of_subscribers = len(subscribers)
    is_subscribed = request.user in subscribers
    completed_projects_count = Project.objects.filter(user=user, status='completed').count()
    for project in completed_projects:
        total_donations = project.donations.filter(status='completed').aggregate(total=Sum('donation_amount')).get('total', 0) or 0
        progress_percentage = (total_donations / project.funding_goal) * 100
        project.progress_percentage = round(progress_percentage, 2)


    context = {
        'user': user,  # Add the user to the context
        'completed_projects': completed_projects,
        'number_of_subscribers': number_of_subscribers,
        'is_subscribed': is_subscribed,
        'completed_projects_count':completed_projects_count,
    }

    return render(request, 'Channel/complete_project.html', context)




class AddSubscriber(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profile.subscribers.add(request.user)

        # Get the 'next' parameter from the request
        next_url = request.GET.get('next', None)
        if next_url:
            return redirect(next_url)

        return redirect('user_channel', username=username)

class RemoveSubscriber(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profile.subscribers.remove(request.user)

        # Get the 'next' parameter from the request
        next_url = request.GET.get('next', None)
        if next_url:
            return redirect(next_url)

        return redirect('user_channel', username=username)


def no_project(request):
     return render(request, 'Channel/no_projects.html')

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import io
import base64


# views.py
import uuid 
import shortuuid
import base64
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile

@login_required
def channel_customization(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        form = ChannelCustomizationForm(instance=profile)

        if request.method == 'POST':
            if 'submit_profile_pic' in request.POST:
                profile_pic = request.FILES.get('profile_pic')
                cropped_image_data = request.POST.get('cropped_image_data')

                if profile_pic and cropped_image_data:
                    # Convert the base64 encoded data to an image file
                    img_data = cropped_image_data.split(',')[1]
                    img_bytes = base64.b64decode(img_data)
                    unique_filename = f'{uuid.uuid4()}.png'
                    img_file = ContentFile(img_bytes, name=unique_filename)

                    # Save the profile picture and cropped image data
                    profile.profile_pic = profile_pic
                    profile.cropped_image_data = img_file
                    profile.save()

                    return redirect('channel_customization')

            elif 'submit_bio' in request.POST:
                bio = request.POST.get('bio')
                if bio:
                    profile.bio = bio
                    profile.save()
                # Handle bio submission
                return redirect('channel_customization')

        return render(request, 'Channel/channel_customization.html', {
            'form': form,
        })

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserUpdateForm

@login_required
def basic_info(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully changed your basic information!')
            return redirect('user_channel', username=request.user.username)  # Redirect to the user's profile page

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'Channel/basic_info.html', {'form': form})



from .forms import DonationForm
from django.utils import timezone




from .forms import ExtPayPalPaymentsForm
from decimal import Decimal  # Import Decimal to handle currency amounts accurately

def donation_landing_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = DonationForm(request.POST or None)
    paypal_dict = {
        'amount': 200,
        'item_name': "Loda",
        'invoice': '69',
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment_completed')),
        'cancel_url': request.build_absolute_uri(reverse('payment_failed')),
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    if request.method == 'POST' and form.is_valid():
        # Save the donation instance before accessing the donation_id
        if request.user.is_authenticated:
            donation = form.save(commit=False)
            donation.project = project
            donation.donor = request.user
            donation.donation_date = timezone.now()
            donation.donor_email = request.user.email
            donation.status = 'pending'
            donation.save()
        else:
            donor_first_name = form.cleaned_data['first_name']
            donor_last_name = form.cleaned_data['last_name']

            donation = form.save(commit=False)
            donation.project = project
            if not donor_first_name and not donor_last_name:
                donation.name = 'Anonymous'
            else:
                donation.name = f"{donor_first_name} {donor_last_name}"
            donation.donor = None
            donation.donation_date = timezone.now()
            donation.status = 'pending'
            donation.save()

        # Update the invoice value with the donation_id
        donation_id = donation.donation_id


        # Update the amount field with the sum of 'donation_amount' and 'platform_donation' from the form
        donation_amount = form.cleaned_data.get('donation_amount', 0)
        total_amount = donation_amount
 

        paypal_updated_dict = {

        'amount': total_amount,

        'item_name': "Loda",
        'invoice': str(donation_id),
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment_completed')),
        'cancel_url': request.build_absolute_uri(reverse('payment_failed')),
         }
        # Create a new context dictionary with the updated PayPal button
        updated_context = {
            'project': project,
            'form': form,
            'paypal_payment_button_updated': ExtPayPalPaymentsForm(initial=paypal_updated_dict),
            'total_amount': total_amount,
            'donation_id': donation_id,
        }

        # Return the updated context in the render function
        return render(request, 'donation/donation_landing_page.html', updated_context)

    # If the form is not submitted, use the existing context with the initial PayPal button
    context = {
        'project': project,
        'form': form,
        'paypal_payment_button': paypal_payment_button,
    }
    return render(request, 'donation/donation_landing_page.html', context)

import json
from django.http import JsonResponse
def paymentcomplete(request):
    body = json.loads(request.body)   
    print('BODY:', body)
    donation = Donation.objects.get(donation_id=body['donationId'])
    donation.status = 'completed'
    donation.save()

@login_required
def donation_history(request):
    user = request.user
    donations = Donation.objects.filter(donor=user, status='completed')
    unseen_updates = Update.objects.filter(project__in=[donation.project for donation in donations], seen_by_users__in=[user])
    context = {
            'donations': donations,
            'percentage_achieved': None,
            'unseen_updates': unseen_updates,
        }

    for donation in donations:
        project = donation.project
        total_donations = project.donations.filter(status='completed').aggregate(total=Sum('donation_amount')).get('total', 0) or 0
        funding_goal = project.funding_goal
        if funding_goal > 0:
            percentage_achieved = round((total_donations / funding_goal) * 100, 2)
        else:
            percentage_achieved = 0
        donation.percentage_achieved = percentage_achieved
        context['percentage_achieved'] = percentage_achieved

       
    return render(request, 'donation/history.html', context)


def mark_update_as_seen(request, update_id):
    update = Update.objects.get(pk=update_id)
    update.seen_by_users.add(request.user)
    return redirect('update_detail')



from django.template.loader import render_to_string    
from django.core.mail import EmailMessage



@login_required
def payment_info(request):
    user_email = request.user.email
    username = request.user.username
    email_subject = 'Verify your email address'
    project = Project.objects.filter(user=request.user).first()

    context = {
        'username': username,
        'project': project,
    }

    if request.method == 'POST':
        

            # Send the email with the verification link
            email_body = render_to_string('projects/verification.html', context)
            email = EmailMessage(email_subject, email_body, to=[user_email])
            email.content_subtype = 'html'
            email.send()
            project.verification_status = 'email_sent'
            project.save()


    return render(request, 'projects/payments.html', context)

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def verify_button(request):
    project = Project.objects.filter(user=request.user).first()
    username = request.user.username
    context = {
        'username': username,
        'project': project,
    }
    
    if request.method == 'POST':
        project.verification_status = 'verified'
        project.save()
        return HttpResponseRedirect(reverse('payment_info'), context)
    return HttpResponse("Invalid request or project not found.")




def completed_channel(request, username, project_id, error_message=None):

    user = get_object_or_404(User, username=username)
    completed_projects = Project.objects.filter(user=user, status='completed')

    completed_projects_count = completed_projects.count()

    context={
        'completed_projects_count':completed_projects_count,
    }
   
    # Get the completed project for the user (assuming there's only one active project)
    project = Project.objects.get(user=user, status__in=['completed'], pk=project_id)
    

    context.update({
        'user': user,
        'project': project,
        'error_message': error_message,
        'project':project,
    })

    if project:
        data2 = Profile.objects.get(user=user)
        comment_form = CommentForm()

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.project = project
                comment.user = request.user
                comment.save()
                # Redirect or perform any other desired action after saving the comment
                return redirect('user_channel', username=username)

        comment_count = project.comments.annotate(total_comments=Count('id')).count()
        
        comments = project.comments.order_by('created_at')


        project.views += 1
        project.save()
        
        subscribers = data2.subscribers.all()
        number_of_subscribers = len(subscribers)
        
        
        
        is_subscribed = request.user in subscribers

        for comment in comments:
            # Calculate the elapsed time since the comment was created
            elapsed_time = humanize.naturaltime(timezone.now() - comment.created_at)
            comment.elapsed_time = elapsed_time

        profile_id = request.user.profile.id if request.user.is_authenticated else None
        total_donations = project.total_donations or 0
        funding_goal = project.funding_goal or 1
        percentage = (total_donations / funding_goal) * 100

        channel_owner = User.objects.get(username=username)

        highest_donation = Donation.objects.filter(project=project, status='completed').order_by('-donation_amount').first()
        most_recent_donation = Donation.objects.filter(project=project, status='completed').order_by('-donation_date').first()
        channel_owner_donation = Donation.objects.filter(project=project, donor=channel_owner, status='completed').first()
        completed_donation_count = project.donations.filter(status='completed').count()
        updates = Update.objects.filter(project=project)

        context.update({
            'data2': data2,
            'comment_form': comment_form,
            'comment_count': comment_count,
            'comments': comments,
            'profile_id': profile_id,
            'number_of_subscribers': number_of_subscribers,
            'is_subscribed': is_subscribed,
            'percentage': percentage,
            'channel_owner': channel_owner,
            'highest_donation': highest_donation,
            'most_recent_donation': most_recent_donation,
            'channel_owner_donation': channel_owner_donation,
            'updates': updates,
            'completed_projects_count':completed_projects_count,
            'completed_donation_count':completed_donation_count,
        
        })

        if not request.user.is_authenticated:
            return render(request, 'Channel/completedchannel.html', context)

    return render(request, 'Channel/completedchannel.html', context)







from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_channel', username=request.user.username)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_user')
   
            

    return render(request, template_name="authenticate/login.html")

    
def logout_user(request):
    logout(request)

    return redirect ('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            # If the form is not valid, add a message to display the errors in the template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return render(request, 'authenticate/register_user.html', {'form': form})
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {'form': form})
    
def payment_completed_view(request):
    if request.user.is_authenticated:
        return redirect('donation_history')
    else:
        return redirect('home')

def payment_failed_view(request):
    return redirect('home')

def privacy_policy(request):
    return render(request, 'footer/privacy_policy.html')
