# Importamos la libreria requests que sirve para tramitar peticiones HTTP usando diferentes metodos, asi como extraer informacion
import requests
# Libreria para imprimir datos de manera entendible
from pprint import pprint
# Libreria para extraer datos de una web de forma estructurada, BeatifulSoup representa el documento HTML o XML 
from bs4 import BeatifulSoup as bs
# Libreria que sirve para concatenar cadenas y luego unirlas a una URL en componentes
from urllib.parse import urljoin

# Funcion que recupera la respuesta html a partir de la url proporcionada
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

# Funcion que recupera toda la informacion potencial del HTML
def get_form_details(form):
    details = {}
    # Obtenemos el valor del atributo 'action', 'method' y las entradas 'inputs[]' del HTML y lo convertimos en minuscula
    action = form.attrs.get("action", "").lower()
    method =form.attrs.get("method", "get").lower()
    inputs = []
    # Bucle for que recorre las inputs_tags del formulario HTML y agregamos esta informacion al arreglo input[]
    for input_tags in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # Se almacena en un diccionario los datos recopilados anteriormente y retornamos el mismo
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

