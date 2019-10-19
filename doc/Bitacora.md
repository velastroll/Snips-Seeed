# 🧠 What i'm doing

## Init day

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

Tras varias pruebas, no se consigue estar en lo cierto, ya vuelve a empezar con el projecto en inglés, y seguimos con el mismo fallo. (si antes funcionaba así, ¿por qué ya no? Posible inestabilidad de snips)
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

``` Bash
tras actualizar snips: todos los servicios arriba excepto analytics
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
.... servicio snips-skill-server caido. Visto el log parece que tiene problemas de acceso a /dev/spidev0.0 , le cambio el permiso

$ sudo chmod +r /dev/spidev0.0

$ sam service start snips-skill-server
.... servicio arriba

.... pruebo el asistente y FUNCIONA!!!!
```

Tras recibir el prototipo del tutor, procedo a probar con mi asistente creado anteriormente, en castellano y con diversos slots del mismo tipo en un único intent. Resultado: funciona perfectamente.
Al parecer, el problema era ese, que nuestro prototipo tenía una version que aún no habia sido actualizada porque no había sido desplegada, y no funcionaba con el asistente, que sí que había sido actualizado.

## Sábado 5 de Octubre

Insertamos en el asistente más posibles casos, al igual que se obtiene la cuenta de la consola de snips a través de la chaché: de esta forma, podemos modificar todos la cuenta de todos los actions que creemos desde el mismo fichero, ahorrándonos trabajo.
Se ha cambiado el hotword de "Hey snips" por "Pregonero", siguiento la [documentación](https://docs.snips.ai/articles/platform/wakeword/personal) de la web.
Tras realizar los pasos se ha conseguido que detecte la esta palabra para levantarse una vez de 15 intentos, por lo que no es viable.

Se procederá a intentar de nuevo la configuración en un espacio más aislado y con una mejor vocalización.

En caso de obtener los mismos resultado, se procederá a seguir un [enlace externo](https://help.github.com/en/articles/basic-writing-and-formatting-syntax#links) con el que también se puede configurar el hotword.

## Domingo 6 de Octubre

Se procedió a instalar en el asistente el hotword no oficial, entrenando al asistente con varias voces de distintos géneros, pero no se fue capaz de dejarlo funcionando.
Hay que probar de nuevo siguiendo todos los pasos sin tener ninguna versión de snips instalada en la tarjeta SD, pero para ello hay que realizar una copia de seguridad de el dispositivo ya funcionando.

Después, se vovlió a instalar el hot word de manera oficial, pero esta vez respondía a la secuencia _"Hey pregonera"_, aunque con un ratio bajo también. Se le subió la sensibilidad hasta 0.7, algo que no es recomendado ya que los valores deben ir entre 0.4 y 0.6, y su ratio de aciertos aumentó 3/5, pero con secuencias de golpes de la misma intensitad, el asistente también responde.
Puede valer como prototipo, pero **NO** para producción, por eso es importante hacer funcionar la manera no-oficial.

## Jueves 10 de Octubre

Se ha intentado configurar el modem con la tarjeta de datos pero sin conseguir que funcionase.
Hablar con JVegas para ver si está activada, o qué puede ser.

## Viernes 11 de Octubre

LA tarjeta sim no estaba activada. Recibo por rocket los valores para activarla, aunque aún no se ha configurado ni probado.

## Domingo 13 de Octubre

Probamos a reinstalar todo en la raspberry:

1. Instalamos la versión Raspbian Stretch Lite: la versión buster no es compatible con snips ni con el customHotword.
2. Configuramos el hotword siguiendo los pasos.
3. Instalamos snips a través de sam.
4. Configuramos los valores del asistente de audio con la siguiente configuración:
**/etc/asound.conf**:

``` vim
pcm.!default {
    type asym
    playback.pcm {
        type plug
        slave.pcm "hw:1,0"
    }
    capture.pcm "multi"
}

pcm.multi {
    type plug
    slave.pcm "multiapps"
}

pcm.multiapps {
    type dsnoop
    slave.pcm "hw:1,0"
    ipc_key 666666
}
```

Hay que tener cuidado, ya que al instalar de vez en cuando la tarjeta de audio, este archivo vuelve a su configuración inicial, de modo que deja de escucharnos, por lo que hay que volver a ponerle esta configuración.

_Tip: Puede ser interesante meterle un script de modo que si al actualizar remotamente el asistente, se vuelva a esta configuración en vez de a la de por defecto._

## Martes 15 de Octubre

Se procede a crear el core del backend que irá en el servidor.

Para ello, intento acceder al servidor que nos proporciona la escuela, pero sin éxito, por lo que mando un correo a los técnicos de la escuela para ver si me lo pueden solucinar.

Mientras tanto, trabajo en local:

- Investigo cómo se puede obtener una página a través de kotlin, que es el lenguaje que voy a utilizar para crear los servicios REST, y veo que un buen parseador de datos es KSoup.
Tras un rato con KSoup, veo que tiene las opciones un poco limitadas ya que está aún muy verde y en fase de pruebas, por lo que tiendo a utiliazr JSoups, que es de dónde deriva KSoup y es compatible con Kotlin, ya que es el predecesor en Java.
- Tras realizar las peticiones, consigo obtener los datos a traves de un filtrado del documento obtenido con JSoup, de modo que hago primero un filtrado por `div`, y posteriormente por diferentes etiquetas css, como son `phone`, `address`, etc.
- Creo un servicio REST en el servidor, configurando como content negotiation a GSon.
Como alternativa a GSon tenemos JAckson, pero prefiero utilizar GSon ya que los valores nulos no los envía, algo que nos va a ser útil, mientras que Jackson los enviaría como null.
Activo el prettyPrinting de GSon que simplemente hará que si imprimimos el JSon, tendrá una mejor visualización:

``` Kotlin
   // JSon converter
    install(ContentNegotiation) {
        gson {
            setPrettyPrinting()
        }
    }
```

- y compruebo que procesa bien la página:

``` zsh
▶ curl localhost:8082/test
{
  "address": {
    "name": "Ayuntamiento de San Vicente del Palacio",
    "street": "Plaza Mayor, 1.",
    "postalcode": "47493",
    "city": "San Vicente del Palacio. Valladolid"
  },
  "telephone": "+34 983 825 006",
  "fax": "+34 983 825 056",
  "email": "ayuntamiento@sanvicentedelpalacio.gob.es",
  "urlExterna": "http://sanvicentedelpalacio.gob.es"
}
```

## Miercoles 16 de Octubre

Esto va cogiendo forma.
La parte del backend tenía una estructura muy poco limpia, por lo que el rato de la tarde de hoy lo gastamos en darle una forma más escalable a todo el sistema, de forma que creamos un controlador llamado `Retriever`, que en su construcción recibe un enum que representa a un pueblo, o servicio del que queremos recibir la información. En función del enum recibido, hace la petición y procesa toda la información.
Dentro de ese procesamiento, está preparado para poder recabar en un futuro toda la información: Ya sea sobre el ayuntamiento, o diferentes establecimientos del pueblo, estando todo muy bien preparado para una futura expansión.
Ya tendríamos una buena base.

Me pongo a investigar sobre posibles utilidades de Snips.
Veo que existe un repositorio donde se comunican con el dispositivo de manera escrita, evitando decir la palabra. Esto podría ser muy útil a la hora de poder cambiar su arquitectura y conseguir mantener una conversacion:

- Actualmente solo se puede hacer esto:
    1. Usuario: [hotword]
    2. Dispositivo: Escucha
    3. Usuario: Dice lo que sea.
    4. Dispositivo: responde y vuelve a esperar hasta que escucha el hotword.

De modo que se podría intentar que dependiendo de la información que haya dicho el usuario, el dispositivo entre en un estado en el que responda, ejecute para sí mismo [hotword] y se ponga a escuchar. Entonces, en la respuesta del dispotivo podría preguntar algo al usuario, y mantenerse escuchando a la respuesta del usuario, repitiendo el proceso y manteniendo una conversación, por ejemplo, de configuración.

Este proceso sería muy laborioso pero muy interesante.

## Jueves 17 de Octubre

Reunión con el tutor JVegas:
MAntenemos una interesante reunión en la que vamos dando nuestra visión sobre el proyecto y sobre qué puntos habría que reforzar, en cual meter mano, y cual es necesario que sea el proyecto final que debería entregar.
Al final quedamos en que sería muy bueno que a la hora de presentar el prototipo, fuese eso, un prototipo, de modo que dejase toda la base funcionando ya sea en servidor, en el dispositivo, y en la web. De esta forma, otra persona podría seguir con el TFG en otro periodo lectivo.

- Requisitos mínimos:
    1. El servidor, recopila información y la actualiza cada X tiempo, de modo que cuando le pregunta el dispoitivo para obtener una caché con todo, el servidor ya la tiene preparada.
    2. Conseguir comunicar el dispositivo con el servidor.
    3. Establecer una llamada cada 5 minutos por parte del dispositivo hacia el servidor, para saber si el estado del dispositivo.
    4. Guardar en el dispositivo diferentes estadísticas sobre su uso, que serán enviadas al servidor.
    5. Enviar las estadísticas al servidor.
    6. Cifrar las peticiones, de modo que nadie pueda falsear los datos.

- Expandiendo la base:
    1. Cuando se inicie el despositivo, que diga unas palabras: útil para saludar, y explicar sus funciones. ¿Tiene configurado el wifi? Ya conoce esa casa, no hace falta que hable.
    2. Permitir que el servidor se comunique con el dispositivo: En las respuesta al `I'm alive` se puede intentar meter qué quiere el servidor que haga el dispositivo, como reiniciarse, por ejemplo.
    3. Procesar en el dispositivo las acciones que quiere el servidor que realice, hacerlas, y avisar si se han hecho correctamente.
    4. Conseguir un diálogo Usuario/dispositivo, por básico que fuese, ya que estableceríamos una conversación un una muy buena base para la siguiente person que quiera tratar con este proyecto.
    5. Si se ha conseguido la conversación, establecer las pautas para poder configurar una conexión al wifi de una casa.

En la charla, el dispositivo no consigue levantar el servicio del audio, lo que nos da dolor de cabeza por la aparente inestabilidad del dispositivo, y una reinstalación de la tarjeta de audio en cada reinicio del dispositivo.

Al llegar a casa, vuelve a funcionar bien sin hacer nada. Se investiga acerca de las posibles causas, ya fuese por la conexión o no a internet, pero no se consigue que vuelva a fallar. El fallo, por tanto, puede haber sido debido a que la fuente de alimentación no tuviese el voltaje necesario. así que habría que probar de nuevo en un futuro, en el despacho del profesor con su fuente de alimentación.

## Viernes 18 de Octubre

Se ha intentado buscar información acerca de OAuth y para ver como funciona.

Para permitir la conexión OAuth, se necesitan 3 partes:

- Dispositivo que se quiere conectar.
- Servidor cliente, con quien se conecta el dispositivo.
- Servidor OAuth, quien mantiene todo el registro de los tokens y permite su acceso a diferentes servidores clientes.

Para enterarnos: PAra nuestro sistema ponemos un servidor OAuth, y para acceder a él y gestionar los tokens, es necesario registrarse con un servidor cliente. El servidor cliente puede ser Spotify, FB, ..., o uno propio. En este caso vamos a utilizar uno propio.

Al utilizar el framework de Ktor, nos viene la opción de configurar las credenciales OAuth, pero esta opcion que nos da es la de gestionar el servidores clientes.

Por ello, se ha buscado como establecer un módulo en nuestro proyecto de servidor Oauth, y se ha encontrado un repositorio en github. Entonces, en nuestro servidor levantaremos ambos servidores.

He estado probando la configuración, y el repo del servidor OAuth está un poco verde, por lo que habría que reajustar ciertos aspectos como cambiar como se hace la verificación de las cuentas (con los valores de nuestra BD), o la generación y borrado de tokens.

Se ha dejado medio planteado para su implantación, al igual que se ha levantado en el servidor un 'intercepteador' de peticiones, para que compruebe en ese punto si esa petición es válida o no, en funcion de la URI o el token.

Esta desarrollado aunque no funcione de momento, pero porque se dejará para más adelante, para seguir la lista de milestones por orden.

## Sábado 19 de Octubre

Después de organizar el trabajo y redactar los informes anteriores, procedo a preparar una actividad que automáticamente recopile los datos.
Para ello se ha creado un singleton que es ejecutado al iniciar el servidor, que hará de caché. Desde él, se le puede pedir recargar cierto pueblo, y en un futuro, otras acciones y labores que requieran un acceso a internet.

En cuanto a la automatización de tareas por parte del servidor, se ha encontrado que toda raspberry cuenta con `crontab`, que srive para automatizar tareas. Es muy util esto para estableer tareas que se ejecuten cada ves que se reinicie el dispositivo.

En este caso, nos interesa que se ejecute el script que realice las labores de `I'M ALIVE!` así que se establecerá la lógica de estas peticiones, y se podnrán en marcha con:

```zsh
@reboot python /home/pi/assistant-logic.py &
```

# 📍 Milestones

- [x] Conseguir que detecte lo escuchado - **30/09/2019**
- [x] Conseguir que hable inglés - **01/10/2019**
- [x] Conseguir que hable - **01/10/2019**
- [x] Conseguir que hable castellano - **04/10/2019**
- [x] Cambiar hotword - **13/10/2019**
- [ ] Tarjeta sim en vez de wifi.
- [ ] Estable el audio con fuentes de alimentación diferentes.
- [X] Crear una caché en el servidor para unas respuestas más rapidas. **19/10/2019**
- [ ] Configurar servidor de la escuela.
- [ ] Automatizar las peticiones `I'm alive!` del dispositivo.
- [ ] DB para guardar el estado de cada dispositivo.
- [ ] FRONTEND para ver el estado de cada dispositivo.
- [ ] protocolo OAuth.
- [ ] Registro de estadísticas en la parte del dispositivo.
- [ ] Envío de estadísticas al servidor.
- [ ] Mostrar estadísticas en la web.
- [ ] Mensaje de bienvenida al iniciar el dispositivo.
- [ ] Servidor manda acciones al dispositivo en el cuerpo de las respuestas al `I'm alive`. _(Reboot)_
- [ ] Dispositivo realiza las acciones que le manda el servidor. _(Reboot)_
- [ ] arranque de la máquina: que hable al encenderse.
- [ ] Conseguir diálogo simple con el dispositivo.
- [ ] Configurar el wifi con el diálogo.
