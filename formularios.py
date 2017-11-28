from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired,EqualTo,Regexp,Length

#En este archivo se encuentran todas las clases de Busqueda
class buscacliente(FlaskForm):
    parametro = StringField('Escriba el Nombre del Cliente: ', validators=[Length(min=3, max=100, message="Minimo de 3 caracteres"),DataRequired(message="Debe escribir valor")])

class buscaproducto(FlaskForm):
    parametro = StringField('Escriba el Nombre del Producto que busca: ', validators=[Length(min=3, max=100, message="Minimo de 3 caracteres"),DataRequired(message="Debe escribir un valor")])

class SearchCant(FlaskForm):
    parametro = StringField('Escriba la Cantidad del Producto: ', validators=[DataRequired(message="Debe escribir un valor"),Regexp(regex="\d+", message="Solo nùmeros enteros ")])

class SearchPrecio(FlaskForm):
    parametro = StringField('Escriba el Precio que busca: ', validators=[DataRequired(message="Debe escribir un valor"),Regexp(regex="^(\d|-)?(\d|,)*\.?\d*$", message="Ingrese un precio valido")])
    

#Clases para validar usuarios y contraseñas.
class Veri_sesion(FlaskForm):
    nombrese = StringField('Usuario:', validators=[DataRequired(message="Debe escribir un nombre de usuario")])
    contrase = PasswordField('Contraseña:', validators=[DataRequired(message="Debe escribir una contraseña")])


#clase para el nuevo usuario y checkeo de contraseñas.
class CreaUsuario(FlaskForm):
    name = StringField('Usuario:', validators=[DataRequired(message="Debe escribir un nombre de usuario")])
    pass1 = PasswordField('Contraseña:', validators=[DataRequired(message="Debe escribir una contraseña")])
    pass2 = PasswordField('Repita Contraseña:', validators=[DataRequired(message="Debe escribir de nuevo su contraseña"),EqualTo('pass1', message='Las contraseñas deben coincidir')])
