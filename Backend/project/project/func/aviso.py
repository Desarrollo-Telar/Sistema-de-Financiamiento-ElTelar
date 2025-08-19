from gtts import gTTS

texto = """
Aviso a nuestros usuarios – Inversiones Integrales El Telar
Estimados usuarios,
Es un gusto notificarles que hemos simplificado la forma de presentar su comprobante de pago.
Ahora, a través de los links que se les proporciona, podrán subir su boleta de manera rápida y segura.
Al momento de registrar su comprobante, por favor tome en cuenta lo siguiente:
1.	Adjuntar la imagen de su boleta de pago.
2.	Si su pago fue realizado en Banrural:
	Marque la casilla correspondiente.
	Ingrese el número de referencia de su boleta.
3.	Si su pago fue realizado en otro banco:
	No marque la casilla.
    Solo adjunte la boleta.
Una vez completado este proceso, su comprobante quedará registrado y en validación, lo que nos permitirá procesar su pago sin retrasos.
Nota importante:
Cada link proporcionado corresponde a sus créditos en específico.
En caso de que cuente con más de un crédito con nosotros, se le estarán proporcionando los links correspondientes para cada uno.
¡Gracias por su confianza en Inversiones Integrales El Telar!

"""

# Generar audio
tts = gTTS(text=texto, lang="es")
tts.save("aviso_telar.mp3")
print("✅ Audio generado: aviso_telar.mp3")
