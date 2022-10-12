import sqlite3


###############################################################################

def buscarUsuario(usuario,password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select * from usuarios where correo='"+usuario+"' and password= '"+password+"' and estado='1'"
    cursor.execute(consulta)
    resultado=cursor.fetchall() # DEVUELVE UNA LISTA
    #print(resultado)
    return resultado


###############################################################################

def listaUsuarios():
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select * from usuarios where estado='1' order by nombreusuario asc"
    cursor.execute(consulta)
    resultado=cursor.fetchall() # DEVUELVE UNA LISTA
    return resultado

###############################################################################

def registroUsuario(nombre,correo,password,codigo):
    try:
        db=sqlite3.connect("mensajes.s3db")
        db.row_factory=sqlite3.Row
        cursor=db.cursor()
        consulta="insert into usuarios(nombreusuario,correo,password,estado,codigovalidacion) values('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"')"
        cursor.execute(consulta)
        #resultado=cursor.fetchall() # DEVUELVE UNA LISTA
        db.commit()
        return "Usuario Registrado Satisfactoriamente. Se le ha enviado un mensaje con el Cod. de Activación"
    except:   
        return "ERROR!!! No es posible registrar el usuario debido a que el CORREO y/o NOMBRE DE USUARIO existen. Lo invitamos a modificar los valores de estos campos."
    

###############################################################################

def enviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario from mensajeria m, usuarios u where u.correo = m.id_usu_recibe and m.id_usu_envia='"+correo+"'order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall() 
    return resultado
###############################################################################


def recibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario from mensajeria m, usuarios u where u.correo = m.id_usu_envia and m.id_usu_recibe='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado
###############################################################################

def guardarMensaje(email_destino,asunto,mensaje,email_origen):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria(asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values('"+asunto+"','"+mensaje+"', DATE('now'),TIME('now'),'"+email_origen+"','"+email_destino+"','0')"
    cursor.execute(consulta)
    #resultado=cursor.fetchall() # DEVUELVE UNA LISTA
    db.commit()
    return "1"


###############################################################################

def ValidarActivarUser(codigovalidacion):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    # esta consulta actualiza el estado a 1 si el codigovalidacion corresponde
    consulta="update usuarios set estado = '1' where codigovalidacion= '"+codigovalidacion+"'"
    cursor.execute(consulta)
    db.commit()

    # en esta consulta verificamos que se haya hecho la activación.
    consulta2="select * from usuarios where codigovalidacion='"+codigovalidacion+"' and estado='1'"
    cursor.execute(consulta2)
    resultado=cursor.fetchall() # DEVUELVE UNA LISTA
    return resultado


  

#############################  ##################################################
def actualizarPassw(correo,password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    # esta consulta actualiza el estado a 1 si el codigovalidacion corresponde
    consulta="update usuarios set password = '"+password+"' where correo= '"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"
###############################################################################