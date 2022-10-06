
from flask import Flask, render_template,request
import hashlib
import controlador
from datetime import datetime
import envioemail


app = Flask(__name__)

origen=""  # Variable GLOBAL utilizada para guardar el correo original

##################### RUTA RAIZ #################################################################
@app.route("/")
def hello_world():
    return render_template("login2.html")
##################### VERIFICA SI EL USUARIO EXISTE EN LA BASE DE DATOS#################################################################

@app.route("/verificarUsuario",methods=['GET', 'POST'])
def verificarUsuario():
    if request.method=='POST':
        correo = request.form["txtcorreo"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        pw = request.form["txtpass"]
        pw=pw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        pw2=pw.encode()
        pw2=hashlib.sha384(pw2).hexdigest() # Metodo de encriptacion "sha384" el cual genera 96 caracteres - para tener en cuenta al momento de crear el campo en la tabla que tenga esa longitud o mas. 
       
        cuenta=len(pw2) 
        print("usuario=" + correo + " | password= " + pw)
        print("# de caracteres: ",cuenta) #solo para prueba
        print("Password Encriptado: ",pw2) #solo para prueba  
       
        respuesta=controlador.buscarUsuario(correo,pw2)

        global origen    

        if len(respuesta)==0:
            origen=""
            mensajes="Usuario No existe . . .   Verifique los datos ingresados ó vaya a la pestaña 'Registro'"
            #return render_template("informacion.html", data=mensajes)
            return render_template("login2.html", data=mensajes)  
        else:
            origen=correo
            respuesta2=controlador.listaUsuarios()
            return render_template("principal2.html", data=respuesta2, infousu=respuesta)
        

##################### SE REGISTRA EL USUARIO Y SE ENVIA MENSAJE DE REGISTRO SATISFACTORIO##################################################

@app.route("/RegistrarUsuario",methods=['GET', 'POST'])
def RegistrarUsuario():
    if request.method=='POST':
        nombre = request.form["txtnombre"]
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email = request.form["txtusuarioregistro"]
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        pw = request.form["txtpassregistro"]
        pw=pw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
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
                        # ENVIO MAIL  AL CORREO REGISTRADO
        mensaje="Sr. " +nombre+ ",  su codigo de activacion es :\n\n" +codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
        asuntoCodVerificacion="Codigo de Activación"

        envioemail.enviar(email,asuntoCodVerificacion,mensaje)
        
                        # GUARDO EL REGISTRO EN LA BASE DE DATOS
        respuesta=controlador.registroUsuario(nombre,email,pw2,codigo2)
      
        #mensajes="Usuario Registrado Satisfactoriamente. Se le ha enviado un mensaje con el Cod. de Activación"
        #return render_template("informacion.html", data=mensajes) 
        return render_template("login2.html", data=respuesta)  
        
        # ANTES DE REGISTRAR FALTA VALIDAR CUANDO EL USUARIO EXISTE, PASA QUE SI YA EXISTE LO INTENTA CREAR Y SE BLOQUEA LA BD

#####################################################################################################

@app.route("/ValidarActivarUsuario",methods=['GET', 'POST'])
def ValidarActivarUsuario():
    if request.method=='POST':
        codigoAct = request.form["txtcodigo"]
        codigoAct =codigoAct.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        respuesta= controlador.ValidarActivarUser(codigoAct)
        
        if len(respuesta)==0:
            mensajes="El Codigo de Activación no es Valido, verifiquelo."
        else:
            mensajes="El Usuario se ha Activado Satisfactoriamente."    

        #return render_template("informacion.html", data=mensajes)  
        return render_template("login2.html", data=mensajes)       


################# SE ENVIA EMAIL A CUALQUIER DESTINATARIO ####################################################################################
@app.route("/enviarMail",methods=['GET', 'POST'])
def enviarMail():
    if request.method=='POST':
        
        emaildestino = request.form["emaildestino"]
        emaildestino = emaildestino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        asunto = request.form["asunto"]
        asunto = asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        mensaje = request.form["mensaje"]
        mensaje = mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        #print("enviarEmailAOtroEmail")
        #print(emaildestino)
        #print(asunto)
        #print(mensaje)
        controlador.guardarMensaje(emaildestino, asunto, mensaje, origen)

        asuntoNotificacion="Mensaje Nuevo"
        mensajeNotificacion= "Sr. Usuario, usted ha recibido un mensaje nuevo, favor ingrese a la plataforma para ver su Email haciendo Click en la pestaña Historial de Correos. \n\n  Gracias."
        
        envioemail.enviar(emaildestino, asuntoNotificacion, mensajeNotificacion) # Este mensaje se envia como Notifcación para que el usuario ingrese a la Plataforma y desde allí vea su mensaje.

        return "Email Enviado Satisfactoriamente"

#################  HISTORIAL ENVIADOS ####################################################################################
@app.route("/historialEnviados",methods=['GET', 'POST'])
def historialEnviados():
    if request.method=='POST':
        
        respuesta=controlador.enviados(origen)
        #print(respuesta)
        return render_template("historial.html", correo=respuesta)



#################  HISTORIAL RECIBIDOS ####################################################################################
@app.route("/historialRecibidos",methods=['GET', 'POST'])
def historialRecibidos():
    if request.method=='POST':
        
        respuesta=controlador.recibidos(origen)
        #print(respuesta)
        return render_template("historial.html", correo=respuesta)


################################### ACRUALIZAR PASSWORD  #############################################################


@app.route("/actualizarPass",methods=['GET', 'POST'])
def actualizarPass():
    if request.method=='POST':
        
        password=request.form["pass"] # Recibimos la variable pass es la se utilizó en la funcion AJAX
        password=password.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        pw2=password.encode()
        pw2=hashlib.sha384(pw2).hexdigest()

        controlador.actualizarPassw(origen, pw2)
       
        return "Contraseña Actualizada Correctamente"
################################################################################################        