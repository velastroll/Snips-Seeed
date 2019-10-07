🧠 Pregonero's story
---

## 📦 Init day
Se obtuvo el dispositivo asisente, pero al parecer no detectaba la voz.
Se creó un asistente llamado _HeyJulia_ con el idioma inglés, que incluía la aplicación _AytoSanVicente_.
Esta app estaba compuesta por un _intent_ llamado 'contacto' que contenía los slots de `fax`, `telefono` y `email`. 
Se instaló este proyecto en el dispositivo a través de la herramienta **sam**, y se hizo la prueba.

El asistente detectaba bien el intent, al igual que los slots. 

Intento conectar el asistente con el repositorio, pero introduzco el repositorio en la carpeta incorrecta.

## Martes 1 de Octubre
Tras una reunión, el tutor JVegas informa acerca de que es al propio asistente desde la consola de snips, desde donde hay que asignar a la aplicación creada una seria de acciones, vinculando la dirección del repositorio alojado en GitHub.

Tras seguir los pasos, el asistente responde bien a los frases que se le asignan a las acciones de cuando detecta cierto intent, pero no a la de los slots.

Tras merodear y probar, pensaba que se accedía a los slots siguiendo una estructura como la siguiente o similar:
`name = intentMessage.slots[i].raw_value`
Pero no, los slots se convierten en clave en pares diccionario valor, de modo que se accede de la siguiente forma:
`slot = intentMessage.slots.nombreDelSlot`
Tras esto, el asistente funciona, pero el único fallo que le queda es que la voz tiene acento inglés y lee los números en ese idioma, lo que no nos es útil.

## Miercoles 2 de Octubre y Jueves 3 de Octubre
Procedemos a crear otro asistente nuevo, pero este que hable en castellano.
Seguimos los pasos anteriores y lo cargamos en el dispositivo.
El asistente detecta nuestras voces, pero no consigue hacer el reconocimiento de las frases: El skill snips-nlu no funciona.
_snips-nlu: natural language understanding_
Tras varios posibles casos, vemos 3 posibles causas:
- El nuevo asistente está en castellano, y anteriormente estaba en inglés, por lo que puede haber una confrontación:
Tras varias pruebas, no se consigue estar en lo cierto, ya vuelve a empezar con el projecto en inglés, y seguimos con el mismo fallo. (si antes funcionaba así, ¿por qué ya no? Posible inestabilidad de snips ⚠)
Esta opción se acaba desechando, ya que JVegas confirma que él en el pasado consiguió que hablase en castellano.
- Otra opción, podía ser la inclusión de varios slots que no siguen un tipo predefinido, si no que son custom, en un mismo intent que no interaccionen entre ellos. Pero también se desecha ya que seconsiguió hacerlo funcionar en el pasado, y probando con un solo intent de un solo slot, tampoco funciona.
- La tercera opción es que el asistente desarrollado en la consola de snips esté funcionando en una version superior que la que tenemos instalada en el dispositivo, de modo que los skills instalados no sean compatibles.
Esta opción coge sentido al mirar los logs del servicio de snips-nlu, ya que informa acerca de que el asistente necesita la v0.20.0 y se está corriendo la 0.19.0.

Volvemos a bajar la imagen de Snips-Seeed, la volvemos a cargar, la actualizamos y vemos datos positivos: Al actualizarla, la version de snips es la 0.64.0, y hace un rato teníamos la 0.63.5.

Nos metemos a ver las versiones de Snips y vemos que evidentemente acaba de salir una nueva release, y que posiblemente el asistente estuviese fallando porque antes no estaba disponible para nosotros la actualización.

Lo dejamos actualizando, ya que tarda demasiado. (+30min)

## Viernes 4 de Octubre
El tutor JVegas me informa de que ahora ya ha conseguido levantar el servicio de snips-nlu. ¡Buenas noticias!
Deja rastro de la secuencia seguida:
```
tras actualizar snips
> todos los servicios arriba excepto analytics
> $ sam reboot
.... sin snips-audio-server
> $ sam test microphone

... sin tarjeta sonido
$ sam setup-audio
.... configura tarjeta sonido
$ sam status
... todos arriba (sin analytics )
$ sam update-assistan
... asistente actualizado con los mismos avisos de version de pip
$ sam status
.... servicio snips-skill-server caído. Visto el log parece que tiene problemas de acceso a /dev/spidev0.0 , le cambio el permiso 
$ sudo chmod +r /dev/spidev0.0
$ sam service start snips-skill-server
.... servicio arriba
pruebo el asistente y FUNCIONA!!!!
```

Tras recibir el prototipo del tutor, procedo a probar con mi asistente creado anteriormente, en castellano y con diversos slots del mismo tipo en un único intent. Resultado: funciona perfectamente.
Al parecer, el problema era ese, que nuestro prototipo tenía una version que aún no habia sido actualizada porque no había sido desplegada, y no funcionaba con el asistente, que sí que había sido actualizado.

## Sábado 5 de Octubre
Insertamos en el asistente más posibles casos, al igual que se obtiene la cuenta de la consola de snips a través de la chaché: de esta forma, podemos modificar todos la cuenta de todos los actions que creemos desde el mismo fichero, ahorrándonos trabajo.
Se ha cambiado el hotword de "Hey snips" por "Pregonero", siguiento la [documentación](https://docs.snips.ai/articles/platform/wakeword/personal) de la web.
Tras realizar los pasos se ha conseguido que detecte la esta palabra para levantarse una vez de 15 intentos, por lo que no es viable.

Se procederá a intentar de nuevo la configuración en un espacio más aislado y con una mejor vocalización.

En caso de obtener los mismos resultado, se procederá a seguir un [enlace externo](https://help.github.com/en/articles/basic-writing-and-formatting-syntax#links) con el que también se puede configurar el hotword.


📍 Milestones:
---
 
 - [x] Conseguir que detecte lo escuchado - **30/09/2019**
 - [x] Conseguir que hable inglés - **01/10/2019**
 - [x] Conseguir que hable - **01/10/2019**
 - [x] Conseguir que hable castellano - **04/10/2019**
 - [x] Cambiar hotword - *06/10/2019** _Ratio de acierto bajo_
 - [ ] Tarjeta sim en vez de wifi -
