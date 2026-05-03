# Documentación del dataset Xeno-canto

## eml.xml

- Nombre del dataset - `<title>`
  - Xeno-canto - Bird sounds from around the world
- Institución proveedora - `<creator><organizationName>`
  - Xeno-canto Foundation for Nature Sounds
- Cantidad de registros - `<abstract>`
  - No figura cantidad exacta. Es un subconjunto del repositorio completo disponible en xeno-canto.org
- Cobertura geográfica - `<coverage><geographicCoverage><geographicDescription>`
  - Global. Límites: Norte: 90, Sur: -90, Oeste: -180, Este: 180
- Cobertura temporal - `<formationPeriod>`
  - Desde 1900 hasta la actualidad
- Tipo de licencia - `<intellectualRights>`
  - Creative Commons Attribution Non Commercial (CC-BY-NC) 4.0 License
- Frecuencia de actualización
  - No figura frecuencia de actualización planificada. Última publicación: 2026-02-17 (`<pubDate>`)

## meta.xml

- Separador de campos - `<archive><core fieldsTerminatedBy>`
  - `,` (coma)
- Codificación de caracteres - `<archive><core encoding>`
  - UTF-8
- Archivo principal - `<core><files><location>`
  - `Occurrence.txt`
- Archivo de extensión - `<extension><files><location>`
  - `Multimedia.txt`

---

## Ejercicio 1.B — Descripción de archivos y atributos

Occurrence.txt : Este archivo contiene los registros de avistamiento y grabación de sonidos de aves alrededor del mundo.

Atributo , Descripción , Ejemplo de valor :

id , Identificador interno del registro , 12345

occurrenceID , Identificador único de la grabación en Xeno-canto , XC123456

basisOfRecord , Tipo de registro de la observación , HumanObservation

scientificName , Nombre científico completo del ave grabada , Elaenia chilensis

kingdom , Reino al que pertenece el organismo , Animalia

family , Familia taxonómica del ave , Tyrannidae

genus , Género taxonómico del ave , Elaenia

vernacularName , Nombre común del ave , Chilean Elaenia

decimalLatitude , Latitud geográfica de la grabación en grados decimales , -32.8908

decimalLongitude , Longitud geográfica de la grabación en grados decimales , -68.8272

country , País donde se realizó la grabación , Argentina

locality , Descripción del lugar de la grabación , Mendoza, cerca del río

eventDate , Fecha en que se realizó la grabación , 2021-11-15

recordedBy , Nombre del grabador , Willem-Pier Vellinga

behavior , Comportamiento del ave durante la grabación , singing

license , Licencia aplicada a la grabación , CC-BY-NC 4.0

Multimedia.txt : Este archivo vincula cada registro de Occurrence.txt con su archivo de audio correspondiente.

Atributo , Descripción , Ejemplo de valor :

id , Identificador que vincula con el registro en Occurrence.txt , 12345

identifier , URL directa al archivo de audio , https://xeno-canto.org/sounds/uploaded/...

type , Tipo de recurso multimedia , Sound

format , Formato MIME del archivo , audio/mpeg

creator , Persona que realizó la grabación , Juan Pérez

rights , Licencia aplicada al recurso multimedia , CC-BY-NC 4.0