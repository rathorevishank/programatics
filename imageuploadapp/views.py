from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Max
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']  # Assuming you are using email as the username
        password = request.POST['userPassword']
        user_obj = User.objects.filter(email=email)
        print(f"User Object: {user_obj}")

        if not user_obj.exists():
            messages.warning(request, 'Account Not Exists')
            return HttpResponseRedirect(request.path_info)
        user = authenticate(username=email, password=password)
        print(f"User: {user}, Password: {password}")


        if user is not None:
         login(request, user)
         messages.success(request, 'Login successful.')
         return redirect('/gallery')
        else:
         messages.error(request, f'Invalid credentials. Email: {email}, Password: {password}')


    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['userName']
        email = request.POST['email']
        password1 = request.POST['userPassword']
        password2 = request.POST['confirmpass']

        if password1 == password2:
            # Check if the username is unique
            if not User.objects.filter(username=username).exists():
                # Check if the email is unique
                if not User.objects.filter(email=email).exists():
                    # Create the user
                    user = User.objects.create_user(username=email, email=email, password=password1)  #saved username as email
                    login(request, user)
                    messages.success(request, 'Registration successful. Welcome!')
                    return redirect('/login')  # Change 'gallery_dashboard' to your actual gallery view name
                else:
                    messages.error(request, 'Email is already taken.')
            else:
                messages.error(request, 'Username is already taken.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')

@login_required
def gallery(request):
    # Fetch all uploaded images for the current user
    images = UploadImage.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'gallery.html', {'images': images})

@login_required
def upload_image(request):
    if request.method == 'POST':
        image_type = request.POST.get('image_type')
        image_file = request.FILES.get('image_file')

        # Validate file type
        allowed_types = ['jpg', 'jpeg', 'png', 'gif']
        if not image_file.name.lower().endswith(tuple(allowed_types)):
            return render(request, 'upload_image.html', {'error': 'Invalid file type. Allowed types: JPG, JPEG, PNG, GIF'})

        # Save the uploaded image
        UploadImage.objects.create(user=request.user, image_type=image_type, image_file=image_file)

        return redirect('/gallery')

    return render(request, 'uploadimage.html')