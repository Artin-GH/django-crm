from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddEditRecordForm
from .models import Record


@require_http_methods(["GET", "POST"])
def home(request: HttpRequest):
    records = Record.objects.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in. Logout first!")
            return redirect('home')
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('rememberMe')
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            if not remember_me:
                request.session.set_expiry(0)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('home')
        messages.error(request, 'Username or password is incorrect')
    return render(request, 'home.html', {'records': records})


@require_http_methods(["GET", "POST"])
def logout_user(request: HttpRequest):
    if request.user.is_anonymous:
        messages.error(request, "You are already logged out.")
        return redirect('home')
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home')
    return render(request, 'logout.html')

@require_http_methods(["GET", "POST"])
def register_user(request: HttpRequest):
    if request.user.is_authenticated:
        messages.error(request, 'Logout first.')
        return redirect('home')
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have been successfully signed up and logged in!")
            return redirect('home')
    return render(request, 'register.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def add_record(request: HttpRequest):
    form = AddEditRecordForm()
    if request.method == "POST":
        form = AddEditRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record added successfully.")
            return redirect('home')
        messages.error(request, "The form is not valid.")
    return render(request, 'add_edit_record.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def edit_record(request: HttpRequest, pk):
    try: old_record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        raise Http404

    form = AddEditRecordForm(instance=old_record)
    if request.method == "POST":
        form = AddEditRecordForm(request.POST, instance=old_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect('home')
        messages.error(request, "The form is not valid.")

    return render(request, 'add_edit_record.html', {'form': form, 'is_edit': True})


@login_required
@require_http_methods(["GET"])
def delete_record(request: HttpRequest, pk):
    try: record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        raise Http404
    
    record.delete()
    messages.success(request, 'Record deleted successfully.')
    return redirect('home')
