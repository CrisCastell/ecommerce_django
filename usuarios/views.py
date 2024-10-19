from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm

@user_passes_test(lambda u: not u.is_authenticated, login_url='/')
def registro_cliente(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('admin:index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'admin/register.html', {'form': form})
