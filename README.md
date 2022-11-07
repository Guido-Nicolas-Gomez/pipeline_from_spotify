# Data pipeline from Spotify
El script __main.py__ obtiene las canciones de spotify escuchadas desde el día de ayer por un determinado usuario y las guarda en una base de datos.
Tambien se cuenta con el jupyter notebook __notebooks.ipynb__, donde el mismo script y las funciones de __tools.py__ se encuentran expresadas en bloques.

## Modulos y Paquetes
A continuacion se listan los paquetes utilizados:
- __requests__: Para las solicitudes de datos a Spotify
- __datetime__: Para filtrar los registros segun una fecha especifica (a partir de ayer)
- __pandas__: Para la manipulacion, limpieza y transformacion de los datos
- __sqlalchemy__: Para la conexion a la base de datos (sqlite3)
- __pytz__: Para configurar la zona horaria segun corresponda

## Variables de entorno
__DATA_BASE_LOCATION__: Indica la ubicacion de la base de datos
__USER_ID__: será el nombre de usuario del cual desea extraer la informacion
__TOKEN__: Es el toke de seguridad el cual se puede generar en el siguiente [enlace](https://developer.spotify.com/console/get-recently-played/)

## Extraccion
La solicitud de los datos se realiza al url "https://api.spotify.com/v1/me/player/recently-played", el cual acepta hasta tres parametros, el limite de registros y el antes y despues de unas fechas determinadas.
Los datos son obtenidos en un formato json, los cuales posteriormentes son convertidos en un objeto DataFrame de pandas pero solo con los campos necesarios.

## Transformacion y validación
Se realizan las transformaciones de los campos de fecha al formato necesario para ser cargados en la base de datos, a su vez se realizan una serie de validaciones, como que el dataset no este vacío, que no haya valores nulos o que las fechas obtenidas sean las solicitadas (desde ayer).

## Carga
La carga de los datos se realiza mediante la utilizacion del modulo sqlalchemy, donde se crea un objeto __Played_list__, el cual representa un registro en la base datos y contiene el schema de la misma para su carga. La carga se realiza registro a registro en la base de datos __my_tracks.db__ y finalmente se realiza el commit de los mismos.
