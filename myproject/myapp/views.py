from django.shortcuts import render, redirect
from myapp.forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login, get_backends

class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 
    authentication_form = EmailAuthenticationForm
    
@login_required
def upload_file(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user  # Attach logged-in user
            document.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('upload_file')
    else:
        form = DocumentForm()

    return render(request, 'upload.html', {'form': form})


# def register_user(request):
#     if request.method == "POST":
#         print("hello")
#         form = CustomUserCreationForm(request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             return redirect('login_user')
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, 'register.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = get_backends()[0]  # use the first backend in AUTHENTICATION_BACKENDS
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email, password)
#         user = authenticate(request, username=email, password=password)
    
#         if user is not None:
#             login(request, user)
#             return redirect('upload_file')
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')