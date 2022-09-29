import smtplib 

from email.message import EmailMessage 


#############################################################

def enviar2():
    print("Enviando Correo...")
    message = 'Hola, este es una prueba de mensaje desde Python'    
    subject = 'prueba de correo'

    message = 'Subject: {}\n\n{}'.format(subject, message)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('vlachocorporativo@gmail.com', 'vlacho2223')

    server.sendmail('vlachocorporativo@gmail.com', 'vladimirq@hotmail.com', message)
    server.quit()

    print("Correo enviado exitosamente")




enviar2()
