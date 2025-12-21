from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import DonationProject, RecipientRequest, Donation, UserProfile


def approved_case_list(request):
    projects = DonationProject.objects.filter(status=DonationProject.STATUS_ACTIVE)
    completed_projects = DonationProject.objects.filter(status=DonationProject.STATUS_COMPLETED)[:6]
    return render(request, 'home.html', {
        'projects': projects,
        'completed_projects': completed_projects
    })


def projects_list(request):
    projects = DonationProject.objects.filter(status=DonationProject.STATUS_ACTIVE)
    return render(request, 'projects.html', {'projects': projects})


def case_detail(request, project_id):
    project = get_object_or_404(DonationProject, id=project_id)
    return render(request, 'project_detail.html', {
        'project': project,
    })


@require_http_methods(["GET", "POST"])
@transaction.atomic
def donate_to_case(request, project_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to make a donation.')
        return redirect('login')
    
    project = get_object_or_404(DonationProject, id=project_id)
    
    if request.method == 'POST':
        if project.status != DonationProject.STATUS_ACTIVE:
            messages.error(request, 'Project is not active')
            return redirect('project_detail', project_id=project_id)
        
        try:
            amount = float(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid amount')
            return render(request, 'donate.html', {'project': project})
        
        if amount <= 0:
            messages.error(request, 'Amount must be greater than zero')
            return render(request, 'donate.html', {'project': project})
        
        donation = Donation.objects.create(
            donor=request.user,
            project=project,
            amount=amount,
        )
        
        messages.success(request, f'Thank you for your donation of ${amount:.2f}!')
        return redirect('project_detail', project_id=project_id)
    
    return render(request, 'donate.html', {'project': project})


def completed_projects(request):
    projects = DonationProject.objects.filter(status=DonationProject.STATUS_COMPLETED)
    return render(request, 'completed_projects.html', {'projects': projects})


def completed_project_detail(request, project_id):
    project = get_object_or_404(DonationProject, id=project_id, status=DonationProject.STATUS_COMPLETED)
    return render(request, 'completed_project_detail.html', {
        'project': project,
    })


@login_required
@require_http_methods(["GET", "POST"])
def recipient_request_view(request):
    try:
        if request.user.profile.role != UserProfile.ROLE_RECIPIENT:
            return HttpResponseForbidden("Access denied. Only recipients can submit requests.")
    except:
        return HttpResponseForbidden("Access denied. Only recipients can submit requests.")
    
    if request.method == 'POST':
        try:
            treatment_cost = float(request.POST.get('treatment_cost', 0))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid treatment cost')
            return render(request, 'recipient_request.html')
        
        if treatment_cost <= 0:
            messages.error(request, 'Treatment cost must be greater than zero')
            return render(request, 'recipient_request.html')
        
        try:
            age = int(request.POST.get('age', 0))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid age')
            return render(request, 'recipient_request.html')
        
        RecipientRequest.objects.create(
            recipient=request.user,
            full_name=request.POST.get('full_name'),
            age=age,
            medical_condition=request.POST.get('medical_condition'),
            hospital_name=request.POST.get('hospital_name'),
            treatment_cost=treatment_cost,
            financial_condition=request.POST.get('financial_condition'),
            medical_document=request.FILES.get('medical_document'),
        )
        
        messages.success(request, 'Your request has been submitted and is pending approval.')
        return redirect('recipient_request')
    
    return render(request, 'recipient_request.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                role = user.profile.role
                if role == 'ADMIN':
                    return redirect('admin:index')
                elif role == 'RECIPIENT':
                    return redirect('recipient_request')
                else:
                    return redirect('home')
            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return render(request, 'register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, password=password)
        
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to SmartSadaqah.')
        return redirect('home')
    
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def contact(request):
    return render(request, 'contact.html')
