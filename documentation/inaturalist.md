# ------------------ Ejaercicio 1 A ------------------

Nombre del dataset: iNaturalist Research-grade Observations.

Institución proveedora: iNaturalist.

Cantidad de registros: 53.854 .

Cobertura geográfica: Límites: Norte: 90 , Sur: -90, Oeste: -180, Este: -180.

Cobertura temporal: Desde el 17/8/1768 hasta el 16/2/2026.

Separador de campos: "," (coma).

Codificación de caracteres: UTF-8.

Tipo de licencia: Creative Commons Attribution-NonCommercial License (CC BY-NC 4.0).

Frecuencia de actualización: Semanal.

# ------------------ Ejaercicio 1 B ------------------

Ocurrence.txt : Este archivo contiene los registros de las observaciones biológicas.

Atributo , Descripción , Ejemplo de Valor :

id / occurrenceID , Identificador único numérico de la observación en iNaturalist , 1771282821

basisOfRecord , una observacion que hace un investigador basandose en la evidencia , HumanObservation

eventDate , La fecha y hora exacta en la que se realizó la observación , 2024-05-12T14:30:00Z

scientificName , El nombre científico completo del organismo observado , Danaus plexippus

kingdom , Reino al que pertenece el organismo , Animalia

decimalLatitude , La latitud geográfica de la observación , -34.6037

decimalLongitude , La longitud geográfica de la observación , -58.3816

taxonRank , La categoría del nombre identificado , "species, genus, family"

recordedBy , El nombre o seudónimo del usuario de iNaturalist que realizó la observación , usuario_naturaleza123

Multimedia.txt : Este archivo vincula las observaciones de Ocurrence.txt con los archivos multimedia (fotos o sonidos) que sirven como evidencia.

Atributo , Descripción , Ejemplo de Valor :

id , El identificador de la ocurrencia (vincula este medio con el registro en Occurrence.txt) , 1771282821

type , Indica si el recurso es una imagen fija, un video o un sonido , "StillImage, Sound"

format , El tipo de formato MIME del archivo digital , "image/jpeg, audio/mpeg"

identifier , La URL directa donde se encuentra alojado el archivo original , https://inaturalist-open-data.s3.../original.jpg

references,Página web de referencia de la observación en el portal de iNaturalist , https://www.inaturalist.org/photos/12345

license , La licencia específica aplicada a ese recurso multimedia , CC-BY-NC 4.0

creator , La persona que tomó la fotografía o grabó el sonido , Juan Pérez
