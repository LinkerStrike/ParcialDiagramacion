#!/usr/bin/env python
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from formularios import buscacliente,buscaproducto,SearchCant,SearchPrecio, Veri_sesion,CreaUsuario
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

#Creacion de una lista en donde se guadaran los datos para iniciar sesion de los usuarios
#2 try por si no encuentra los archivos csv

vali_usuario=[]
try:
    with open('users.csv') as archivo:
        mirar_csv = csv.reader(archivo)
        for linea in mirar_csv:
            vali_usuario.append(linea[0])
except FileNotFoundError:
    print('Error del csv')

try:
    with open('client.csv') as archivo:
        pass
except FileNotFoundError:
    print('Error al buscar el csv de client')

@app.route('/')
def index():
    if 'InicioSesion' in session:
        return render_template('index.html', username=session.get('InicioSesion'))
    return render_template('salir.html')

@app.route('/iniciarsesion', methods=['GET', 'POST'])
def Iniciar():
    formulario_inicio= Veri_sesion()
    if formulario_inicio.validate_on_submit():
        try:
            with open('users.csv') as archivo:
                    archicsv = csv.reader(archivo)
                    for linea in archicsv:
                        ubicacion = linea
                        nombre = ubicacion[0]
                        contra = ubicacion[1]
                        if formulario_inicio.nombrese.data == nombre and formulario_inicio.contrase.data == contra:
                            session['InicioSesion'] = formulario_inicio.nombrese.data
                            return render_template('index.html', username=session.get('InicioSesion'))
        except IndexError:
            return 'usuario de users.csv invalido'        
        except FileNotFoundError:
            return 'No se encuentra el archivo de usuariosbase'
    return render_template('sesion.html', form=formulario_inicio, username=session.get('InicioSesion'))

#Que sea visible la base de datos si inicio sesion
@app.route('/Cliente', methods=['GET', 'POST'])
def client():
    if 'InicioSesion' in session:
        try:
            with open('client.csv', 'r') as archivo:
                datalines = csv.reader(archivo)                
                titulos = next(datalines)                                
                return render_template('datos.html', cabeza=titulos, cuerpo=datalines, username=session.get('InicioSesion'))
        except FileNotFoundError:
            return 'No se encuentra client.csv'
    return render_template('salir.html')

@app.route('/Venta',methods=['GET', 'POST'])
def Ulventas():
    with open('vent.csv', 'r') as archi:
        datlines = csv.reader(archi)                
        title = next(datlines)                                
        return render_template('Venta.html', cabeza=title, cuerpo=datlines, username=session.get('InicioSesion'))

#Funcionan solo si el usuario inicio sesion.
#Busqueda de cliente
@app.route('/Buscliente', methods=['GET', 'POST'])
def busquedacliente():
    if 'InicioSesion' in session:        
        formu_name = buscacliente()    
        try:
            with open('client.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'cvs de base de datos inexistente'    
        if formu_name.validate_on_submit():            
            with open('client.csv') as archivo:
                try:
                    archicsv = csv.reader(archivo)
                    lista=[]
                    for linea in archicsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        cliente = ubicacion[1]
                        # El primer if tiene los encabezados y el segundo la informacion que coincide
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        if formu_name.parametro.data.lower() in cliente.lower():
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            lista.append(info)
                    #Este if por si no se encuentran los resultados.
                    if len(lista) == 0 :
                        flash('El cliente que busca no se encuentra en nuestra Base de Datos.')
                        return render_template('cliente.html', form=formu_name, username=session.get('InicioSesion'))
                    return render_template('datos.html', form=formu_name, cabeza=tupla, cuerpo=lista, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Numero invalido de datos a corroborar.'           
        return render_template('cliente.html', form=formu_name, username=session.get('InicioSesion'))
    return render_template('salir.html')

#Busqueda de Producto
@app.route('/producto', methods=['GET', 'POST'])
def busquedaproducto():
    if 'InicioSesion' in session:        
        formu_prod = buscaproducto()
        try:
            with open('client.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'Error al buscar el csv de client'
        if formu_prod.validate_on_submit():
            with open('client.csv') as archivo:
                try:
                    archicsv = csv.reader(archivo)
                    lista=[]
                    for linea in archicsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        producto = ubicacion[2]
                        # El primer if tiene los encabezados y el segundo la informacion que coincide
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        if formu_prod.parametro.data.lower() in producto.lower():
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            lista.append(info) 
                    #Este if por si no se encuentran los resultados.
                    if len(lista) == 0 :
                        flash('El Producto que busca no se encuentra en nuestra Base de Datos.')
                        return render_template('producto.html', form=formu_prod, username=session.get('InicioSesion'))
                    return render_template('datos.html', form=formu_prod, cabeza=tupla, cuerpo=lista, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Error al buscar el producto'                           
        return render_template('producto.html', form=formu_prod, username=session.get('InicioSesion'))
    return render_template('salir.html')


#Consulta de cantidad.
@app.route('/cantidad', methods=['GET', 'POST'])
def consulcantidad():
    if 'InicioSesion' in session:
        form_cantidad = SearchCant()
        try:
            with open('client.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'Error al buscar el csv de client'
        if form_cantidad.validate_on_submit():
            with open('client.csv') as archivo:
                try:
                    archicsv = csv.reader(archivo)
                    lista=[]
                    for linea in archicsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        cantidad = ubicacion[3]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las lista que coincide el cliente
                        if form_cantidad.parametro.data == cantidad:
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            lista.append(info)                            
                    #Este if se adiciono para informar que no se encuentran resultados.
                    if len(lista) == 0 :
                        flash('La cantidad ingresada  es inexistente en nuestra base de datos.')
                        return render_template('cantidad.html', form=form_cantidad, username=session.get('InicioSesion'))
                    return render_template('datos.html', form=form_cantidad, cabeza=tupla, cuerpo=lista, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Error al encontrar los usuarios y cantidad'                           
        return render_template('cantidad.html', form=form_cantidad, username=session.get('InicioSesion'))
    return render_template('salir.html')


#Consulta de precios.
@app.route('/precio', methods=['GET', 'POST'])
def consulprecio():
    if 'InicioSesion' in session:
        form_precio = SearchPrecio()
        try:
            with open('client.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de lista'
        if form_precio.validate_on_submit():
            with open('client.csv') as archivo:
                try:
                    archicsv = csv.reader(archivo)
                    lista=[]
                    for linea in archicsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        precio = ubicacion[4]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las lista que coincide el cliente
                        if form_precio.parametro.data == precio:
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            lista.append(info)                           
                    #Este if se adiciono para informar que no se encuentran resultados.
                    if len(lista) == 0 :
                        flash('El Precio que busca no se encuentra en nuestra Base de Datos.')
                        return render_template('precio.html', form=form_precio, username=session.get('InicioSesion'))
                    return render_template('datos.html', form=form_precio, cabeza=tupla, cuerpo=lista, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Error al buscar el usuario y su precio'                           
        return render_template('precio.html', form=form_precio, username=session.get('InicioSesion'))
    return render_template('salir.html')

#If para confirmar contraseñas
@app.route('/register', methods=['GET', 'POST'])
def register():
    form_registro = CreaUsuario()
    if form_registro.validate_on_submit():
        if form_registro.pass1.data == form_registro.pass2.data:
            try:
                with open('users.csv', 'a') as archivo:
                    escritor = csv.writer(archivo)
                    if form_registro.name.data in vali_usuario:
                        return "Usuario existente"
                    else:
                        escritor.writerow([form_registro.name.data, form_registro.pass1.data])
                        return redirect('iniciarsesion')
            except FileNotFoundError:
                return 'No se encuentra el CSV'
        return "Revise la contraseña"
    return render_template('register.html', form=form_registro)

@app.route('/salir', methods=['GET', 'POST'])
def signoff():
    session.pop('InicioSesion', None)
    return redirect('/')

#Se agrego el , username=session.get('InicioSesion') para validar la navbar.
@app.errorhandler(404)
def paginanotf(e):
    return render_template('404.html', username=session.get('InicioSesion')), 404


#Se agrego el , username=session.get('InicioSesion') para validar la navbar.
@app.errorhandler(500)
def servererror(e):
    return render_template('500.html', username=session.get('InicioSesion')), 500


if __name__ == "__main__":
    manager.run()