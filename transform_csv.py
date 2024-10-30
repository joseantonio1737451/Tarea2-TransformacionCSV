import csv
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import os

# Función para leer el archivo CSV
def leer_csv(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"El archivo {ruta_csv} no existe.")
        return []

    registros = []
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                registros.append(fila)
        return registros
    except Exception as e:
        print(f"Error leyendo el archivo CSV: {e}")
        return []

# Función para transformar los datos de CSV a XML
def transformar_a_xml(registros):
    root = Element('odoo')  # Elemento raíz XML

    for idx, registro in enumerate(registros, start=1):
        record = SubElement(root, 'record', attrib={
            'id': f'film_{idx}',
            'model': 'videoclub.peliculas'
        })
        
        # Campos individuales
        SubElement(record, 'field', name="name").text = registro.get('name', '')
        SubElement(record, 'field', name="director", ref=registro.get('director', ''))
        
        # Procesar actores separados por '-'
        actores = registro.get('actors', '').split('-')
        actor_refs = [f"ref('{actor.strip()}')" for actor in actores]
        SubElement(record, 'field', name="actors", eval=f"[(6,0,[{','.join(actor_refs)}])]")
        
        # Otros campos
        SubElement(record, 'field', name="release").text = registro.get('release', '')
        SubElement(record, 'field', name="country").text = registro.get('country', '')
        SubElement(record, 'field', name="duration").text = registro.get('duration', '')
        SubElement(record, 'field', name="rating").text = registro.get('rating', '')
        SubElement(record, 'field', name="cover", file=registro.get('file', ''), type="base64")

    return root

# Función para guardar el XML en un archivo
def guardar_xml(root, ruta_salida):
    try:
        tree = ElementTree(root)
        with open(ruta_salida, "wb") as archivo_xml:
            tree.write(archivo_xml, encoding='utf-8', xml_declaration=True)
        print(f"Archivo XML guardado en {ruta_salida}")
    except Exception as e:
        print(f"Error guardando el archivo XML: {e}")

# Ejecución del programa
if __name__ == "__main__":
    ruta_csv = "entrada.csv"  # Cambia a la ruta de tu archivo CSV
    ruta_xml = "salida.xml"
    
    registros = leer_csv(ruta_csv)
    if registros:
        root = transformar_a_xml(registros)
        guardar_xml(root, ruta_xml)
