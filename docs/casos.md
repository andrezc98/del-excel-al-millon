# Casos reales por etapa

Investigado el 2026-09-26. Cada cita es textual de la página indicada; se
revisó abriendo la página. No hay casos publicados de startups peruanas con
estos servicios; se usan LATAM (Argentina, Chile, Colombia, Brasil, Ecuador).

## Elegidos para las láminas

| Etapa | Startup | Servicio | Dato para la lámina | Fuente |
|-------|---------|----------|---------------------|--------|
| 1 · MVP | Pomelo (fintech, Argentina, fundada 2021) | S3 Lifecycle → S3 Glacier Flexible Retrieval | "lifecycle rules that automatically transitions its objects to the low-cost S3 Glacier Flexible Retrieval storage class". Ahorro **proyectado** de 40–50% en almacenamiento | [Wayback, caso AWS 2023](https://web.archive.org/web/20250508050009/https://aws.amazon.com/solutions/case-studies/pomelo-s3-case-study/) (la URL original ya redirige) |
| 2 · Primeros clientes | Platzi (Colombia) | Amazon Aurora | "Si el nodo Máster falla, Aurora automáticamente selecciona a uno de sus servidores de sólo lectura y lo promueve a Máster sin intervención nuestra y en menos de 30 segundos." | [Blog de Platzi, 2020-10-14](https://platzi.com/blog/migramos-a-amazon-rds-aurora/) |
| 3 · Pico viral | Beat (ride-hailing, ~90% del negocio en LATAM) | ElastiCache for Redis | Cuando Colombia prohibió a su competidor principal (feb. 2020), tuvieron que escalar el cache "fast"; nueva arquitectura en 2 semanas, 22 millones de usuarios | [Wayback, caso AWS 2021](https://web.archive.org/web/20250426185659/https://aws.amazon.com/solutions/case-studies/beat-elasticache-case-study/) |
| 3 · alternativa DynamoDB | Kushki (pagos, Ecuador) | Lambda + DynamoDB | "100% serverless using AWS Lambda and Amazon DynamoDB" | [AWS Partners](https://aws.amazon.com/partners/success/kushki-grafana/) |
| 4 · Cerebro (Rekognition) | Banlek (fotos, Brasil) | Rekognition | Cada cliente encuentra solo las fotos en las que aparece; 180 millones de fotos procesadas por mes | [AWS Brasil, 2026-06-19](https://aws.amazon.com/pt/blogs/aws-brasil/como-a-banlek-transforma-o-atendimento-com-ia-generativa-e-agentes-usando-o-amazon-bedrock/) |
| 4 · Cerebro (Textract) | Condolivre (crédito para condominios, Brasil) | Textract | 80% de las revisiones de crédito validadas automáticamente; préstamos aprobados en 15 minutos | [AWS Brasil, 2024-02-14](https://aws.amazon.com/pt/blogs/aws-brasil/saiba-como-a-condolivre-inova-no-mercado-de-credito-para-condominios-com-ia-em-arquitetura-serverless-da-aws/) |
| 5 · Negocio | Defontana (ERP en la nube, Chile, opera en Perú) | S3 → Glue → Athena → QuickSight | Toda la cadena del examen en un caso; "more than 80 dashboards" | [AWS BI blog, 2023-05-25](https://aws.amazon.com/blogs/business-intelligence/defontana-provides-business-administration-solutions-to-latin-american-customers-using-amazon-quicksight/) |
| 5 · alternativa Kinesis | Pismo (fintech, Brasil) | Kinesis, SNS, SQS | De 750 millones a 6 mil millones de eventos al mes en 2023 | [AWS en español, 2023-10-11](https://aws.amazon.com/es/blogs/aws-spanish/como-pismo-procesa-200-millones-de-eventos-al-dia-utilizando-los-servicios-de-aws/) |
| Más allá del examen | Banlek (Brasil) | Amazon Bedrock (agente de soporte) | 70% menos esfuerzo de atención; el agente absorbe lo repetitivo | misma fuente que Banlek |

## Ojo antes de subirlos a una lámina

- **Beat cerró sus operaciones en Latinoamérica el 9 de noviembre de 2022**, incluido Perú. Contarlo en pasado; hasta sirve de lección: el cache escaló, el negocio no. ([LatamList](https://latamlist.com/ride-hailing-company-beat-shuts-down-operations-in-latin-america/), [Bloomberg Línea](https://www.bloomberglinea.com/english/beat-exits-argentina-mexico-and-peru-to-focus-on-european-markets/))
- **Pismo fue comprada por Visa** (cierre el 16 de enero de 2024, USD 1.000 millones en efectivo). El caso AWS es de octubre de 2023: contarlo como "cuando eran startup". ([Visa IR](https://investor.visa.com/news/news-details/2024/Visa-Completes-Acquisition-of-Pismo/default.aspx))
- **Defontana** tiene unos 20 años: es una empresa SaaS, no una startup recién nacida. Presentarlo así.
- **Pomelo**: el 40–50% es un ahorro proyectado, no medido. Decir "proyectado".
- **Banlek** cierra el hilo: la misma startup aparece en la etapa 4 (Rekognition) y en el bonus (Bedrock).

## Pistas sin verificar (no usar tal cual)

Truora (Colombia, Rekognition: solo página propia), Software Colombia (Face Liveness,
el enlace del caso redirige), Sun Finance con Bedrock (solo snippets), Mecanizou (solo
título), Rappi (EC2, RDS, ECS: página viva pero sin detalle de Multi-AZ ni fecha).
Mercado Libre (DynamoDB) y Nubank (Aurora) están verificados pero son empresas grandes;
sirven para una lámina de cierre "hacia dónde lleva esto".
