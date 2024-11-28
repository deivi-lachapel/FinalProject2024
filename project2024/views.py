from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail  # Si quieres notificaciones por correo
from .models import *
from .serializers import *


# Create your views here.

# ViewSet para gestionar las vistas, utilizando las operaciones CRUD

class DocenteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los docentes. Permite realizar operaciones CRUD (crear, leer, actualizar y eliminar)
    sobre los registros de docentes en el sistema.
    """
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class EstudianteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los estudiantes. Proporciona las operaciones CRUD para los registros
    de estudiantes, que incluyen su creación, visualización, actualización y eliminación.
    """
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class AdministrativoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el personal administrativo. Permite el manejo completo de los registros 
    administrativos a través de operaciones CRUD.
    """
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class InscripcionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las inscripciones. Este endpoint permite crear nuevas inscripciones,
    ver detalles de inscripciones existentes, así como actualizarlas o eliminarlas.
    """
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

    # Agregar opciones de filtrado y búsqueda
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['fecha_inscripcion', 'estado']  # Permite ordenar por estos campos
    search_fields = ['estado', 'curso__nombre', 'estudiante__nombre']  # Permite buscar por estado, nombre del curso o nombre del estudiante

    def perform_create(self, serializer):
        # Personalización para agregar lógica durante la creación de una inscripción, si es necesario
        serializer.save()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los cursos. Proporciona las operaciones CRUD necesarias para manejar
    los cursos ofrecidos en el sistema, lo cual incluye crear, ver, actualizar y eliminar cursos.
    """
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class PagoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los pagos. Permite realizar operaciones CRUD sobre los registros
    de pagos y tiene acciones adicionales para obtener pagos por inscripción y cambiar el estado del pago.
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo registro de pago en el sistema. Se puede añadir lógica adicional antes
        de guardar el pago en la base de datos.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Actualiza un registro de pago existente. Se puede implementar lógica adicional
        antes de actualizar el pago en la base de datos.
        """
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Recupera y devuelve los detalles de un pago específico por su ID.
        """
        return super().retrieve(request, *args, **kwargs)
    
    # Método para obtener pagos por inscripción
    @action(detail=False, methods=['get'])
    def by_inscripcion(self, request, inscripcion_id=None):
        """
        Endpoint personalizado para obtener los pagos relacionados con una inscripción específica.
        Requiere el ID de la inscripción en el parámetro `inscripcion_id`.
        """
        pagos = self.queryset.filter(inscripcion_id=inscripcion_id)
        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)

    # Método para cambiar el estado del pago
    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        """
        Endpoint para cambiar el estado de un pago. Recibe el nuevo estado en el campo `estado_pago`
        del cuerpo de la solicitud. Actualiza el estado del pago y devuelve un mensaje de confirmación.
        """
        pago = self.get_object()
        nuevo_estado = request.data.get('estado_pago')
        if nuevo_estado:
            pago.estado_pago = nuevo_estado
            pago.save()
            return Response({'status': 'estado de pago actualizado'})
        return Response({'error': 'estado no proporcionado'}, status=400)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class HistorialPagoViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar el historial de pagos.
    Permite obtener todos los registros y crear nuevos registros de historial de pagos.
    """
    queryset = HistorialPago.objects.all()  # Definir el queryset para el ModelViewSet
    serializer_class = HistorialPagoSerializer  # Usar el serializador adecuado



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class ReembolsoViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar las solicitudes de reembolso.
    Permite obtener, crear y actualizar solicitudes de reembolso.
    """
    queryset = Reembolso.objects.all()  # Obtener todas las solicitudes de reembolso
    serializer_class = ReembolsoSerializer  # Usar el serializador adecuado

    def perform_create(self, serializer):
        # Aquí podrías agregar lógica adicional, como notificar al usuario
        serializer.save()

    def update(self, request, *args, **kwargs):
        # Aquí se manejan las actualizaciones del reembolso (por ejemplo, cambiar el estado)
        return super().update(request, *args, **kwargs)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar las notificaciones.
    Permite obtener todas las notificaciones, crear nuevas y actualizar su estado.
    """
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

    def perform_create(self, serializer):
        # Puedes agregar lógica para el envío de notificaciones aquí, si es necesario
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        # Actualización de estado u otros datos
        return super().update(request, *args, **kwargs)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Vista para listar y crear administrativos
class AdministrativoListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear registros de personal administrativo.
    Proporciona la funcionalidad de listar todos los registros administrativos existentes,
    así como de crear nuevos registros en el sistema.
    """
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo registro administrativo. Valida los datos y, si son válidos,
        guarda el registro en la base de datos y devuelve los datos del registro creado.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Vista para obtener, actualizar y eliminar un administrativo por su ID
class AdministrativoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar o eliminar un registro administrativo por su ID.
    Permite realizar operaciones de recuperación, actualización y eliminación de un registro específico.
    """
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer

    def get(self, request, *args, **kwargs):
        """
        Recupera los detalles de un registro administrativo específico basado en su ID.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Actualiza un registro administrativo específico por su ID. Valida y guarda los
        cambios en la base de datos si los datos son válidos.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Elimina un registro administrativo específico por su ID. Borra el registro de la base
        de datos y devuelve una respuesta de confirmación.
        """
        return self.destroy(request, *args, **kwargs)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class AccesoUsuarioView(APIView):
    """
    Verifica el acceso de un usuario (Administrativo, Estudiante, Docente) basado en el código único (codigo_doc, codigo_adm, matricula) y password.
    Retorna el nivel de acceso si el identificador y contraseña están registrados en el sistema.
    """
    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        codigo_doc = request.data.get('codigo_doc')
        codigo_adm = request.data.get('codigo_adm')
        matricula = request.data.get('matricula')

        if not password:
            return Response(
                {"error": "Password es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Intentar obtener al usuario en cada uno de los modelos
        usuario = None
        modelo_usuario = None

        # Buscar en el modelo Administrativo (solo por codigo_adm)
        if codigo_adm:
            try:
                usuario = Administrativo.objects.get(
                    password=password,
                    codigo_adm=codigo_adm
                )
                modelo_usuario = 'administrativo'
            except Administrativo.DoesNotExist:
                pass

        # Buscar en el modelo Estudiante (solo por matricula)
        if not usuario and matricula:
            try:
                usuario = Estudiante.objects.get(
                    password=password,
                    matricula=matricula
                )
                modelo_usuario = 'estudiante'
            except Estudiante.DoesNotExist:
                pass

        # Buscar en el modelo Docente (solo por codigo_doc)
        if not usuario and codigo_doc:
            try:
                usuario = Docente.objects.get(
                    password=password,
                    codigo_doc=codigo_doc
                )
                modelo_usuario = 'docente'
            except Docente.DoesNotExist:
                pass

        # Si no se encontró el usuario en ninguno de los modelos
        if not usuario:
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar el nivel de acceso según el modelo de usuario
        if modelo_usuario == 'administrativo':
            if usuario.acceso in ['solo_ver', 'ver_agregar', 'superusuario']:
                serializer = AdministrativoAccesoSerializer(usuario)
                return Response(
                    {
                        "mensaje": "Acceso permitido",
                        "nivel_acceso": usuario.acceso,
                        "id": usuario.id,
                        "datos": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "No tienes permisos de acceso válidos."},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Si es Estudiante o Docente, solo retornamos los datos asociados
        if modelo_usuario == 'estudiante':
            serializer = EstudianteSerializer(usuario)
        elif modelo_usuario == 'docente':
            serializer = DocenteSerializer(usuario)

        return Response(
            {
                "mensaje": "Acceso permitido",
                "id": usuario.id,
                "datos": serializer.data
            },
            status=status.HTTP_200_OK
        )

        # Si el tipo de usuario no se reconoce, se retorna un error
        return Response(
            {"error": "Tipo de usuario no reconocido."},
            status=status.HTTP_400_BAD_REQUEST
        )



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class ReporteViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar los reportes generados por el sistema.
    Permite obtener todos los reportes y crear nuevos reportes.
    """
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

    def perform_create(self, serializer):
        # Aquí puedes agregar lógica adicional al crear un reporte si es necesario
        serializer.save()



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class VerificarEstudiante(APIView):
    """
    Vista para verificar las inscripciones y pagos de un estudiante.
    Proporciona detalles sobre los cursos en los que el estudiante está inscrito,
    los pagos pendientes relacionados con esas inscripciones y el porcentaje de ocupación
    de cada curso.
    """
    def get(self, request, estudiante_id):
        # Verifica si el estudiante tiene inscripciones
        inscripciones = Inscripcion.objects.filter(estudiante_id=estudiante_id)
        if not inscripciones.exists():
            return Response({"detalle": "El estudiante no tiene inscripciones."}, status=404)
        
        resultado = []
        for inscripcion in inscripciones:
            # Calcula la cantidad de inscritos en el curso
            curso = inscripcion.curso
            cantidad_inscritos = Inscripcion.objects.filter(curso=curso).count()
            capacidad_curso = curso.capacidad

            # Evita división por cero y calcula el porcentaje de ocupación
            if capacidad_curso > 0:
                porcentaje_ocupacion = round((cantidad_inscritos / capacidad_curso) * 100, 2)
            else:
                porcentaje_ocupacion = 0.0
            
            # Busca pagos pendientes relacionados con la inscripción
            pagos_pendientes = Pago.objects.filter(inscripcion=inscripcion, estado_pago="pendiente")
            
            pagos_pendientes_data = []
            for pago in pagos_pendientes:
                # Buscar el historial de cambios del pago
                historial_pagos = HistorialPago.objects.filter(pago=pago).order_by('-fecha_cambio')

                # Si existe historial, buscamos el último cambio
                ultimo_historial = historial_pagos.first() if historial_pagos.exists() else None

                # Agregar el pago a la lista
                pagos_pendientes_data.append({
                    "id": pago.id,
                    "monto": str(pago.monto),  # Convertimos a string para evitar problemas de serialización
                    "estado_pago": pago.estado_pago,
                    "fecha_vencimiento": pago.fecha_vencimiento.isoformat(),
                    "comentario": ultimo_historial.comentario if ultimo_historial else "Sin cambios recientes",
                    "estado_pago_anterior": ultimo_historial.estado_pago_anterior if ultimo_historial else None,
                    "estado_pago_nuevo": ultimo_historial.estado_pago_nuevo if ultimo_historial else None,
                    "fecha_pago": pago.fecha_pago.isoformat() if pago.fecha_pago else None
                })
            
            # Agregar los resultados del curso con pagos pendientes
            resultado.append({
                "curso": curso.nombre,
                "estado_inscripcion": inscripcion.estado,
                "pagos_pendientes": pagos_pendientes_data,
                "porcentaje_ocupacion": porcentaje_ocupacion,
                "capacidad_curso": capacidad_curso,
                "inscritos_actuales": cantidad_inscritos
            })
        
        return Response(resultado, status=200)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class DocenteCursoView(APIView):
    """
    Vista para obtener información de los cursos asignados a un docente.
    Proporciona detalles sobre la capacidad de los cursos, la cantidad de inscritos,
    el porcentaje de ocupación, y los cupos disponibles. Envía una notificación
    al docente si un curso alcanza el 50% de ocupación.
    """
    def get(self, request, docente_id):
        try:
            # Obtener el docente por su ID
            docente = Docente.objects.get(id=docente_id)

            # Obtener todos los cursos del docente
            cursos = Curso.objects.filter(docente_id=docente)

            # Lista para almacenar la información de los cursos
            cursos_data = []

            for curso in cursos:
                # Obtener inscripciones relacionadas con el curso
                inscripciones = Inscripcion.objects.filter(curso=curso)

                # Calcular la cantidad de alumnos inscritos
                cantidad_inscritos = inscripciones.count()

                # Calcular el porcentaje de ocupación
                capacidad_curso = curso.capacidad
                porcentaje_inscritos = (cantidad_inscritos / capacidad_curso) * 100 if capacidad_curso > 0 else 0
                cupos_disponibles = capacidad_curso - cantidad_inscritos

                # Notificación al docente si se alcanza el 50% de capacidad
                if porcentaje_inscritos >= 50 and curso.estado == "inactivo":
                    curso.estado = "activo"  # Activar el curso
                    curso.save()
                    # Enviar notificación por correo
                    send_mail(
                        subject=f"Curso {curso.nombre} listo para pagos",
                        message=f"El curso {curso.nombre} ha alcanzado el 50% de su capacidad. "
                                f"Cantidad de inscritos: {cantidad_inscritos}.",
                        from_email="admin@cursos.com",
                        recipient_list=[docente.correo],
                        fail_silently=False,
                    )

                # Añadir información del curso a la lista
                cursos_data.append({
                    "id": curso.id,
                    "nombre": curso.nombre,
                    "descripcion": curso.descripcion,
                    "capacidad": capacidad_curso,
                    "cantidad_inscritos": cantidad_inscritos,
                    "cupos_disponibles": cupos_disponibles,
                    "tarifa": str(curso.tarifa),
                    "estado": curso.estado,
                    "docente": docente.nombre_completo,
                    "porcentaje_ocupacion": round(porcentaje_inscritos, 2)  # Redondeado a 2 decimales
                })

            # Devolver la información en la respuesta
            return Response(cursos_data, status=status.HTTP_200_OK)

        except Docente.DoesNotExist:
            return Response(
                {"error": "El docente no existe."},
                status=status.HTTP_404_NOT_FOUND
            )
        