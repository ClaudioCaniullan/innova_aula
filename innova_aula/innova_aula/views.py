from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User

from .forms import RegisterForm



def index(request):
	return render(request, 'index.html', {})


def perfil(request):
	return render(request, 'perfil.html', {})

def crear_material(request):
	return render(request, 'crear_material.html', {})

def crear_planificacion(request):
	return render(request, 'crear_planificacion.html', {})



def login_user(request):
	# si el usuario esta logeado, evitamos que vaya a login desde el navegador
	if request.user.is_authenticated:
		return redirect('perfil')

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		# si user existe en nuestra base de datos hay login
		user = authenticate(username=username, password=password)
		if user:
			login(request,user)
			# una vez logeado enviamos un mensaje desde el servidor
			messages.success(request, 'Bienvenido {}'.format(user.username))
			return redirect('perfil')
		else:
			messages.error(request, 'Usuario o contraseña no validos')

	return render(request, 'login.html', {})



def register(request):
	# si el usuario esta logeado, evitamos que vaya a registro desde el navegador
	if request.user.is_authenticated:
		return redirect('perfil')

	#generamos un formulario con datos del cliente o vacio
	form = RegisterForm(request.POST or None)
    
    # vamos a validar los datos del formulario para luego obtenerlos
	if request.method == 'POST' and form.is_valid():
        # obtenemos los datos del formulario y lo validamos en RegisterForm
		user = form.save()
		if user:
			# al crear el usuario se logea y redirige
			login(request, user)
			messages.success(request, 'Usuario creado exitosamente')
			return redirect('perfil')

	return render(request, 'register.html', {'form':form}) 



def logout_user(request):
	logout(request)
	messages.success(request, 'Sesión cerrada exitosamente')
	return redirect('index')