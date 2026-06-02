from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Confirmacion
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
SPREADSHEET_ID = '1ogSseXtwVbhR1EYlRtsLXxIw9MI5ax6-8LBaGITW32Y'
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'credentials.json')

HEADERS = ['Nombre', 'Email', 'Teléfono', '¿Asistirá?', 'Adultos', 'Niños', 'Mensaje', 'Comprobante', 'Celíaco/a', 'Cant. Celíacos', 'Vegano/a', 'Cant. Veganos', 'Vegetariano/a', 'Cant. Vegetarianos', 'Otra restricción', 'Detalle otra restricción', 'Bebida', 'Fecha']

def get_google_creds():
    # Obtenemos el JSON en formato string desde las variables de entorno
    json_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    
    # Lo convertimos a diccionario
    creds_dict = json.loads(json_raw)
    
    # Definimos los alcances (scopes) necesarios
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Retornamos las credenciales listas para usar
    return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

def _get_sheet():
    creds = get_google_creds()
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    sheet = spreadsheet.sheet1
    # Agregar encabezados si la hoja está vacía
    if sheet.row_count == 0 or sheet.cell(1, 1).value != 'Nombre':
        sheet.insert_row(HEADERS, 1)
    return sheet

def _registrar_en_sheets(confirmacion):
    try:
        sheet = _get_sheet()
        fila = [
            confirmacion.nombre,
            confirmacion.email,
            confirmacion.telefono,
            'Sí' if confirmacion.asistira else 'No',
            confirmacion.numero_adultos,
            confirmacion.numero_ninos,
            confirmacion.mensaje,
            'Sí' if confirmacion.comprobante else 'No',
            'Sí' if confirmacion.celiaco else 'No',
            confirmacion.celiaco_cantidad if confirmacion.celiaco else '',
            'Sí' if confirmacion.vegano else 'No',
            confirmacion.vegano_cantidad if confirmacion.vegano else '',
            'Sí' if confirmacion.vegetariano else 'No',
            confirmacion.vegetariano_cantidad if confirmacion.vegetariano else '',
            'Sí' if confirmacion.restriccion_otro else 'No',
            confirmacion.restriccion_otro_detalle,
            confirmacion.bebida,
            confirmacion.fecha_confirmacion.strftime('%d/%m/%Y %H:%M'),
        ]
        sheet.append_row(fila)
    except Exception as e:
        # Si falla Google Sheets, no interrumpir el flujo principal
        print(f'[Google Sheets] Error al registrar: {e}')

# Create your views here.

def index(request):
    """Vista principal de la invitación"""
    if request.method == 'POST':
        try:
            restricciones = request.POST.getlist('restricciones')
            confirmacion = Confirmacion(
                nombre=request.POST.get('nombre'),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono', ''),
                asistira=request.POST.get('asistira') == 'si',
                numero_adultos=int(request.POST.get('adultos', 1)),
                numero_ninos=int(request.POST.get('ninos', 0) or 0),
                mensaje=request.POST.get('mensaje', ''),
                comprobante=request.FILES.get('comprobante'),
                celiaco='celiaco' in restricciones,
                celiaco_cantidad=int(request.POST.get('celiaco_cantidad', 0) or 0),
                vegano='vegano' in restricciones,
                vegano_cantidad=int(request.POST.get('vegano_cantidad', 0) or 0),
                vegetariano='vegetariano' in restricciones,
                vegetariano_cantidad=int(request.POST.get('vegetariano_cantidad', 0) or 0),
                restriccion_otro='otro' in restricciones,
                restriccion_otro_detalle=request.POST.get('restriccion_otro_detalle', ''),
                bebida=request.POST.get('bebida', ''),
            )
            confirmacion.save()
            _registrar_en_sheets(confirmacion)
            messages.success(request, '¡Gracias por confirmar tu asistencia!')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'Hubo un error al procesar tu confirmación. Por favor, intenta nuevamente.')
    
    return render(request, 'InvitacionVirtual/index.html')
