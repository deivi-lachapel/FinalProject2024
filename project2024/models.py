from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Tabla Usuarios: almacena información básica de los usuarios del sistema
class Usuario(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    nombre_completo = models.CharField(max_length=255)
    cedula = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=255, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        unique_together = (('cedula', 'correo'),)

    def __str__(self):
        return self.nombre_completo


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Estudiantes: hereda de Usuarios y almacena información específica de estudiantes
class Estudiante(Usuario):
    matricula = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Docentes: hereda de Usuarios y almacena información específica de docentes
class Docente(Usuario):
    especialidad = models.CharField(max_length=255)
    fecha_contratacion = models.DateField()
    facultad = models.CharField(max_length=255)
    escuela = models.CharField(max_length=255)
    campus = models.CharField(max_length=255)
    codigo_doc = models.CharField(max_length=20, unique=True, default="default_code")  # Campo para iniciar sesión
    
    ESTATUS_CHOICES = [
        ('activo', 'Activo'),
        ('jubilado', 'Jubilado'),
    ]
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default='activo')
    
    CODIGO_CHOICES = [
        ('invitado', 'Invitado'),
        ('oficial', 'Oficial'),
    ]
    codigo = models.CharField(max_length=10, choices=CODIGO_CHOICES)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Administrativos: hereda de Usuarios y tiene permisos de acceso
class Administrativo(Usuario):
    departamento = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    fecha_ingreso = models.DateField()
    codigo_adm = models.CharField(max_length=20, unique=True, default="default_code")  # Campo para iniciar sesión

    ACCESO_CHOICES = [
        ('solo_ver', 'Solo Ver'),
        ('ver_agregar', 'Ver y Agregar'),
        ('superusuario', 'Superusuario'),
    ]
    acceso = models.CharField(max_length=15, choices=ACCESO_CHOICES, default='solo_ver')



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Cursos: almacena información sobre los cursos disponibles
class Curso(models.Model):
    TIPO_CHOICES = [
        ('curso', 'Curso'),
        ('diplomado', 'Diplomado'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    capacidad = models.IntegerField(default=0)
    docente_id = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    modulos = models.IntegerField()
    horas = models.IntegerField()
    codigo = models.CharField(max_length=20)
    profesor = models.CharField(max_length=255)
    facultad = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    imagen_url = models.URLField(blank=True, null=True)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Inscripciones: almacena las inscripciones de los estudiantes en los cursos
class Inscripcion(models.Model):
    ESTADO_CHOICES = [
        ('inscrito', 'Inscrito'),
        ('pendiente', 'Pendiente'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)

     # Método para obtener el nombre del curso
    def __str__(self):
        return f"{self.estudiante} inscrito en {self.curso.nombre}"


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Pagos: almacena información sobre los pagos realizados por los estudiantes
class Pago(models.Model):
    METODO_CHOICES = [
        ('transferencia', 'Transferencia'),
        ('Paypal', 'Paypal'),
        ('manual', 'Manual'),
    ]
    ESTADO_CHOICES = [
        ('completado', 'Completado'),
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
    ]
    
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=15, choices=METODO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=15, choices=ESTADO_CHOICES)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Historial de Pagos: para auditar cambios en los estados de pago
class HistorialPago(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    estado_pago_anterior = models.CharField(max_length=15, choices=Pago.ESTADO_CHOICES)
    estado_pago_nuevo = models.CharField(max_length=15, choices=Pago.ESTADO_CHOICES)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Reembolsos: almacena información sobre solicitudes de reembolso
class Reembolso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    motivo = models.TextField()
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'Reembolso {self.id} - {self.estado}'


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Notificaciones: almacena notificaciones enviadas a los usuarios
class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    TIPO_CHOICES = [
        ('recordatorio_pago', 'Recordatorio de Pago'),
        ('ingreso_registrado', 'Ingreso Registrado'),
    ]
    tipo_notificacion = models.CharField(max_length=25, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('pendiente', 'Pendiente'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f'Notificación {self.tipo_notificacion} para {self.usuario.nombre_completo} - {self.estado}'



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Tabla Reportes: almacena reportes generados por el sistema
class Reporte(models.Model):
    TIPO_CHOICES = [
        ('ingresos', 'Ingresos'),
        ('pagos_pendientes', 'Pagos Pendientes'),
        ('asistencia', 'Asistencia'),
    ]
    
    tipo_reporte = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f'Reporte de {self.tipo_reporte} - {self.fecha_generacion}'
