# 🧠 What i'm doing

## Init day

Se obtuvo el dispositivo asisente, pero al parecer no detectaba la voz.
Se creó un asistente llamado _HeyJulia_ con el idioma inglés, que incluía la aplicación _AytoSanVicente_.
Esta app estaba compuesta por un _intent_ llamado 'contacto' que contenía los slots de `fax`, `telefono` y `email`. 
Se instaló este proyecto en el dispositivo a través de la herramienta **sam**, y se hizo la prueba.

El asistente detectaba bien el intent, al igual que los slots. 

Intento conectar el asistente con el repositorio, pero introduzco el repositorio en la carpeta incorrecta.

---

## Martes 1 de Octubre

Tras una reunión, el tutor JVegas informa acerca de que es al propio asistente desde la consola de snips, desde donde hay que asignar a la aplicación creada una seria de acciones, vinculando la dirección del repositorio alojado en GitHub.

Tras seguir los pasos, el asistente responde bien a los frases que se le asignan a las acciones de cuando detecta cierto intent, pero no a la de los slots.

Tras merodear y probar, pensaba que se accedía a los slots siguiendo una estructura como la siguiente o similar:

`name = intentMessage.slots[i].raw_value`

Pero no, los slots se convierten en clave en pares diccionario valor, de modo que se accede de la siguiente forma:

`slot = intentMessage.slots.nombreDelSlot`

Tras esto, el asistente funciona, pero el único fallo que le queda es que la voz tiene acento inglés y lee los números en ese idioma, lo que no nos es útil.

---

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

---

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

---

## Sábado 5 de Octubre

Insertamos en el asistente más posibles casos, al igual que se obtiene la cuenta de la consola de snips a través de la chaché: de esta forma, podemos modificar todos la cuenta de todos los actions que creemos desde el mismo fichero, ahorrándonos trabajo.
Se ha cambiado el hotword de "Hey snips" por "Pregonero", siguiento la [documentación](https://docs.snips.ai/articles/platform/wakeword/personal) de la web.
Tras realizar los pasos se ha conseguido que detecte la esta palabra para levantarse una vez de 15 intentos, por lo que no es viable.

Se procederá a intentar de nuevo la configuración en un espacio más aislado y con una mejor vocalización.

En caso de obtener los mismos resultado, se procederá a seguir un [enlace externo](https://help.github.com/en/articles/basic-writing-and-formatting-syntax#links) con el que también se puede configurar el hotword.

---

## Domingo 6 de Octubre

Se procedió a instalar en el asistente el hotword no oficial, entrenando al asistente con varias voces de distintos géneros, pero no se fue capaz de dejarlo funcionando.
Hay que probar de nuevo siguiendo todos los pasos sin tener ninguna versión de snips instalada en la tarjeta SD, pero para ello hay que realizar una copia de seguridad de el dispositivo ya funcionando.

Después, se vovlió a instalar el hot word de manera oficial, pero esta vez respondía a la secuencia _"Hey pregonera"_, aunque con un ratio bajo también. Se le subió la sensibilidad hasta 0.7, algo que no es recomendado ya que los valores deben ir entre 0.4 y 0.6, y su ratio de aciertos aumentó 3/5, pero con secuencias de golpes de la misma intensitad, el asistente también responde.
Puede valer como prototipo, pero **NO** para producción, por eso es importante hacer funcionar la manera no-oficial.

---

## Jueves 10 de Octubre

Se ha intentado configurar el modem con la tarjeta de datos pero sin conseguir que funcionase.
Hablar con JVegas para ver si está activada, o qué puede ser.

---

## Viernes 11 de Octubre

LA tarjeta sim no estaba activada. Recibo por rocket los valores para activarla, aunque aún no se ha configurado ni probado.

---

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

---

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

---

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

---

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

---

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

---

## Sábado 19 de Octubre

Después de organizar el trabajo y redactar los informes anteriores, procedo a preparar una actividad que automáticamente recopile los datos.
Para ello se ha creado un singleton que es ejecutado al iniciar el servidor, que hará de caché. Desde él, se le puede pedir recargar cierto pueblo, y en un futuro, otras acciones y labores que requieran un acceso a internet.

En cuanto a la automatización de tareas por parte del servidor, se ha encontrado que toda raspberry cuenta con `crontab`, que srive para automatizar tareas. Es muy util esto para estableer tareas que se ejecuten cada ves que se reinicie el dispositivo.

En este caso, nos interesa que se ejecute el script que realice las labores de `I'M ALIVE!` así que se establecerá la lógica de estas peticiones, y se podnrán en marcha con:

```zsh
@reboot python /home/pi/assistant-logic.py &
```

---

## Domingo 20 de Octubre

Organizo bien todos los repositorios e intento que se ejecute el script de inicio con crontable, pero no parece funcionar bien.
El script que se envia cada 5 minutos sí que funciona, y tendré que modificarlo para usarlo de controlador y dotarlo de funciones.

Me doy cuenta que **el dispositivo no responde si hacemos un reboot**.

Creo las clases que vamos a utilizar en la base de datos y también creo un frontend para el login con vuejs.
No puedo probarlo por que el servidor no permite acceder a él desde fuera, asi que mando un correo para que me lo abran.

---

## Lunes 21 de Octubre

Me abren el puerto:
65141 --> ssh
65142 --> 80 para el front
65143 --> 8082 para el core

Despliego el login con unos últimos retoques del front y ya es accesible.

## Martes 22 de Octubre
Intento instalar la [base de datos](https://tecadmin.net/install-postgresql-server-on-ubuntu/) en el servidor, para poder desplegar el core:

1. Obtengo la clave y recursos de postgres:

```zsh
$ sudo apt-get install wget ca-certificates
.... obtengo los certificados

$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
.... añado la clave de postgres

$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
.... lo configuro
```

2. Instalo el servidor:

```zsh
$ sudo apt-get update
.... actualizo los paquetes

$ sudo apt-get install postgresql postgresql-contrib
.... los instalo
```

3. Accedo a él:

```zsh
$ sudo su - postgres
.... entro con el usuario de postgres

$ psql
.... me conecto a la consola
```

Ahora procedo a crear una base de datos:

```psql
postgres@psql> CREATE DATABASE assistant;
```

Me responde: _CREATE DATABASE_ por lo que se ha creado. Podemos verla con `\l`.
Y podemos entrar a ella con:

```psql
postgres@psql> assistant
```

La creación de todas las tablas se la vamos a dejar a Kotlin, con el framework de exposed, que es muy útil.
Una vez visto esto, procedemos a desplegar el core en el servidor.

Para poder conectar nuestro core con la base de datos necesitamos un usuario y contraseña, para ello redefinimos la contraseña de postgres entrado dentro y alterando el usuario:

```psql
postgres@psql> ALTER USER postgres PASSWORD 'nueva_contraseña';
```

En el core, ponemos la configuración de la base de datos y el puerto específico, que en este caso es el 5432, el que se usa por defecto en postgres.

Lanzamos el core y vemos que funciona perfectamente haciendo la petición en local:

```zsh
$ curl localhost:8082/test/SANVICENTEDELPALACIO
{
  "status": "ALIVE",
  "places": [
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
  ]
}
```

Pero no conseguimos respuesta en `http://virtual.lab.infor.uva.es:65143/test/SANVICENTEDELPALACIO`, por lo que aún no nos han configurado la pasarela para acceder desde fuera.

Se retrasa la configuración del login y del frontend debido a que no se puede establecer la conexión.

---

## Miércoles 23 de Octubre

AL parece le había solicitado otro puerto, por lo que lo estaba indexando al que no era. Ya me lo ha cambiado al que era y sí que funciona.

Como ya ponemos comprobar la autenticación, generaremos el esquema de estilo de las respuestas y peticiones que lanzaremos:
  > **[get] url:65143/alive**
  
  - response:

  ```zsh
  {
    status : 200,
    action : "ALIVE",
    data : {
      next_action: null, # null / next action
      config: JSON # configuration for the next_action
    }
  }
  ```

  > **[post] url:65143/towns/{town}**

- **post: /towns/{town}**:
  - request:

  ```zsh
  {
    data : {
      from: String, # date time in ISO: YYYY-MM-DDTHH-MM-SS
    }
  }
  ```

  - response:

  ```zsh
  {
    status: 200,
    data : {
      content : [
        {
          address: {
            name: String,
            street: String,
            postalcode: Int,
            city: String
          },
          telephone: String,
          fax: String,
          email: String,
          urlExterna: String
        }
      ]
    }
  }
  ```

  Con el puerto ya establecido, intento una conexión entre el dispositivo y el servidor, funcionando de manera correcta, pero no consigo que se inicie automaticamente al reiniciar el dispositivo.

  Tras dos horas de intenso trabajo y búsqueda de información, acabo encontrar [por qué no funciona](https://www.digitalocean.com/community/questions/unable-to-execute-a-python-script-via-crontab-but-can-execute-it-manually-what-gives) **cron**, y es, al aprecer, que no sabe leer bien las rutas.

  También, hago que se inicie automáticamente el servicio de cron, añadiendo en `/etc/rc.local`, antes del '`exit 0`' la siguiente línea.
  
  ```
  /etc/init.d/cron start
  ```

  Procedo a utilizar el siguiente código (entrando con `$ crontab -e`), con el que finalmente sabe situarse, y funcionar:
  
  ```cron
  @reboot sleep 60; cd /home/pi/assistant.task/src/ ; /usr/bin/python /home/pi/assistant.task/src/assistant-alive.py & > logfile.txt"
  ```

---

## Jueves 24 de Octubre

Como ya funciona correctamente lo de ejecutar un script al reiniciarse, toca hacer el planning de **QUÉ se ejecuta**, y en **QUÉ orden**.

- El usuario y contraseña de la raspberry _[hidden]_. De esta forma, se podrá descifrar en el lado del servidor y servirá para todas.

  1.  [LOGIN] : intenta iniciar sesión.

      [LISTENER] : Escucha al servidor MQTT apuntando lo que salga que no sea cogido por ningun intent _(no estoy seguro de que aparezca si no hay intent)_

``` zsh
[Login] Recibe HTTP 200:  inicia [RETRIEVER]
                          inicia [SENDER]
                          inicia [ALIVE].
```

> [RETRIEVER] Recibe :(401/500) = muere. 200 = elimina los ficheros.

> [SENDER] igual que RETRIEVER.

> [ALIVE] Si recibe un 401/500, lanza [LOGIN] y muere. Si recibe un (200;ALIVE), espera y vuelve a mandar petición. Si recibe un (200;REBOOT) avisa de que se va a reiniciar y se reinicia.

Por tanto, una vez planificado, vamos a darle caña.

---

## Viernes 25 de Octubre

Vamos a ver como podemos obtener la dirección MAC del dispositivo, extrayéndolo:

```zsh
$ ifconfig | grep ether
  ether XX:XX:XX:XX:XX:XX
  ether XX:XX:XX:XX:XX:XX
```

De este modo, podemos extraerla y guardarla en un fichero.

```python
import os;
import time;

macfile = "macfile.txt"
comando = "ifconfig | grep ether > " + macfile

os.system(comando) # execute command

time.sleep(2) # wait to do more safe

with open(macfile, "r") as file: # open file to read it
    data = file.readline().replace('ether', '').replace("\t", '').replace("\n", '').replace(" ", '')

with open(macfile, "w") as file: # open the same file to save the MAC
    file.write(data)
```

De esta forma obtenemos un fichero `macfile.txt` donde tenemos registrada la dirección mac.

Las contraseña se encriptará con el número: _42,503_.

---

## Domingo 27 de Octubre

Configuramos el servicio de login de administradores por parte del sistema, de modo que introduciendo sus datos, se le creen los tokens necesarios.

> [POST] http://virtual.lab.infor.uva.es:65143/worker/login

```json
{
	"user": "admin",
	"password" : "laquesea"
}
```

Y de tal envío, recibimos la respuesta del servidor

```json
{
  "access_token": "Bearer aOs3eHPQfa3zMpRdhIyGQ2TbWSYCZgK1",
  "refresh_token": "Bearer Ddk3T6Cxyu5fmghAgBMcxNQnHkZNsmRz"
}
```

Para filtrar las URI públicas y privadas, se ha creado `src/config/GrantAccess.kt` quien permite acceso a una determinada URI en funcion del tipo de usuario que es, y ese usuario se comprueba a través del identificador asociado a sus tokens.

---

## Lunes 27 de Octubre

Se ha modificado el método de login de los dispositivos, de modo que al solicitar los tokens, se comprueba si la contraseña es corracta sin necesidad de acceder a la base de datos. Una vez comprobada, se guarda el dispositivo en la base de datos en caso de que nunca hubiese sido registrado y se añade una nueva fila a la tabla **status**, informando de qué dispositivo se ha conectado con petición de _login_, y a qué hora.

---

## Martes 28 de Octubre

Se intenta crear un servicio que obtenga todos los dispositivos si eres un trabajador, pero no se consigue hacer funcionar.
Al final el fallo es que se estaba decodificando mal la contraseña de los dispositivos y por un fallo decía que era correcta, de modo que no se llegaban a registrar. Una vez solucionado, se añaden perfectamente en el registro.

Se termina el servicio de recogida de todos los dispositivos mediante un usuario autenticado, y funciona perfectamente. De este modo, se verifica que está bien configurado el OAuth, y funcionando.

Ya tenemos el servicio rest levantado para poder mostrar los dispositivos en la web de administración, con información acerca de su ultima conexión.

> [get] http://virtual.lab.infor.uva.es:65143/worker/devices

```json
[
    {
        "device": "b8:27:eb:33:78:eb",
        "state": "LOGIN",
        "timestamp": "2019-10-29T20:02:47.435Z"
    }
]
```

## Hasta el Martes 6 de Noviembre

Se crean los servicios Web necesarios para **crear a personas**, relacionarlas con dispositivos específicos, y se desarrolla la web hasta dejar operativa una versión de prueba en la que aparecen los dispositivos registrados y a quién están asignados, al igual que una más interactiva respuesta de forma que cambia el color del dispositivo en función de cuánto tiempo lleva sin conectarse al sistema.
_(Así escrito parece poco, pero ha sido mucho trabajo._)

---

## Martes 6 de Noviembre

Hoy nos vamos a dentrar en la programación orientada a objetos en python, ya que la desconozco y con esto podríamos mejorar los servicios y expansibilidad de las funciones en la parte del dispositivo.
Se ha estado trasteando y se ha conseguido cambiar la estructura de la parte del dispositivo, de una manera más orientada a objetos, y ahora el dispositivo es capaz de iniciar sesion, conectarse al sistema y enviar ping al servidor de manera automática con tan solo conectarlo a corriente, **siempre y cuando tenga una red wifi configurada**.

---

## Miercoles 7 de Noviembre

Se ha cambiado al configuración del backend a la hora de autenticar usuarios, ya que se encontró un error a la hora de diferenciar a administradores y dispositivos por sus access tokens, al utilizar el mismo servidor OAuth. Ya ha sido reparado.

---

## Jueves 8 de Noviembre

Se ha empezado la parte del front en la que se puede añadir usuarios al sistema, pero falta refinar la especificación:

 > asignar a un usuario un CP en vez de un pueblo, y a cada pueblo sus CP, asi realizamos las acciones en funcion de CP.

 Este cambio nos hace cambiar al estructura del core y sus tablas.

---

## Domingo 10 de Noviembre

Antes de finalizar la parte de añadir usuarios se va a realizar la de añadir pueblos y su código postal, ya que es requerido en la creación de los usuarios.

Se ha añadido un script que añade todas las provincias automáticamente, y posteriormente los servicios de crear pueblos, añadir usuarios a esos pueblos, y obtener la lista completa de provincias con sus respectivos pueblos, usuarios y dispositivos asociados.

Se ha dejado todo muy bien preparado en el BACKEND para ultimar detalles en la parte del FRONTEND y dejarlo ya medio terminado.

---

## Lunes 11 de Noviembre

Se ha procedido al esbozo en papel de los posibles diseños de las páginas y botones.
Se procede a su elaboración.

---

## Hasta el 20 de Noviembre

- Se ha creado la parte del front y del back para crear usuarios, y que se asocie automaticamnete a los pueblos al establecer un codigo postal, al igual que al crear un pueblo que te lo meta en la provincia mediante su codigo postal. De esta forma es fácil e intuituvo tener todo bien organizado.

- Falta hacer mejor visible la parte del front, ya que está sin terminar. Tras muchos esbozos no se ha llegado a un diseño en claro de como va a ser la página. Almacenaré todos los esbozos para posible documentación del TFG a la hora de implementar un diseño de una página (Es de lo que dimos en IPC).

- Tras varios replanteamientos de como organizar las tareas que se van a enviar a los dispositivos, se ha llegado a un diseño que puede ser válido.
Se ha implementado  los servicios de **Tareas** que se asignan a determinados dispositivos, dejando registro de si están creadas, ya hechas, no se han podido realizar, o qué. Cada tarea tiene asociada un evento. Un **Evento** tiene un nombre, por ejemplo _REBOOT_ y un contenido, que sería _sudo reboot_ para que lo ejecute el dispositivo. Se han creado los servicios para los trabajadores, pero aún sin probarse en los dispositivos, cosa que se hará mañana.
Ha sido un tedioso trabajo estos últimos 10 días, ya que hay mucho que cambiar tanto en el dispositivo, como en el backend, como en el front.

Pasos a seguir el próximo día:

1. Probar la creación de tareas y eventos mediante Postman.
2. Mostrar de manera básica las tareas y eventos en la web.
3. Implementar la creación de tareas o eventos en la web.
4. Gestionar el muestreo de tareas y estados del dispositivo.
5. Devolver tareas al dispositivo si tiene alguna que hacer.
6. Implementar la lectura de las tareas en el dispositivo.
7. Implementar la recepcion de la respuesta de las tareas en el backend.
8. Implementar la respuesta de las tareas en el dispositivo
9. Comprobar en la web que funciona

---

## Jueves 21 de Noviembre

Tras dos horas de prueba y error, se ha conseguido testear las funciones creadas ayer con postman, y configurar para que devuelva al dispositivo las tareas que tiene pendientes.

- **[get] device/alive** : modificado para que compruebe tareas pendientes => 200: No hay, 300: devuelve lista
- **[post] worker/event** : Se le envia `{ "name" : "REBOOT", "content": "sudo reboot" }` para crear un nuevo evento.
- **[post] worker/tasks** : Se le envia `{"device" : "b8:XX:eb:XX:eb", "from": "YY-MM-DDTHH:MM:SS.MMMZ", "to" : "YY-MM-DDTHH:MM:SS.MMMZ"}` y se recibe las tareas que tiene entre esas fechas. las que no tienen el campo **"datetime"** son las que están sin completar.
- **[post] worker/task** :  Se le envía `{"device" : "b8:XX:eb:XX:eb", "event": "REBOOT"}` para crear una nueva tarea.

Se ha añadido en el dispositivo una salida para ver como se procesan las tareas al recibirlas con la petición de ALIVE: Funciona correctamente.

1. ~~Probar la creación de tareas y eventos mediante Postman.~~
2. Mostrar de manera básica las tareas y eventos en la web.
3. Implementar la creación de tareas o eventos en la web.
4. Gestionar el muestreo de tareas y estados del dispositivo.
5. ~~Devolver tareas al dispositivo si tiene alguna que hacer.~~
6. ~~Implementar la lectura de las tareas en el dispositivo.~~
7. Implementar la recepcion de la respuesta de las tareas en el backend.
8. Implementar la respuesta de las tareas en el dispositivo
9. Comprobar en la web que funciona

al que añadiremos el punto:

- 6.2. Crear el administrador de tareas en el dispositivo, en función del tipo de tarea que sea.

---

## Viernes 22 de Noviembre

Se ha planteado un supuesto práctico para que se puedan realizar las tareas nuevas y así integrar nuevas posibilidades de forma remota:

[STEP 1]
- Se le manda hacer la tarea REBOOT.
- Comprueba si tiene ./task/reboot/init.sh:

  - SÍ: lo ejecuta.

  - NO: [GET] /download/reboot

  ```json
          [{
            "name" : "init.sh",
            "content" : "sudo reboot"
          }]
  ```

  Otro ejemplo. La tarea es EXAMPLE. Comprueba si tiene ./task/example/init.sh
  
  - SÍ: lo ejecuta.
  
  - NO: [GET] /download/example

  ```json
        [{
          "name" : "init.sh",
          "content" : "sudo reboot"
        }, {
          "name" : "example.py",
          "content" : "<Python code>"
        }]
  ```

✅ El sistema para organizar las tareas está guay.

❌ El sistema para crear esas tareas sería muy laborioso.

👍🏻 Seguir ese sistema de tareas pero **que se guarden en un repo**, y que simplemente se haga un `git pull` del repo específico en el que estén las tareas subidas.

📦 Al final se ha organizado todas las acciones en carpetas, p.e. `tasks/REBOOT`, donde está `/tasks/REBOOT/init.sh`, de modo que el nombre de la carpeta es el nombre del comando, que es el **evento** que se crea desde la administración.
Dentro de `REBOOT` tenemos el archivo python `/REBOOT/Reboot.py` que es iniciado con `init.sh` que realiza el evento e informa al sistema acerca de ello.

---

## Sábado 23 de Noviembre

Se ha modificado la página de forma que deje enviar tareas a los dispositivos, ademas de mostrar cada tarjeta de dispositivo de diferente color en función de si está ejecutando una tarea en ese momento.
También deja ver qué taresa están pendientes.

---

## Domingo 24 de Noviembre

Se ha estado arregladno las vistas de Usuario y de Provinicias, que tenia botones que no mostraban bien el contenido al igual que procesar bien las tareas y toda la parte de experiencia de usuario para quefuncione bien.

Se ha estado viendo como meter gráficos en función de las estadísticas, pero como aún no tenemos recogidas las estadisiticas, se va a dejar esto apartado, aunque ya se ha hecho un diseño válido, de modo que sea la página de cada **DISPOSITIVO**, donde se puede assignar y quitar un usuario, y ver sus estadisticas del año que se desee, del mes y o del día.

No está implementado pero se ha hecho en papel todo el diseño para ver cómo mostrar los logs, los ultimos estados, y la asignación de tareas.

La idea es que esta página pueda servir para varios apartados:

- Estadisticas y acciones sobre un dispositivo especifico
- Estadisticas y acciones sobre un pueblo (codigo postal) específico.

También, se ha estado replanteando como hacer para meter al dispositivo la **contraseña del wifi** de su casa, y se ha optado que la mejor opcion es habilitar una página web para que el usuario pueda entrar, pero una página muy simple, donde pueda ver sus estadisticas, y configurar la contraseña del wifi.

---

## Martes 26 de Noviembre

Tras una reunión con el tutor se ha hablado sobre qué le falta o qué diseños podrían ser útiles:

1. Parametrización: Tener un apartado de configuración de valores generales podr defecto, que más tarde se puedan cambiar individualmente para cada dispositivo.
Entre ellos están los **periodos** de ping, lsa **direcciones** tanto de web, como de servidor, o de repositorio para actualizarse.
2. Añadir la opcion de manejar usuarios: Activos, congelados, y borrado permanente.
3. Ordenación ascendente y descendente de los dispositivos en función de su último alive, su último intent, el último evento realizado, o la ultima fecha de relación con usuarios.
4. Añadir un mapa desde donde sea más visible ver dónde están los dispositivos.

---

## Miercoles 27 de Noviembre

Se ha estado implementando el mapa.

> Se está utilizanfo leaflet ya que es de open source al igual que OpenStreetMaps para no depender de licencias en uso privado.
También se está utilizando Leaflet con ESRI, para la geolocalización reversible, de forma que podamos obtener el codigo posta, calle y toda la información a través de una latitud y longitud.

Para todo lo visto ayer, va a ser útil cambiar la obtención de los dispositivos, de forma que se obtenga el siguiente formato y así sea más facil la ordenación.
Cada atributo array tendrá un máximo de 5 elementos.

```json
[
    {
        "device": "b8:27:eb:33:78:eb",
        "last_status": [{
          "timestamp": "2019-10-29T20:02:47.435Z"
        }],
        "last_events": [{
          "event": "REBOOT",
          "timestamp": "2019-10-29T20:02:47.435Z"
        }],
        "last_intents": [{
          "timestamp": "2019-10-29T20:02:47.435Z",
          "intent": "Contacto",
          "slots": [{"slot": "Fax"}],
          "accuracy": 0.94
        }],
        "relation": {
          "name": "Alvaro Velasco",
          "nif": "1242XXXXG",
          "from": "2019-10-29T20:02:47.435Z",
          "position": {
            "latitude" : 0,
            "longitude" : 0,
            "postcode" : 47140
          }
        }
    }
]
```

---

## Jueves 28 de Noviembre

Se procede al diseño de los iconos para el mapa.
> Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
> Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>

---

## Hasta el 04 de Diciembre

Esta semana por temas de trabajo no se ha podido hacer casi nada:

- Se ha cambiado la base de datos para dar cabida a que cada localidad tenga una ubicación.
- Se ha cambiado la forma en la que se añadían localidades: ahora simplemente se da click en el mapa (pudiendo buscar con la lupa) y se añade la localidad.

Se va a proceder ahora a comprobar si afecta a la creación de nuevos usuarios: no parece afectar, al introducir el CP te sigue indicando el pueblo.

Qué hacer:

- Añadir la opción de relacionar usuarios con dispositivos.
- Mostrar los pueblos en el mapa.
- Mostrar los dispositivos en el mapa.
- Añadir la opción de acabar con la relación de los usuarion y dispositivo.

---

## Jueves 5 de Diciembre

Se ha cambiado el formato del objeto **Relacion** de modo que ahora incluye una posicion. De esta amnera ahora se han posicionado los dispositivos en su ubicación. En caso de que no tengan relación, se ponen en la costa del Atlántico, ya que así es más visual, y aparecen en otro color.
Cada dispositivo tiene un popup que muestra información sobre él, teniendo la opcion de ir a la página de estadísticas de cada uno:

 > [X] Mejorar esta opción.

La página de estadísticas ya muestra las tareas pendientes, y tiene un diseño muy robusto, pero está al 30%. Hoy se mejorará:

- Se añadirá la opcion de asignar/desasignar dispositivos (postpuesto de ayer)
- Se añadirá la opción de ordenar nuevas tareas.
- Se mostrarán las últimas tareas realizadas.

---

## Viernes 6 de Diciembre

Ya se muestran las tareas realizadas, las nuevas, y se distingue las estadisticas y 'cards' en función de:

- cargar usuario que no tiene dispositivo asociado.
- cargar usuario que tiene dispositivo asociado.
- cargar dispositivo que no está relacionado con nadie
- cargar dispositivo que sí que está relacionado.

La vista tiene una mejor visión, siendo todo más simple.
Se ha añadido la opción de poder asignar un dispositivo a un usuario desde el panel del usuario, mostrando un modal donde aparecen los dispositivos que se han actualizado más recientemente y no estén asignados a nadie, de este modo el primero que aparezca será el que está encendido a la espera de ser asignado.

Se ha encontrado un fallo:

> [x] El usuario 'PEdro Pepin' no tiene asociado ningun dispositivo. Se lo asocies o no, en la página de la lista de todos los usuarios sigue sin salir, aunque en la de las estadisticas sí que aparece.

---

## Sábado 7 de Diciembre

Se ha arreglado el fallo en la parte del backend: si encontraba varias relaciones devolvía null, y se ha sustituido por la opción de que devuelva solo la relación que esté sin terminar.

Se ha centrado al posicion de los iconos en el mapa para que apiunten exactasmente a la posición, y se han agrupado  los dispositivos en un cluster, de modo que sea una mejor visualización.

Antes de empezar con la parametrización de los campos del dispositivo vamos a dejar bien visible la página de estadísiticas de modo que sea responsible web design.

---

## Domingo 8 de Diciembre

La parte del front nos retrasa más de lo esperado, pero ya se ha dejado algo viable.
Cambiamos la visión de USERS, modificando las b-col por una tabla.

Hoy comenzamos con la parametrización, donde encontramos de momento dos posibles campos:

1. Cada cuanto tiempo se hace ping.
2. De donde se recuperan los ficheros (url del servidor)
3. Contraseña.

Lo primero es plantear cómo gestionarlo: Cuando un dispositivo inicia sesión, se le pasa un nuevo atributo junto a los tokens con datos. De esta forma, cada vez que queramos cambiarle los valores por defecto al dispositivo, tan solo hay que reiniciarlo.

❌ se ha hecho así pero sería un problema, asi que lo mejor va a ser que cambiar los datos sea un nuevo evento.

Evento **CONF** cuyo flow en el DISPOSITIVO es:

1. Le llega el evento _CONF_
2. Actualiza el fichero.
3. Se reinicia el dispositivo.

Evento **CONF** cuyo flow en el SERVIDOR es:

- Cada dispositivo tiene una configuración fija, y una pendiente. Una vez que el dispositivo ha confirmado la configuración (devuelve el identificador de la ultima configuración que se le ha mandado), se actualiza la configuración fija, se borra la pendiente, y se finaliza el evento.

  1. Generar nueva configuración pendiente (guardar)
  2. Generar evento (añadir evento)
  3. *El dispositivo marca el evento como que lo está realizando, por lo que el evento ya no está en tareas pendientes.
  4. El dispositivo cambia la configuración.
  5. Dispositivo avisa al servidor sobre que ha terminado de configurarlo (manda el timestamp).
  6. El servidor marca la configuración como no pendiente (pending = false)

Evento **CONF** en la web:

- Existe la posibilidad de modificar la configuración, de modo que se crea la nueva configuración una vez se da a GUARDAR, que es cuando se genera el evento y se crea la pendiente.
- Aparecerá la configuración normal, con la pendiente al lado en rojo en caso de que exista.
- Si se quiere eliminar, se cancela el evento.

Se ha conseguido hacer la parte del servidor y la parte del dispositivo. Para la parte del disopsitivo se ha tardado más de la cuenta por culpa de la forma de parsear los datos en python, ya que si los guardamos en formato unicode, luego no nos deja leerlos bien (esto tiene que tener alguna solucion pero no lo he encontrado).

De momento, la unica forma de que funcionase ha sido guardando en el fichero el json completo recibido como respuesta, y a la hora de usar la configuración, hay que leer el fichero y luego buscar el parametro dentro del atributo *body*, ya que si en el fichero guardabamos solo el atributo body, se guardaba en unicode.

> **DEVICE**:
[GET] URL/device/conf

Responde a un dispositivo su configuración: puede estar pendiente (si es nueva) o no (si es la vieja).

```json
{
  "device" : "El que sea",
  "timestamp" : "2019-12-08T17:10:00.000000Z",
  "pending" : true,
  "body" : {
    "sleep_sec": 15
  }
}
```

> **DEVICE** [PUT] URL/device/conf/:timestamp

Lo envia el dispositivo para avisar al servidor sobre que ha actualizado su configuración a los datos recibidos que concuerdan con el _timestamp_.

> **WORKER** [POST] URL/worker/conf

Envía la nueva configuración de un dispositivo específico:

```json
{
  "device" : "Identificador del dispositivo, o codigo postal, o 'GLOBAL'",
  "body" : {
    "sleep_sec": 15
  }
}
```

---

## Lunes 9 de Diciembre

Se termino de arreglar la aprte del dispositivo que llevaba la parametrización.

Una vez puestos se va a crear el evento de apagar el dispositivo, ya que vamos a proceder a cambiar la tarjeta SD entre varios, y así hacerlo de manera más segura.

1. Creamos el evento: ✅ OFF
2. Creamos la tarea; ✅
3. Comprobamos que funciona: ✅

Se ha cambiado el estilo de las tarjetas de dispositivo, de modo que si el último estado ha sido el de OFF indica que ha sido apagado por el administrados y el cliente aun no lo ha vuelto a encender, de modo que se muestra un color grisaceo, pudiendo distinguirlo mejor, en caso de que necesitemos contactar con el cliente para que lo encienda.

---

## Martes 10 de Diciembre

Se han editado unos nuevos iconos ya que los viejos era un poco rancios, aunque los nuevos tampoco me termina de gustar como quedan en el mapa, ya que la sondas de la voz se acoplan y no se diferencian.

Procedemos hoy a crear el apartado de la parametrización desde la web: cómo mostrarlo y organizarlo mejor.

Existe una configuración global, una por localidades, y  un máximo de dos para cada dispositivo.
Las de cada dispositivo, una tiene que estar pendiente, y la otra no. Cuando se ejecute la actualización, la pendiente dejará de estarlo, y la antigua será eliminada.

Cuando se ejecute el **evento CONF** de un dispositivo específico, se comprobará cual es más actual de los tres campos: El global, el de la localidad, o el pendiente del dispositivo. El más actual será el que se envíe al dispositivo, y será el que sustituya la configuración no-pendiente por esa otra configuración, actualizando el timestamp, que será quien haga de identificador.

Se ha puesto que al administrador, cuando pregunte por un dispositivo le mande 4 configuraciónes: la global, la de la localidad, la pandiente y la actual. El administrador podrá solicitar la de un dispositivo concreto (a+p+l+g), la de la localidad (l+g) o solo la global (g).

---

## Miercoles 11 de Diciembre

Se ha hecho el diseño de las vistas de la página de ajustes, aunque falta integrarlo con el servidor.
Tambien se ha trasteado sobre los test del  backend y se ha visto que hay que cambiar la estructura si se desea implementar, de modo que los controladores tengan acceso a un objecto DAO en vez de una llamada estática, para poder cambiar estos DAO por mocks.

Se procede a hacer las pruebas del nuevo diseño de la configuración:

- Devolver las confs y al dispositivo solo la más reciente: ✅
- Actualizar la actual cuando el dispositivo acutalice: ✅

---

## Jueves 18 de Diciembre

Tras una larga revisión se han encontrado 4 puntos críticos a mejorar que hace que cambie toda la estructura:

1. Poner inversión de dependencias.
2. INyectarlas con Koin.

Parece chungo pero ya lo he ido elaborando y ya he visto como va, eso sí, se necesaitan unas 10h para cambiarlo todo.
Empezaremos hoy temrinando de integrar la configuración de los parametros a través de la web, que lleva una semana pendiente.

Se ha integrado y se han corregido fallos a la hora de confirmar la configurción tomada.
También se ha arreglado al web de forma que muestre bien cuál es la próxima configuración pendiente, al igual que poder añadir nuevas.

---

# 📍 Milestones

- [x] Conseguir que detecte lo escuchado - **30/09/2019**
- [x] Conseguir que hable inglés - **01/10/2019**
- [x] Conseguir que hable - **01/10/2019**
- [x] Conseguir que hable castellano - **04/10/2019**
- [x] Cambiar hotword - **13/10/2019**
- [ ] Tarjeta sim en vez de wifi.
- [X] Estable el audio con fuentes de alimentación diferentes. **29/10/2019**
- [X] Crear una caché en el servidor para unas respuestas más rapidas. **19/10/2019**
- [X] Configurar servidor de la escuela. **20/10/2019**
- [X] Automatizar las peticiones `I'm alive!` del dispositivo. **23/10/2019**
- [X] Generar un usuario y contraseña para cada dispositivo. **27/10/2019**
- [X] protocolo OAuth. **28/10/2019**
- [X] DB para guardar el estado de cada dispositivo. **28/10/2019**
- [X] FRONTEND con inicio de sesión **29/12/2019**
- [X] FRONTEND para ver el estado de cada dispositivo. **3/11/2019**
- [X] BACKEND para crear usuarios **04/11/2019**
- [X] BACKEND para relacionar usuarios y dispositivos **05/11/2019**
- [X] Dispositivo: POO **06/11/2019**
- [X] Dispositivo arranca y automáticamente se inicia sesión, o se crea un usuario si no está creado, y se mantienen enviando pings cada 5 minutos. **06/11/2019**
- [X] FRONTEND para crear usuarios
- [X] FRONTEND para relacionar usuarios y dispositivos
- [ ] Servidor HTTPS
- [ ] Registro de estadísticas en la parte del dispositivo.
- [ ] Envío de estadísticas al servidor.
- [ ] Mostrar estadísticas en la web.
- [X] Servidor manda acciones al dispositivo en el cuerpo de las respuestas al `I'm alive`. _(Reboot)_ **23/11/2019**
- [X] Dispositivo realiza las acciones que le manda el servidor. _(Reboot)_ **23/11/2019**
- [ ] ~~Configurar el wifi con el diálogo~~.
- [ ] Web para configurar el wifi.
- [ ] Mensaje de bienvenida al iniciar el dispositivo.
- [ ] arranque de la máquina: que hable al encenderse.
- [ ] Conseguir diálogo simple con el dispositivo.
