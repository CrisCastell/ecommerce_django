from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test



@user_passes_test(lambda u: not u.is_authenticated, login_url='/')
def registro_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()

            # Si el usuario no es superusuario, agregarlo al grupo "clientes"
            if not user.is_superuser:
                client_group = Group.objects.get(name='clientes')
                user.groups.add(client_group)

            messages.success(request, f'Usuario {user.username} registrado exitosamente.')
            return redirect('admin:index')
    else:
        form = UserCreationForm()

    return render(request, 'admin/register.html', {'form': form})


# def registro_cliente(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.is_staff = True
#             user.save()

#             client_group = Group.objects.get(name='clientes')
#             user.groups.add(client_group)

#             messages.success(request, f'Usuario {user.username} registrado exitosamente como cliente.')
#             return redirect('admin:index')  
#     else:
#         form = UserCreationForm()
#         print(form)

#     return render(request, 'admin/register.html', {'form': form})