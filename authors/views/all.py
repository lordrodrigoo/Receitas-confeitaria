


from django.http import HttpResponse

def show_menu(request):
	return HttpResponse('<h1>Menu visualizado!</h1>')

def show_login(request):
	return HttpResponse('<h1>Página de Login</h1>')

def show_register(request):
	return HttpResponse('<h1>Página de Registro</h1>')

def show_dashboard(request):
	return HttpResponse('<h1>Painel de Controle</h1>')

def show_new_recipe(request):
	return HttpResponse('<h1>Nova Receita</h1>')

def show_logout(request):
	return HttpResponse('<h1>Logout</h1>')
