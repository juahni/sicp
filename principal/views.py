from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from principal.models import *
from principal.forms import *

def logout_page(request):
    """
    Se que se encarga de cerrar la sesion del usuario.

    @type request: RequestContext
    @param request: Datos incluidos en la peticion

    """

    logout(request)
    return HttpResponseRedirect('/')


# Vistas de administracion de USUARIOS.

@login_required
def admin_usuarios(request):
    """
    Retorna la pagina de administracion de proyectos.

    @type request: RequestContext
    @param request: Datos incluidos en la peticion

    """

    permisos = permisos_sistema(request.user)
    usuarios = User.objects.filter(is_active=True).order_by('username')

    variables = RequestContext(request, {
                # La pagina de administracion es accesible si se posee algun
                # permiso de administracion.
                'administrar':'administrarUsuario' in permisos or
                              'modificarUsuario' in permisos or
                              'crearUsuario' in permisos or
                              'eliminarUsuario' in permisos
                              #or 'asignarRolesDeSistema' in permisos
                              ,
                'modificar': 'modificarUsuario' in permisos,
                'crear': 'crearUsuario' in permisos,
                'eliminar': 'eliminarUsuario' in permisos,
                #'asignarrol': 'asignarRolesDeSistema' in permisos,
                'usuarios': usuarios,
                })

    return render_to_response('administracion/usuarios/admin_usuarios.html',
                              variables)

@login_required
def registrar_usuario(request):
    """
    Registra un nuevo usuario.

    @type request: RequestContext
    @param request: Datos incluidos en la peticion

    """

    permisos = permisos_sistema(request.user)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Crar el usuario.
            usuario = User.objects.create_user(
                       username=form.cleaned_data['username'],
                       password=form.cleaned_data['password1'],
                       email=form.cleaned_data['email'],
                      )

            # Agregar los datos extra.
            usuario.first_name=form.cleaned_data['nombre']
            usuario.last_name=form.cleaned_data['apellido']

            # Guardar el usuario creado.
            usuario.save()

            # Crear el userprofile.
            usuarioprofile = UserProfile(user=usuario,
                              ci=form.cleaned_data['ci'],
                              direccion=form.cleaned_data['direccion'],
                              telefono=form.cleaned_data['telefono']
                             )

            # Guardar el los datos extras del usuario creado.
            usuarioprofile.save()

            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
                'form': form,
                'crear': 'crearUsuario' in permisos,
                })

    return render_to_response('administracion/usuarios/registrar_usuario.html',
                              variables)

@login_required
def modificar_usuario(request, username):
    """
    Modificar los datos de un usuario.

    @type request: RequestContext
    @param request: Datos incluidos en la peticion

    @type username: User
    @param username: Nombre del usuario a modificar

    """

    permisos = permisos_sistema(request.user)

    if request.method == 'POST':
        # Obtener el usuario.
        usuario = User.objects.get(username=username)
        form = ModificarUserForm(request.POST)

        if form.is_valid():
            # Guardar los cambios en el usuario.
            usuario.first_name=form.cleaned_data['nombre']
            usuario.last_name=form.cleaned_data['apellido']
            # Obtener el userprofile. Objeto que almacena los campos
            # agregados al modelo User.
            usuarioprofile = usuario.get_profile()
            # Guardar los cambios en userprofile.
            usuarioprofile.ci=form.cleaned_data['ci']
            usuarioprofile.direccion=form.cleaned_data['direccion']
            usuarioprofile.telefono=form.cleaned_data['telefono']
            # Guardar los cambios en la base de datos.
            usuario.save()
            usuarioprofile.save()

            return HttpResponseRedirect('/administracion/usuarios/')
    else:
        username = request.GET['nombre']
        usuario = get_object_or_404(User, username=username)

        form = ModificarUserForm({
                'nombre': usuario.first_name,
                'apellido': usuario.last_name,
                'ci': usuario.get_profile().ci,
                'direccion': usuario.get_profile().direccion,
                'telefono': usuario.get_profile().telefono,
                'email': usuario.email,
                })

    variables = RequestContext(request, {
                'form': form,
                'usuario': usuario,
                'modificar': 'modificarUsuario' in permisos,
                'asignarrol': 'asignarRolesDeSistema' in permisos,
                })

    return render_to_response('administracion/usuarios/modificar_usuario.html',
                              variables)
