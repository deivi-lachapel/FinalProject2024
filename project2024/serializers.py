from rest_framework import serializers
from .models import Curso, Pago, Inscripcion, Estudiante,Docente, Administrativo, HistorialPago, Reembolso, Notificacion, Reporte


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class AdministrativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrativo
        fields = '__all__'


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__' 


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'  # O puedes especificar los campos que deseas incluir


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

    def validate(self, data):
        if data['monto'] <= 0:
            raise serializers.ValidationError("El monto debe ser mayor que cero.")
        return data


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class HistorialPagoSerializer(serializers.ModelSerializer):
    pago = PagoSerializer()  # Define el serializer para el pago anidado

    class Meta:
        model = HistorialPago
        fields = ['pago', 'estado_pago_anterior', 'estado_pago_nuevo', 'fecha_cambio', 'comentario']
        read_only_fields = ['fecha_cambio']  # Este campo se genera automáticamente y no debe ser modificado

    def create(self, validated_data):
        # Extraer los datos del pago del serializer anidado
        pago_data = validated_data.pop('pago')
        
        # Crear el pago relacionado con este historial de pago
        pago = Pago.objects.create(**pago_data)
        
        # Crear el historial de pago usando el pago recién creado
        historial_pago = HistorialPago.objects.create(pago=pago, **validated_data)
        
        return historial_pago

    def update(self, instance, validated_data):
        # Actualizar el pago si es necesario
        pago_data = validated_data.pop('pago', None)
        
        if pago_data:
            # Si se proporciona un pago anidado, actualízalo
            instance.pago.monto = pago_data.get('monto', instance.pago.monto)
            instance.pago.estado_pago = pago_data.get('estado_pago', instance.pago.estado_pago)
            instance.pago.save()
        
        # Actualizar los demás campos del historial de pago
        instance.estado_pago_anterior = validated_data.get('estado_pago_anterior', instance.estado_pago_anterior)
        instance.estado_pago_nuevo = validated_data.get('estado_pago_nuevo', instance.estado_pago_nuevo)
        instance.fecha_cambio = validated_data.get('fecha_cambio', instance.fecha_cambio)
        instance.comentario = validated_data.get('comentario', instance.comentario)
        
        instance.save()
        return instance


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class ReembolsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reembolso
        fields = ['id', 'usuario', 'pago', 'motivo', 'estado', 'fecha_solicitud', 'fecha_resolucion']
        read_only_fields = ['fecha_solicitud', 'fecha_resolucion']
    
    def update(self, instance, validated_data):
        # Aquí puedes agregar lógica adicional para actualizar el estado del reembolso
        instance.estado = validated_data.get('estado', instance.estado)
        instance.fecha_resolucion = validated_data.get('fecha_resolucion', instance.fecha_resolucion)
        instance.save()
        return instance
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'tipo_notificacion', 'mensaje', 'fecha_envio', 'estado']
        read_only_fields = ['fecha_envio']  # Solo se establece automáticamente en el envío
    
    def validate(self, data):
        # Validación personalizada si es necesario
        return data


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class InscripcionSerializer(serializers.ModelSerializer):
    nombre_curso = serializers.ReadOnlyField(source='curso.nombre') 

    class Meta:
        model = Inscripcion
        fields = '__all__'


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'  # O especifica los campos que deseas incluir

    def validate(self, data):
        # Aquí puedes agregar validaciones personalizadas si es necesario
        return data


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class AdministrativoAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrativo
        fields = ['password', 'acceso', 'codigo_adm']  # El campo 'correo' se elimina
        extra_kwargs = {
            'password': {'write_only': True}  # Oculta el campo 'password' en las respuestas
        }


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class UserAuthSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    codigo_doc = serializers.CharField(required=False, allow_blank=True)
    codigo_adm = serializers.CharField(required=False, allow_blank=True)
    matricula = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        # Verificamos que al menos uno de los campos de identificador esté presente
        if not any([attrs.get('codigo_doc'), attrs.get('codigo_adm'), attrs.get('matricula')]):
            raise serializers.ValidationError("Debe proporcionar al menos un código docente, administrativo o matrícula.")
        return attrs


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'tipo_reporte', 'fecha_generacion', 'descripcion']
        read_only_fields = ['fecha_generacion']  # Solo lectura, se genera automáticamente

    def validate(self, data):
        # Validación adicional si es necesaria
        return data