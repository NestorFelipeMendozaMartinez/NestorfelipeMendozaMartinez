from flask import Flask, render_template, request, redirect, url_for, flash
from services.usuario_service import crear_usuario, login
from services.producto_service import crear_producto, listar_productos

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clave secreta para mensajes flash

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de login y registro
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        if 'registro' in request.form:
            # Registrar nuevo usuario
            nombre = request.form['nombre']
            email = request.form['email']
            password = request.form['password']
            crear_usuario(nombre, email, password, "cliente")
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('login_route'))
        else:
            # Iniciar sesión
            email = request.form['email']
            password = request.form['password']
            usuario = login(email, password)
            if usuario:
                flash("Login exitoso.", "success")
                return redirect(url_for('index'))
            else:
                flash("Credenciales incorrectas.", "error")
    return render_template('login.html')

# Ruta para productos
@app.route('/productos', methods=['GET', 'POST'])
def productos_route():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        imagen = request.form['imagen']
        crear_producto(nombre, descripcion, precio, imagen)
        flash("Producto creado correctamente.", "success")
        return redirect(url_for('productos_route'))
    
    productos = listar_productos()
    return render_template('productos.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)