from django.db import models

# from django.contrib.gis.geos import LineString

""" 
Clases a crear 
    - Agencia (agency)
    - Paradas (stops)
    - Rutas (routes)
    - Viajes (trips)
    - Horario (stop_times)
    - Calendario (calendar)
    - Feriados (calendar_dates)
    *****
    *****
    - Zone  Para agregar tarifas - ForeignKey en Stop
    - Fare  Para agregar tarifas
    - Shape Se usa como ForeignKey en Trip

Nota: todos deben tener el __str__()
"""
class Agency(models.Model):
    """One or more transit agencies that provide the data in this feed.
    Maps to agency.txt in the GTFS feed.
    """
    agency_id = models.CharField(
        primary_key=True,
        max_length=255, blank=True, db_index=True,
        help_text="Identificador único de la agencia de transportes")
    name = models.CharField(
        max_length=255,
        help_text="Nombre completo de la agencia de transportes")
    url = models.URLField(
        blank=True, help_text="URL de la agencia de transportes")
    timezone = models.CharField(
        max_length=255,
        help_text="Zona horaria de la agencia de transportes")
    lang = models.CharField(
        max_length=2, blank=True,
        help_text="ISO 639-1 código del lenguaje primario")
    phone = models.CharField(
        max_length=255, blank=True,
        help_text="Número de teléfono")
    fare_url = models.URLField(
        blank=True, help_text="URL para la compra de tiquetes en línea")
    email = models.EmailField(max_length=254,  blank=True, help_text="Customer Service email")

    def __str__(self):
        return self.name

class Stop(models.Model):
    """A stop or station
    Maps to stops.txt in the GTFS feed.
    """    
    stop_id = models.CharField(
        primary_key=True,
        max_length=255, db_index=True,
        help_text="Identificador único de una parada o estación.")
    code = models.CharField(
        max_length=255, blank=True,
        help_text="Identificador único (texto pequeño o número) de pasajeros.")
    name = models.CharField(
        max_length=255,
        help_text="Nombre de la parada.")
    # tts_stop_name = models.CharField(
    #     max_length=255,
    #     help_text="Readable version of the name (no abbreviations).")
    desc = models.CharField(
        "description",
        max_length=255, blank=True,
        help_text='Descripción de la parada.')
    lat = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        help_text='WGS 84 latitud de la parada o estación')
    lon = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        help_text='WGS 84 longitud de la parada o estación')
    zone = models.ForeignKey(
        'Zone', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Fare zone for a stop ID.") # ¿a qué se refiere acá?
    url = models.URLField(
        blank=True, help_text="URL de la parada")
    location_type = models.CharField(
        max_length=1, blank=True, choices=(('0', 'Parada'), ('1', 'Estación')),
        help_text="¿Es una parada o una estación?")
    parent_station = models.ForeignKey(
        'Parada', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="La estación asociada con la parada")
    timezone = models.CharField(
        max_length=255, blank=True,
        help_text="Zona horaria para la parada")
    wheelchair_boarding = models.CharField(
        max_length=1, blank=True,
        choices=(
            ('0', 'No hay información'),
            ('1', 'Algunas sillas de ruedas pueden subir'),
            ('2', 'Las sillas de ruedas no pueden subir')),
        help_text='¿Es posible subir al transporte en silla de ruedas?')
    
    def __str__(self):
        return self.stop_id

class Route(models.Model):
    """A transit route
    Maps to route.txt in the GTFS feed.
    """
    route_id = models.CharField(
        primary_key=True,
        max_length=64, db_index=True,
        help_text="Identificador único de la ruta.")
    agency = models.ForeignKey(
        'Agency', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Agencia de transportes de la ruta.")
    short_name = models.CharField(
        max_length=63,
        help_text="Nombre corto de la ruta")
    long_name = models.CharField(
        max_length=255,
        help_text="Nombre largo de la ruta")
    desc = models.TextField(
        "description",
        blank=True,
        help_text="Descripción detallada de la ruta")
    route_type = models.IntegerField(
        "route type",
        default=3,
        choices=((0, 'Tranvía o tren ligero'),
                 (1, 'Subterráneo o metro'),
                 (2, 'Ferrocarril'),
                 (3, 'Bus'),
                 (4, 'Ferry'),
                 (5, 'Teleférico'),
                 (6, 'Gondola'),
                 (7, 'Funicular')),
        help_text='Medio de transporte usado en la ruta')
    url = models.CharField(
        max_length=32,
        blank=True, help_text="Página web de la ruta")
    color = models.CharField(
        max_length=6, blank=True,
        help_text="Color de la ruta en hexadecimal")
    text_color = models.CharField(
        max_length=6, blank=True,
        help_text="Color del texto de ruta en hexadecimal")
    
    def __str__(self):
        return self.long_name

class Trip(models.Model):
    """A trip along a route
    This implements trips.txt in the GTFS feed
    """
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    service = models.ForeignKey(
        'Calendar', null=True, blank=True, on_delete=models.SET_NULL)
    trip_id = models.CharField(
        primary_key=True,
        max_length=255, db_index=True,
        help_text="Indentificador único de viaje.")
    headsign = models.CharField(
        max_length=255, blank=True,
        help_text="Identificación de destino para pasajeros.")
    short_name = models.CharField(
        max_length=63, blank=True,
        help_text="Nombre corto utilizado en horarios y letreros.")
    direction = models.CharField(
        max_length=1, blank=True,
        choices=(('0', 'Hacia San José'), ('1', 'Desde San José')),
        help_text="Dirección para rutas en dos sentidos.")
    # block = models.ForeignKey(
    #     'Block', null=True, blank=True, on_delete=models.SET_NULL,
    #     help_text="Block of sequential trips that this trip belongs to.")
    shape = models.ForeignKey(
        'Shape', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Forma usada para el viaje.")
    wheelchair_accessible = models.CharField(
        max_length=1, blank=True,
        choices=(
            ('0', 'No hay información.'),
            ('1', 'Hay espacio para el transporte de sillas de ruedas.'),
            ('2', 'No hay espacio para el transporte de sillas de ruedas.')),
        help_text='¿Hay espacio para el transporte de sillas de ruedas?')
    bikes_allowed = models.CharField(
        max_length=1, blank=True,
        choices=(
            ('0', 'No hay información.'),
            ('1', 'Hay espacio para el transporte de bicicletas.'),
            ('2', 'No hay espacio para el transporte de bicicletas.')),
        help_text='¿Hay espacio para el transporte de bicicletas?')
    
    def __str__(self):
        return self.trip_id

class StopTime(models.Model):
    """A specific stop on a route on a trip.
    This implements stop_times.txt in the GTFS feed
    """
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    stop = models.ForeignKey('Stop', on_delete=models.CASCADE)
    arrival_time = models.TimeField(
        default=None, null=True, blank=True,
        help_text="Hora de llegada. Debe configurarse para las últimas paradas del viaje.)
    departure_time = models.TimeField(  
        auto_now=False, auto_now_add=False,
        default=None, null=True, blank=True,
        help_text='Hora de salida. Debe configurarse para las últimas paradas del viaje.')
    stop_sequence = models.PositiveIntegerField()
    stop_headsign = models.CharField(
        max_length=255, blank=True,
        help_text="Texto de referencia que identifica la parada para los pasajeros.")
    pickup_type = models.CharField(
        max_length=1, blank=True,
        choices=(('0', 'Recogida programada regularmente.'),
                 ('1', 'No hay recogida disponible.'),
                 ('2', 'Debe llamar a la agencia para coordinar recogida.'),
                 ('3', 'Debe coordinar con conductor para agendar recogida.')),
        help_text="¿Cómo se recoge a los pasajeros?")
    drop_off_type = models.CharField(
        max_length=1, blank=True,
        choices=(('0', 'Llegadas programadas regularmente.'),
                 ('1', 'No hay llegadas disponibles.'),
                 ('2', 'Debe llamar a la agencia para coordinar llegada.'),
                 ('3', 'Debe coordinar con el conductor para agendar la llegada.')),
        help_text="¿Cómo se deja a los pasajeros en su destino?")
    # shape_dist_traveled = models.FloatField(
    #     "shape distance traveled",
    #     null=True, blank=True,
    #     help_text='Distance of stop from start of shape')
    # timepoint = models.CharField(
    #     max_length=1, blank=True, default=0,
    #     choices=(('0', 'Hora aproximada'),
    #              ('1', 'Hora exacta')),
    #     help_text="Exactitud de la hora de llegada y salida")
    
    def __str__(self):
        return str(self.trip)

class Calendar(models.Model):
    """Calendar with service disponibility for one or more routes 
    This implements trips.txt in the GTFS feed
    """
    service_id = models.CharField(
        primary_key=True,
        max_length=255, db_index=True,
        help_text="Indentificador único de un calendario.")
    monday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los lunes incluidos en este período'),
            ('0', 'El servcio no está disponible los lunes incluidos en este período')),
        help_text='¿El servicio está disponible los lunes?')
    tuesday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los martes incluidos en este período'),
            ('0', 'El servcio no está disponible los martes incluidos en este período')),
        help_text='¿El servicio está disponible los martes?')
    wednesday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los miércoles incluidos en este período'),
            ('0', 'El servcio no está disponible los miércoles incluidos en este período')),
        help_text='¿El servicio está disponible los miércoles?')    
    thursday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los jueves incluidos en este período'),
            ('0', 'El servcio no está disponible los jueves incluidos en este período')),
        help_text='¿El servicio está disponible los jueves?')
    friday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los viernes incluidos en este período'),
            ('0', 'El servcio no está disponible los viernes incluidos en este período')),
        help_text='¿El servicio está disponible los viernes?')
    saturday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los sábados incluidos en este período'),
            ('0', 'El servcio no está disponible los sábados incluidos en este período')),
        help_text='¿El servicio está disponible los sábados?')
    sunday = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio sí está disponible los domingos incluidos en este período'),
            ('0', 'El servcio no está disponible los domingos incluidos en este período')),
        help_text='¿El servicio está disponible los domingos?')
    start_date = models.DateField(
        auto_now=False, auto_now_add=False,
        default=None,
        help_text='Inicio de la vigencia del horario')
    end_date = models.DateField(
        auto_now=False, auto_now_add=False,
        default=None,
        help_text='Fin de la vigencia del horario')
    
    def __str__(self):
        return self.service_id

class CalendarDate(models.Model):
    """Calendar without service disponibility for one or more routes 
    This implements calendar_dates.txt in the GTFS feed
    """
    service = models.ForeignKey('Calendar', on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False, auto_now_add=False,
        default=None,
        help_text='Fecha en que se aplica el feriado')
    exception_type = models.CharField(
        max_length=1,
        choices=(
            ('1', 'El servicio ha sido agregado para la fecha especificada'),
            ('2', 'El servicio ha sido removido de la fecha especificada')),
        help_text='¿Agregar o remover servicio?')
    holiday_name = models.CharField(
        max_length=64,
        help_text="Nombre oficial del feriado")

    def __str__(self):
        return self.holiday_name

class Fare(models.Model):
    """A fare class"""

    fare_id = models.CharField(
        primary_key=True,
        max_length=255, db_index=True,
        help_text="Identificador único de la clase de tarifa.")
    price = models.DecimalField(
        max_digits=17, decimal_places=4,
        help_text="Precio de tarifa, en unidades especificadas en currency_type")
    currency_type = models.CharField(
        max_length=3,
        help_text="ISO 4217 código alfabético de moneda: CRC")
    payment_method = models.IntegerField(
        default=1,
        choices=((0, 'La tarifa se paga abordo.'),
                 (1, 'La tarifa se paga previo a subir al transporte.')),
        help_text="¿Cuándo se paga la tarifa?")
    transfers = models.IntegerField(
        default=None, null=True, blank=True,
        choices=((0, 'No se permiten transferencias en esta tarifa.'),
                 (1, 'Los pasajeros pueden transferir una vez.'),
                 (2, 'Los pasajeros pueden transferir dos veces.'),
                 (None, 'Se pueden realizar transferencias ilimitadas.')),
        help_text="¿Se permiten las transferencias?")
    transfer_duration = models.IntegerField(
        null=True, blank=True,
        help_text="Tiempo en segundos hasta que un tiquete o transferencia expira")

    def __str__(self):
        return self.fare_id

class Zone(models.Model):
    """Represents a fare zone.
    This data is not represented as a file in the GTFS. It appears as an
    identifier in the fare_rules and the stop tables.
    """
    zone_id = models.CharField(
        primary_key=True,
        max_length=63, db_index=True,
        help_text="Identificador único de una zona.")

    def __str__(self):
        return self.zone_id

# class Shape(models.Model):
#     """The path the vehicle takes along the route.
#     Implements shapes.txt."""
#     shape_id = models.CharField(
#         max_length=255, db_index=True,
#         help_text="Unique identifier for a shape.")
#     geometry = models.LineStringField(
#         null=True, blank=True,
#         help_text='Geometry cache of ShapePoints')

class Shape(models.Model):
    """The path the vehicle takes along the route.
    Implements shapes.txt."""
    shape_id = models.CharField(
        primary_key=True,
        max_length=255, db_index=True,
        help_text="Identificador único de una forma.")
    pt_lat = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        help_text='WGS 84 latitud de punto de la forma.')
    pt_lon = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        help_text='WGS 84 longitud de punto de la forma')
    pt_sequence = models.PositiveIntegerField(
        help_text='Secuencia en la que los puntos de la forma se conectan para crear la forma')
    
    def __str__(self):
        return self.shape_id
