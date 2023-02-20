
import RPi.GPIO as GPIO
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('/home/prii/proyectos/cred.json')


# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://proyecto-iot-e053a-default-rtdb.firebaseio.com/'
})


ref = db.reference('home')
print(ref.get())

print ('Ok !')



GPIO.setmode(GPIO.BOARD)

Trigger = 10
Echo = 12



GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

print("Sensor Ultrasonico")

while True:
	#crea un pulso de micro hondas 
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)
    #guarda el momento en que se envio el pulso
    inicio = time.time()

	#es un bucle que esta a la espera a que regrese el pulso, hasta eso s emantiene en 0 
    while GPIO.input(Echo) == 0:
        inicio = time.time()

	#es un bucle que se repite mientras el pin tenga voltaje sucede cuando el pin recibio el pulso enviado
	# y la variable final captura cuando fue capturado el pulso entrante
    while GPIO.input(Echo) == 1:
        final = time.time()
        
     # calculo de la distancia la velocidad del sonido es de 340 m/s
	# tiempo que transcurrio en volver el pulso
    t_transcurrido = final - inicio
    
    tiempo_local1 = time.localtime(inicio)
    #tiempo_local2 = time.localtime(final)
    #print(time.strftime("%Y-%m-%d %H:%M:%S", tiempo_local1))
    #print(time.strftime("%Y-%m-%d %H:%M:%S", tiempo_local2))
    #print(t_transcurrido)
    
    # es el calculo de la distancia   la velocidad se calcula  asi :  v=m/s
    # por lo que despejando m seria igual a m=v*s
    distancia = t_transcurrido * 34000
    # se divide por 2 porque la distancia anterior comprende ida y regreso del pulso entonces la distacia real seria la mitad
    distancia = distancia / 2
    # documentos para guardar en firebase el que se moestrara en una aplicacion android
    docGuardado = {
    'distancia': distancia,
    'fechaActualizacion': time.strftime("%Y-%m-%d %H:%M:%S", tiempo_local1)
    }
	
	#imprime el valor de la distancia
    print("distancia = %.2f cm" % distancia)
    ref.set(docGuardado)
    
    time.sleep(0.5)
    #break
