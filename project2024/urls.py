from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoViewSet, PagoViewSet, InscripcionViewSet, 
    EstudianteViewSet, DocenteViewSet, AdministrativoViewSet, 
    AccesoUsuarioView, HistorialPagoViewSet, ReembolsoViewSet,
    NotificacionViewSet, ReporteViewSet
)

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet)  
router.register(r'docentes', DocenteViewSet)
router.register(r'inscripciones', InscripcionViewSet) 
router.register(r'cursos', CursoViewSet)
router.register(r'historial-pagos', PagoViewSet)
router.register(r'administrativos', AdministrativoViewSet)
router.register(r'pagos', HistorialPagoViewSet)  
router.register(r'reembolsos', ReembolsoViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'reportes', ReporteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('acceso/usuario/', AccesoUsuarioView.as_view(), name='acceso-usuario'),
]
