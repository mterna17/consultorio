#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------



app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Paciente:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            dni INT,
            apellido VARCHAR(255) NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            edad INT NOT NULL,
            especialidad VARCHAR(255) NOT NULL,
            diagnostico VARCHAR(255) NOT NULL)''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_paciente(self, dni, apellido, nombre, edad, especialidad, diagnostico):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute(f"SELECT * FROM productos WHERE dni = {dni}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        
        sql = "INSERT INTO productos (dni, apellido, nombre, edad, especialidad, diagnostico) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (dni, apellido, nombre, edad, especialidad, diagnostico)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def consultar_paciente(self, dni):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE dni = {dni}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_paciente(self, dni, nuevo_apellido, nuevo_nombre, nueva_edad, nueva_especialidad, nuevo_diagnostico):
        sql = "UPDATE productos SET apellido = %s, nombre = %s, edad = %s, especialidad = %s, diagnostico = %s WHERE dni = %s"
        valores = (nuevo_apellido, nuevo_nombre, nueva_edad, nueva_especialidad, nuevo_diagnostico, dni)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_pacientes(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos

    #----------------------------------------------------------------
    def eliminar_paciente(self, dni):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM productos WHERE dni = {dni}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_paciente(self, dni):
        # Mostramos los datos de un producto a partir de su código
        producto = self.consultar_paciente(dni)
        if producto:
            print("-" * 40)
            print(f"DNI         : {producto['dni']}")
            print(f"Apellido    : {producto['apellido']}")
            print(f"Nombre      : {producto['nombre']}")
            print(f"Edad        : {producto['edad']}")
            print(f"Especialidad: {producto['especialidad']}")
            print(f"Diagnostico : {producto['diagnostico']}")
            print("-" * 40)
        else:
            print("Paciente no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
paciente = Paciente(host='localhost', user='root', password='', database='prueba8')

# Agrego elementos a la BD para que no este vacia
paciente.agregar_paciente(42326851, 'Martínez', 'Valentina', 25, 'Bacteriología', 'Faringitis')
paciente.agregar_paciente(37299645, 'Pérez', 'Francisco', 30, 'Clínica Médica', 'Resfriado')
paciente.agregar_paciente(44846123, 'López', 'Carlos', 20, 'Dermatología', 'Acné')
paciente.agregar_paciente(26541382, 'Díaz', 'Martín', 42, 'Cardiología', 'Hipertensión arterial')
paciente.agregar_paciente(31552917, 'Sánchez', 'Ana', 33, 'Clínica Médica', 'Gripe')
paciente.agregar_paciente(27845138, 'Fernández', 'Juan', 41, 'Fisioterapia', 'Dolor crónico')
paciente.agregar_paciente(38767251, 'Gómez', 'Lucía', 29, 'Fonoaudiología', 'Trastorno de voz')
paciente.agregar_paciente(43428652, 'González', 'María', 23, 'Clínica Médica', 'Infección urinaria')
paciente.agregar_paciente(17538653, 'Rodríguez', 'Laura', 57, 'Cardiología', 'Hipercolesterolemia')
# Datos para agregar a la tabla
#paciente.agregar_paciente(23852146, 'Álvarez', 'Diego', 46, 'Endocrinología', 'Diabetes')


# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/imagenes/'

#--------------------------------------------------------------------
@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = paciente.listar_pacientes()
    return jsonify(productos)


#--------------------------------------------------------------------
@app.route("/productos/<int:dni>", methods=["GET"])
def mostrar_producto(dni):
    producto = paciente.consultar_paciente(dni)
    if producto:
        return jsonify(producto), 201
    else:
        return "Paciente no encontrado", 404


#--------------------------------------------------------------------
@app.route("/productos", methods=["POST"])
def agregar_producto():
    #Recojo los datos del form
    dni = request.form['dni']
    apellido = request.form['apellido']
    nombre = request.form['nombre']
    edad = request.form['edad']
    especialidad = request.form['especialidad']
    diagnostico = request.form['diagnostico']  
    #nombre_imagen=""

    # Me aseguro que el producto exista
    producto = paciente.consultar_paciente(dni)
    if not producto: # Si no existe el producto...
        # Genero el nombre de la imagen
        # nombre_imagen = secure_filename(especialidad.filename)
        # nombre_base, extension = os.path.splitext(nombre_imagen)
        # nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        
        if  paciente.agregar_paciente(dni, apellido, nombre, edad, especialidad, diagnostico):
            #especialidad.save(os.path.join(RUTA_DESTINO, nombre_imagen))
            return jsonify({"mensaje": "Paciente agregado correctamente."}), 201
        else:
            return jsonify({"mensaje": "Error al agregar el paciente."}), 500

    else:
        return jsonify({"mensaje": "Paciente ya existe."}), 400
    

#--------------------------------------------------------------------
@app.route("/productos/<int:dni>", methods=["PUT"])
def modificar_paciente(dni):
    #Recojo los datos del form
    nuevo_apellido = request.form.get("apellido")
    nuevo_nombre = request.form.get("nombre")
    nueva_edad = request.form.get("edad")
    nueva_especialidad = request.form.get("especialidad")
    nuevo_diagnostico = request.form.get("diagnostico")

    # Procesamiento de la imagen
    # nombre_imagen = secure_filename(imagen.filename)
    # nombre_base, extension = os.path.splitext(nombre_imagen)
    # nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    # Busco el producto guardado
    # producto = producto = catalogo.consultar_paciente(dni)
    # if producto: # Si existe el producto...
    #     imagen_vieja = producto["imagen_url"]
    #     # Armo la ruta a la imagen
    #     ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

    #     # Y si existe la borro.
    #     if os.path.exists(ruta_imagen):
    #         os.remove(ruta_imagen)
    
    if paciente.modificar_paciente(dni, nuevo_apellido, nuevo_nombre, nueva_edad, nueva_especialidad, nuevo_diagnostico):
        # imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        return jsonify({"mensaje": "Paciente modificado"}), 200
    else:
        return jsonify({"mensaje": "Paciente no encontrado"}), 403

#--------------------------------------------------------------------
@app.route("/productos/<int:dni>", methods=["DELETE"])
def eliminar_paciente(dni):
    # Busco el producto guardado
    # producto = paciente.consultar_paciente(dni)
    # if producto: # Si existe el producto...
        # imagen_vieja = producto["imagen_url"]
        # Armo la ruta a la imagen
        # ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe la borro.
        # if os.path.exists(ruta_imagen):
            # os.remove(ruta_imagen)

    # Luego, elimina el producto del catálogo
    if paciente.eliminar_paciente(dni):
        return jsonify({"mensaje": "Paciente eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el paciente"}), 500
    

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)