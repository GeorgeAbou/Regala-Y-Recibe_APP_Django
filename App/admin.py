from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  *
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import json


#Registrando todos los modelos en el paneladmin para crear 

admin.site.register(UsuarioGeneral)
# admin.site.register(UserAdmin)
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Intercambio)
admin.site.register(Donacion)
#admin.site.register(Valoracion)

# admin.site.register(Ciudad)
admin.site.register(TipoTransaccion)


class ComunaAdmin(admin.ModelAdmin):
    list_display = ['nombre_comuna', 'ciudad']
    search_fields = ['nombre_comuna']
    list_filter = ['ciudad']

    def save_model(self, request, obj, form, change):
        if not obj.ciudad:
            raise ValidationError("La comuna debe tener una ciudad asociada.")
        super().save_model(request, obj, form, change)


class CiudadAdmin(admin.ModelAdmin):
    list_display = ['nombre_ciudad']
    search_fields = ['nombre_ciudad']

# Registra los modelos con los permisos adecuados
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Ciudad, CiudadAdmin)


# Definir el admin con acción personalizada para extraer informe de valoraciones 
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'puntaje', 'resena', 'fecha_valoracion', 'usuario_que_valora')  # Mostrar información relevante en la lista
    actions = ['filtrar_valoraciones_bajas']  # Acción personalizada

    def filtrar_valoraciones_bajas(self, request, queryset):
        # Realizamos la consulta de valoraciones menores a 3
        valoraciones_bajas = Valoracion.objects.filter(puntaje__lt=3)

        # Si hay valoraciones bajas, se genera una tabla HTML para mostrarla
        if valoraciones_bajas.exists():
            # Generar los datos para el gráfico
            usuarios = []
            puntajes = []
            fechas = []
            for valoracion in valoraciones_bajas:
                usuarios.append(f"{valoracion.usuario.nombre} {valoracion.usuario.apellido}")
                puntajes.append(valoracion.puntaje)
                fechas.append(valoracion.fecha_valoracion.strftime("%d-%m-%Y"))

            # Generar el contenido HTML con Chart.js y estilo
            html_content = """
            <html>
            <head>
                <title> Informe de usuarios con Valoraciones Menores a 3 estrellas</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        padding: 20px;
                        background-color: #f4f4f4;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 30px;
                    }
                    table, th, td {
                        border: 1px solid #ddd;
                    }
                    th, td {
                        padding: 8px;
                        text-align: center;
                    }
                    th {
                        background-color: cadetblue;
                        color:white;
                    }
                    .chart-container {
                        width: 80%;
                        margin: 0 auto;
                    }
                </style>
            </head>
            <body>
                <h2>Informe de usuarios con Valoraciones Menores a 3 estrellas</h2>
                
                <!-- Gráfico de barras con Chart.js -->
                <div class="chart-container">
                    <canvas id="valoracionesChart"></canvas>
                </div>

                <!-- Tabla con los datos -->
                <table>
                    <thead>
                        <tr>
                            <th>Usuario</th>
                            <th>Puntaje</th>
                            <th>Reseña</th>
                            <th>Fecha de Valoración</th>
                            <th>Usuario que Valora</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            # Agregar las filas de la tabla con los datos de las valoraciones
            for valoracion in valoraciones_bajas:
                html_content += f"""
                <tr>
                    <td>{valoracion.usuario.nombre} {valoracion.usuario.apellido}</td>
                    <td>{valoracion.puntaje}</td>
                    <td>{valoracion.resena or 'No hay reseña'}</td>
                    <td>{valoracion.fecha_valoracion}</td>
                    <td>{valoracion.usuario_que_valora.nombre} {valoracion.usuario_que_valora.apellido}</td>
                </tr>
                """
            
            # Cerrar la tabla
            html_content += "</tbody></table>"

            # Incluir el código para el gráfico de barras
            html_content += f"""
                <script>
                    var ctx = document.getElementById('valoracionesChart').getContext('2d');
                    var valoracionesChart = new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                            labels: {json.dumps(usuarios)},  // Nombres de los usuarios
                            datasets: [{{
                                label: 'Puntaje',
                                data: {json.dumps(puntajes)},  // Puntajes de las valoraciones
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 1,
                                barThickness: 30  // Controlar el grosor de las barras
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,  // Mantener el tamaño al cambiar el tamaño de la ventana
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    ticks: {{
                                        stepSize: 1  // Definir el paso en la escala
                                    }}
                                }},
                                x: {{
                                    ticks: {{
                                        autoSkip: true,
                                        maxRotation: 0,  // Evitar la rotación de las etiquetas
                                        minRotation: 0
                                    }}
                                }}
                            }},
                            animation: {{
                                duration: 500,  // Reducir la duración de la animación
                                easing: 'easeOutQuart'  // Hacer la animación más suave
                            }}
                        }}
                    }});
                </script>
            """

            html_content += "</body></html>"

            # Devolver la respuesta HTML con el gráfico y la tabla
            return HttpResponse(html_content, content_type="text/html")

        else:
            # Si no hay valoraciones menores a 3, mostrar un mensaje
            self.message_user(request, "No se encontraron valoraciones menores a 3.")
            return HttpResponse("No se encontraron valoraciones menores a 3", content_type="text/plain")

    filtrar_valoraciones_bajas.short_description = "Filtrar y Mostrar Valoraciones Menores a 3"

# Registra el modelo en el admin
admin.site.register(Valoracion, ValoracionAdmin)