# Preguntas tipo Cloud Practitioner (cierre de la charla)

Dos preguntas al final, una de "memoria" y una de "cerebro". Todas las opciones
están en la lista de servicios del CLF-C02
(https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/clf-02-in-scope-services.html).
La tercera queda de reserva por si sobra tiempo o para la ronda de preguntas.

## Pregunta 1 · Memoria

La app de la startup tiene un carrito de compras. Casi todo el día el tráfico es
bajo, pero cuando un influencer publica la app, las solicitudes se multiplican
en minutos. El equipo es pequeño y no quiere planificar capacidad ni
administrar servidores de base de datos. ¿Qué opción cumple mejor?

- A) Amazon RDS for PostgreSQL en una instancia fija
- B) Amazon DynamoDB en modo on-demand
- C) Amazon Redshift
- D) Una base de datos instalada por el equipo en Amazon EC2

**Respuesta: B.** DynamoDB on-demand escala solo, cobra por solicitud y no
requiere planificar capacidad.
- A: es gestionada, pero una instancia fija no absorbe el pico sin que alguien la redimensione.
- C: Redshift es para analítica (data warehouse), no para el carrito de una app.
- D: el equipo tendría que administrar el servidor, lo contrario de lo que pide.

Fuente: "automatically scales to accommodate the most demanding workloads without
capacity planning ... you only pay for the throughput you actually use."
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html

## Pregunta 2 · Cerebro

Los clientes suben fotos de sus boletas para pedir reembolsos. La startup quiere
extraer automáticamente el nombre del proveedor, la fecha y el total, sin
entrenar un modelo propio. ¿Qué servicio debe usar?

- A) Amazon Rekognition
- B) Amazon Textract
- C) Amazon Comprehend
- D) Amazon SageMaker AI

**Respuesta: B.** Textract extrae datos de facturas y boletas (proveedor, fecha,
total) sin plantillas. Es exactamente lo que hizo la demo con la boleta de la
Bodega Doña Rosa.
- A: Rekognition entiende imágenes (objetos, rostros), no lee campos de un documento.
- C: Comprehend analiza texto que ya tienes (sentimiento, entidades); no lee imágenes.
- D: SageMaker AI sirve para entrenar modelos propios, justo lo que el enunciado descarta.

Fuente: "Amazon Textract extracts relevant data such as vendor and receiver contact
information, from almost any invoice or receipt without the need for any templates
or configuration." https://docs.aws.amazon.com/textract/latest/dg/invoices-receipts.html

## Reserva · Memoria

La startup guarda las boletas escaneadas. Se consultan durante el primer mes y
casi nunca después, pero deben conservarse varios años al menor costo posible,
sin que nadie las mueva a mano. ¿Qué debe configurar?

- A) Snapshots diarios de Amazon EBS
- B) Una regla de ciclo de vida de Amazon S3 que pase los objetos a S3 Glacier
- C) Amazon EFS en la clase Standard
- D) Amazon ElastiCache

**Respuesta: B.** Una regla de ciclo de vida mueve los objetos a una clase de
archivo de S3 Glacier automáticamente. La demo lo hace con la carpeta
`facturas/` a los 90 días.
- A: los snapshots respaldan discos, no archivan documentos por antigüedad.
- C: EFS es un sistema de archivos compartido, más caro para guardar años.
- D: ElastiCache es memoria para respuestas rápidas, no archivo.

Fuente: "By using an S3 Lifecycle configuration, you can transition objects to the
S3 Glacier Flexible Retrieval or S3 Glacier Deep Archive storage classes for archiving."
https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html
