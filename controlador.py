import sqlite3


###############################################################################

def buscarUsuario(usuario,password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select * from usuarios where correo='"+usuario+"' and password= '"+password+"' and estado='1'"
    cursor.execute(consulta)
    resultado=cursor.fetchall() # DEVUELVE UNA LISTA
    return resultado

###############################################################################

def registroUsuario(nombre,correo,password,codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into usuarios(nombreusuario,correo,password,estado,codigovalidacion) values('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"')"
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


  

###############################################################################

###############################################################################