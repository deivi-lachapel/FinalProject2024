"""
URL configuration for AppDevTFG2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from project2024.views import DocenteCursoView, VerificarEstudiante

# Configura la vista del esquema
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Documentation for the API endpoints of the project.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="wilberthvers05@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Configura las rutas principales del proyecto
urlpatterns = [
    path('', lambda request: HttpResponseRedirect('/api/')),  # Redirige la raíz a la API
    path('admin/', admin.site.urls),
    path('api/', include('project2024.urls')),  # Incluye las URLs de la aplicación
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Documentación Swagger
    path('api/docs.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # Documentación JSON
    path('estudiante/<int:estudiante_id>/verificar/', VerificarEstudiante.as_view(), name='verificar_estudiante'),
    path('docente/<int:docente_id>/cursos/', DocenteCursoView.as_view(), name='docente_cursos'),
]
