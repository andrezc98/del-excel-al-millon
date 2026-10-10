# Textos de las láminas (versión final)

## Cambios (antes → después)

- 03-pregunta-pico-viral: "¿Tu base de datos aguanta el tráfico de la mañana siguiente?" → "¿Tu base de datos aguanta el tráfico de esa misma noche?" (el influencer publica a las 9 p.m.; el pico es esa noche)
- 05a-arquitectura-etapa1: "Una app en Amazon EC2 con su disco EBS; las fotos van a Amazon S3 y las viejas bajan a S3 Glacier." → "Una app en Amazon EC2 con su disco EBS. Las fotos van a Amazon S3 y las viejas, a S3 Glacier."
- 05d-arquitectura-etapa4: "Etapa 4 · La startup gana un cerebro" → "Etapa 4 · La startup estrena cerebro"
- 06a-numero-condolivre: "de las revisiones de crédito pasó a validarse automáticamente" → "de las revisiones de crédito ya se valida automáticamente"
- 06c-stats-casos: "40–50%" → "40-50%" (sin raya)
- 06c-stats-casos: "Startups de la región que ya usan estos servicios, con su dato publicado." → "Startups de la región que ya usan estos servicios, con datos públicos."
- 00b-gracias: "linkedin.com/in/POR-CONFIRMAR" → "linkedin.com/in/andreszc" (se quitó el recuadro punteado de pendiente; mismo estilo que la URL del repo: IBM Plex Mono 30 px, naranja, x=96)

El resto del texto ya sonaba natural y hablado; se dejó igual.

## Texto por lámina

## 00-portada.svg
- [ | AWS CLOUD CLUB UNI · 9 DE OCTUBRE DE 2026 | ]
- Del Excel al millón
- la memoria y el cerebro | de una startup en AWS
- Andrés Zeballos
- Solutions Architect, phData

## 00b-gracias.svg
- [ | PREGUNTAS | ]
- Gracias
- Andrés Zeballos
- Solutions Architect, phData
- Repo de la demo
- github.com/andrezc98/del-excel-al-millon
- LinkedIn
- linkedin.com/in/andreszc
- Escanea y repite la demo
- en tu cuenta de capa gratuita

## 01a-agenda-etapa1.svg
- [ | ETAPA 1 DE 5 | ]
- El MVP: la memoria
- Las fotos de productos viven en el
- disco del servidor.
- Un día, el servidor muere.
- Amazon S3
- Amazon EBS
- Amazon EFS
- S3 Glacier
- [ | EL RECORRIDO | ]
- 1
- 1
- El MVP
- S3, EBS, EFS, Glacier
- 2
- Primeros clientes
- RDS, Aurora
- 3
- Pico viral
- DynamoDB, ElastiCache
- 4
- El cerebro
- Servicios de IA
- 5
- Entender el negocio
- Kinesis, Glue, Athena, Redshift
- +
- Más allá del examen
- Amazon Bedrock

## 01b-agenda-etapa2.svg
- [ | ETAPA 2 DE 5 | ]
- Primeros clientes
- El Excel ya no aguanta y alguien
- instala PostgreSQL a mano en EC2.
- Amazon RDS
- Amazon Aurora
- [ | EL RECORRIDO | ]
- 1
- El MVP
- S3, EBS, EFS, Glacier
- 2
- 2
- Primeros clientes
- RDS, Aurora
- 3
- Pico viral
- DynamoDB, ElastiCache
- 4
- El cerebro
- Servicios de IA
- 5
- Entender el negocio
- Kinesis, Glue, Athena, Redshift
- +
- Más allá del examen
- Amazon Bedrock

## 01c-agenda-etapa3.svg
- [ | ETAPA 3 DE 5 | ]
- El pico viral
- 9:00 p.m.
- Un influencer publica tu app.
- Amazon DynamoDB
- Amazon ElastiCache
- [ | EL RECORRIDO | ]
- El MVP
- S3, EBS, EFS, Glacier
- 2
- Primeros clientes
- RDS, Aurora
- 3
- 3
- Pico viral
- DynamoDB, ElastiCache
- 4
- El cerebro
- Servicios de IA
- 5
- Entender el negocio
- Kinesis, Glue, Athena, Redshift
- +
- Más allá del examen
- Amazon Bedrock

## 01d-agenda-etapa4.svg
- [ | ETAPA 4 DE 5 | ]
- El cerebro
- Cada cliente nuevo sube la foto
- de su DNI. ¿Quién la revisa?
- Amazon Rekognition
- Amazon Textract
- Amazon Comprehend
- SageMaker AI
- [ | EL RECORRIDO | ]
- El MVP
- S3, EBS, EFS, Glacier
- Primeros clientes
- RDS, Aurora
- 3
- Pico viral
- DynamoDB, ElastiCache
- 4
- 4
- El cerebro
- Servicios de IA
- 5
- Entender el negocio
- Kinesis, Glue, Athena, Redshift
- +
- Más allá del examen
- Amazon Bedrock

## 01e-agenda-etapa5.svg
- [ | ETAPA 5 DE 5 | ]
- Entender el negocio
- El CEO pregunta qué distrito
- compra más los viernes.
- Amazon Kinesis
- AWS Glue
- Amazon Athena
- Amazon Redshift
- [ | EL RECORRIDO | ]
- El MVP
- S3, EBS, EFS, Glacier
- Primeros clientes
- RDS, Aurora
- Pico viral
- DynamoDB, ElastiCache
- 4
- El cerebro
- Servicios de IA
- 5
- 5
- Entender el negocio
- Kinesis, Glue, Athena, Redshift
- +
- Más allá del examen
- Amazon Bedrock

## 03-pregunta-pico-viral.svg
- [ | ETAPA 3 · PICO VIRAL | ]
- 9:00 p.m. Un influencer publica tu app.
- ¿Tu base de datos aguanta el tráfico de esa misma noche?

## 04-demo-flujo.svg
- [ | DEMO EN VIVO | ]
- Los tres sentidos de la startup
- Subes un archivo y, según la carpeta, una función Lambda lo manda a un servicio de IA distinto.
- evento
- Amazon S3
- bucket Archivos
- productos/
- facturas/
- resenas/
- AWS Lambda
- función Sentidos
- lee la carpeta
- y elige el servicio
- Amazon Rekognition
- productos/ | DetectLabels
- qué hay en la foto
- Amazon Textract
- facturas/ | AnalyzeExpense
- proveedor, total y fecha
- Amazon Comprehend
- resenas/ | DetectSentiment
- sentimiento de la reseña
- Amazon DynamoDB
- tabla Resultados
- tipo: productos
- tipo: facturas
- tipo: resenas

## 05a-arquitectura-etapa1.svg
- [ | ARQUITECTURA · ETAPA 1 DE 5 | ]
- Etapa 1 · El MVP sale con lo mínimo
- Una app en Amazon EC2 con su disco EBS. Las fotos van a Amazon S3 y las viejas, a S3 Glacier.
- Usuarios
- Amazon EBS
- disco de EC2
- Amazon EC2
- la app
- Amazon S3
- fotos de productos
- S3 Glacier
- ciclo de vida

## 05b-arquitectura-etapa2.svg
- [ | ARQUITECTURA · ETAPA 2 DE 5 | ]
- Etapa 2 · El Excel se jubila
- Entra Amazon Aurora: Multi-AZ por si cae una zona, réplica de lectura por si leen demasiado.
- Usuarios
- Amazon EBS
- disco de EC2
- Amazon EC2
- la app
- Amazon S3
- fotos de productos
- S3 Glacier
- ciclo de vida
- Amazon Aurora
- Multi-AZ · réplica

## 05c-arquitectura-etapa3.svg
- [ | ARQUITECTURA · ETAPA 3 DE 5 | ]
- Etapa 3 · El carrito aguanta el pico
- Entran Amazon DynamoDB on-demand para el carrito y Amazon ElastiCache delante de la base.
- Usuarios
- Amazon EBS
- disco de EC2
- Amazon EC2
- la app
- Amazon S3
- fotos de productos
- S3 Glacier
- ciclo de vida
- Amazon Aurora
- Multi-AZ · réplica
- Amazon ElastiCache
- caché de la base
- Amazon DynamoDB
- carrito, on-demand

## 05d-arquitectura-etapa4.svg
- [ | ARQUITECTURA · ETAPA 4 DE 5 | ]
- Etapa 4 · La startup estrena cerebro
- Una función AWS Lambda manda cada archivo a Rekognition, Textract o Comprehend.
- Usuarios
- Amazon EBS
- disco de EC2
- Amazon EC2
- la app
- Amazon S3
- fotos de productos
- S3 Glacier
- ciclo de vida
- Amazon Aurora
- Multi-AZ · réplica
- Amazon ElastiCache
- caché de la base
- Amazon DynamoDB
- carrito, on-demand
- AWS Lambda
- procesa la subida
- Amazon Rekognition
- valida el DNI
- Amazon Textract
- lee facturas
- Amazon Comprehend
- separa reseñas

## 05e-arquitectura-etapa5.svg
- [ | ARQUITECTURA · ETAPA 5 DE 5 | ]
- Etapa 5 · El CEO entiende su negocio
- Kinesis capta los clics, S3 los guarda, Glue los cataloga, Athena y Redshift responden, Quick Sight los muestra.
- Usuarios
- Amazon EBS
- disco de EC2
- Amazon EC2
- la app
- Amazon S3
- fotos de productos
- S3 Glacier
- ciclo de vida
- Amazon Aurora
- Multi-AZ · réplica
- Amazon ElastiCache
- caché de la base
- Amazon DynamoDB
- carrito, on-demand
- AWS Lambda
- procesa la subida
- Amazon Rekognition
- valida el DNI
- Amazon Textract
- lee facturas
- Amazon Comprehend
- separa reseñas
- Amazon Kinesis
- clics en vivo
- Amazon S3
- data lake
- AWS Glue
- catálogo y ETL
- Amazon Athena
- SQL sobre S3
- Amazon Redshift
- data warehouse
- Amazon Quick Sight
- dashboards

## 06a-numero-condolivre.svg
- [ | ETAPA 4 · CEREBRO | ]
- Condolivre, Brasil
- Crédito para condominios
- 0%
- 8%
- 16%
- 23%
- 30%
- 36%
- 41%
- 46%
- 51%
- 55%
- 59%
- 62%
- 65%
- 68%
- 70%
- 72%
- 74%
- 75%
- 76%
- 77%
- 78%
- 79%
- 80%
- de las revisiones de crédito ya se valida automáticamente
- Amazon Textract
- Fuente: Condolivre en el blog de AWS Brasil, 2024

## 06b-numero-banlek.svg
- [ | ETAPA 4 · CEREBRO | ]
- Banlek, Brasil
- Cada cliente encuentra solo las fotos en las que aparece
- 0 millones
- 19 millones
- 36 millones
- 52 millones
- 67 millones
- 80 millones
- 93 millones
- 104 millones
- 114 millones
- 124 millones
- 132 millones
- 140 millones
- 146 millones
- 152 millones
- 158 millones
- 162 millones
- 166 millones
- 169 millones
- 172 millones
- 174 millones
- 176 millones
- 177 millones
- 178 millones
- 179 millones
- 180 millones
- de fotos procesadas por mes en la plataforma
- Amazon Rekognition encuentra a cada cliente en ellas
- Fuente: Banlek en el blog de AWS Brasil, 2026

## 06c-stats-casos.svg
- [ | CASOS LATAM | ]
- Casos reales, etapa por etapa
- Startups de la región que ya usan estos servicios, con datos públicos.
- ETAPA 1 · MVP
- 40-50%
- ahorro proyectado
- en almacenamiento
- Pomelo · Argentina
- Amazon S3 Glacier
- Fuente: caso de AWS, 2023
- ETAPA 2 · PRIMEROS CLIENTES
- < 30 s
- failover automático
- a una réplica de lectura
- Platzi · Colombia
- Amazon Aurora
- Fuente: blog de Platzi, 2020
- ETAPA 4 · CEREBRO
- 15 min
- para aprobar
- un préstamo
- Condolivre · Brasil
- Textract + Lambda + S3
- Fuente: blog de AWS Brasil, 2024

## 10a-divisor-etapa1.svg
- [ | ETAPA 1 | ]
- El MVP
- S3, EBS, EFS y Glacier: dónde viven los archivos

## 10b-divisor-etapa2.svg
- [ | ETAPA 2 | ]
- Primeros clientes
- RDS y Aurora: el Excel ya no aguanta

## 10c-divisor-etapa3.svg
- [ | ETAPA 3 | ]
- Pico viral
- DynamoDB y ElastiCache: la base se ahoga

## 10d-divisor-etapa4.svg
- [ | ETAPA 4 | ]
- El cerebro
- Rekognition, Textract, Comprehend y compañía

## 10e-divisor-demo.svg
- [ | ETAPA 4 · DEMO | ]
- Demo en vivo
- Subes un archivo a S3 y la IA lo lee

## 10f-divisor-etapa5.svg
- [ | ETAPA 5 | ]
- Entender el negocio
- Kinesis, Glue, Athena y Redshift

## 10g-divisor-mas-alla.svg
- [ | FUERA DEL CLF-C02 | ]
- Más allá del examen
- Amazon Bedrock y S3 Vectors
