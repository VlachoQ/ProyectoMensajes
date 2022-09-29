
from flask import Flask, render_template,request
import hashlib
import controlador
from datetime import datetime
import envioemail


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login2.html")

##################### VERIFICA SI EL USUARIO EXISTE EN LA BASE DE DATOS#################################################################

@app.route("/verificarUsuario",methods=['GET', 'POST'])
def verificarUsuario():
    if request.method=='POST':
        usu = request.form["txtusuario"]
        pw = request.form["txtpass"]
        
        pw2=pw.encode()
        pw2=hashlib.sha384(pw2).hexdigest() # Metodo de encriptacion "sha384" el cual genera 96 caracteres - para tener en cuenta al momento de crear el campo en la tabla que tenga esa longitud o mas. 
       
        cuenta=len(pw2) 
        print("usuario=" + usu + " | password= " + pw)
        print("# de caracteres: ",cuenta) #solo para prueba
        print("Password Encriptado: ",pw2) #solo para prueba  
       
        respuesta=controlador.buscarUsuario(usu,pw2)
        if len(respuesta)==0:
            mensajes="Usuario No existe . . .   por favor verifique los datos ingresados    :("
            return render_template("informacion.html", data=mensajes)  
        else:
            return render_template("EnviarMsg.html")   

      
        
        
    return render_template("inbox.html")

##################### SE REGISTRA EL USUARIO Y SE ENVIA MENSAJE DE REGISTRO SATISFACTORIO##################################################

@app.route("/RegistrarUsuario",methods=['GET', 'POST'])
def RegistrarUsuario():
    if request.method=='POST':
        nombre = request.form["txtnombre"]
        email = request.form["txtusuarioregistro"]
        pw = request.form["txtpassregistro"]
        
        pw2=pw.encode()
        pw2=hashlib.sha384(pw2).hexdigest() # Metodo de encriptacion "sha384" el cual genera 96 caracteres - para tener en cuenta al momento de crear el campo en la tabla que tenga esa longitud o mas. 
       
        #cuenta=len(pw2) 
        print("usuario=" + nombre + " | email= " + email+ "| password= " + pw)
        #print("# de caracteres: ",cuenta) #solo para prueba
        #print("Password Encriptado: ",pw2) #solo para prueba  
        codigo=datetime.now() # aqui guardamos la fecha-hora y milisegundos
        codigo2=str(codigo)# lo convertimos a una cadena de caracteres
        codigo2=codigo2.replace("-","")# quitamos los (- : . " ") guiones, dos puntos, los puntos y los espacios de esa cadena
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(".","")

        mensaje="Sr. "+nombre+",  su codigo de activacion es :\n\n"+codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
        
        envioemail.enviar(email, mensaje)
        
        
        controlador.registroUsuario(nombre,email,pw2,codigo2)
      
        mensajes="Usuario Registrado Satisfactoriamente :)"
        return render_template("informacion.html", data=mensajes)  
        
        # ANTES DE REGISTRAR FALTA VALIDAR CUANDO EL USUARIO EXISTE, PASA QUE SI YA EXISTE LO INTENTA CREAR Y SE BLOQUEA LA BD

#####################################################################################################

@app.route("/ValidarActivarUsuario",methods=['GET', 'POST'])
def ValidarActivarUsuario():
    if request.method=='POST':
        codigoAct = request.form["txtcodigo"]

        respuesta= controlador.ValidarActivarUser(codigoAct)
        
        if len(respuesta)==0:
            mensajes="El Codigo de Activación no es Valido, verifiquelo :("
        else:
            mensajes="El Usuario se ha Activado Satisfactoriamente :)"    

        return render_template("informacion.html", data=mensajes)  
              


#####################################################################################################