from django.db import models
# Definicion de las etapas de un proyecto.
ETAPA_PROYECTO = (
                  ('E', 'Especificacion de Requerimientos'),
                  ('D', 'Analisis y Disenho'),
                  ('I', 'Implementacion'),
                  ('F', 'Finalizado')
                  )
   
class Proyecto(models.Model):
    """
    Esta clase representa a los proyectos de desarrollo de software
    que seran creados en la aplicacion.
        
    """
    
    nombre = models.CharField(unique=True, max_length=30)
    descripcion = models.TextField()
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    etapa = models.CharField(max_length=1, choices=ETAPA_PROYECTO)
    # Lider de proyecto asignado.
    #lider = models.ForeignKey(User)

    def __unicode__(self):
        return self.nombre

