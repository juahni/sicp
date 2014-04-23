from django.shortcuts import render

from principal.models import Proyecto
from django.shortcuts import render_to_response

def lista_proyectos(request):
	proyectos = Proyecto.objects.all()
	return render_to_response('lista_proyectos.html',{'lista':proyectos})
