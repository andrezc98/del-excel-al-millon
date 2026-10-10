# Guion: Del Excel al millón (45–60 min)

Regla de oro: cada etapa es **problema → servicio → palabra clave del examen**.

## Apertura (0–5 min)
1. **Portada.** Preséntate: Arequipa, Solutions Architect en phData, Golden Jacket.
2. **Día 1 contra día 500.** "Día 1: una laptop y un Excel. Día 500: un millón de usuarios. ¿Qué servicio entra en cada momento?"
   Aviso de mapa: **su Dominio 4 del curso = Dominio 3 del examen** (Tecnología y servicios). El Dominio 4 del examen es facturación y soporte.

## Etapa 1 · El MVP, la memoria (5–14 min)
3. **Divisor 1 · Agenda.** "Las fotos viven en el disco del servidor. Un día el servidor muere."
4. **Arquitectura 1.**
   - **EBS**: el disco de *una* instancia EC2.
   - **EFS**: archivos compartidos entre varios servidores.
   - **S3**: objetos, ilimitado, pagas lo que guardas. Aquí van las fotos.
   - **Glacier + ciclo de vida**: lo que casi no se lee baja de clase solo.
   - Palabra clave: *"durable, ilimitado, objetos" = S3*.

## Etapa 2 · Primeros clientes (14–23 min)
5. **Divisor 2 · Agenda.** "El Excel ya no aguanta; alguien instala PostgreSQL a mano en EC2."
6. **Arquitectura 2.**
   - **RDS**: base relacional administrada (AWS parcha, respalda).
   - **Aurora**: la versión de AWS, más rápida y con failover automático. Caso **Platzi**: failover en menos de 30 s.
   - **Multi-AZ** = cuando se cae una zona. **Read replicas** = cuando leen demasiado.
   - Responsabilidad compartida: en RDS el parche del motor es de AWS; tus datos y accesos, tuyos.

## Etapa 3 · Pico viral (23–31 min)
7. **Divisor 3 · Pregunta.** Deja la pregunta en el aire: "9 p.m., un influencer publica tu app. ¿Tu base aguanta?"
8. **Agenda · Arquitectura 3.**
   - **DynamoDB on-demand**: NoSQL, sin servidores, escala solo, pagas por solicitud. Ideal para carrito y sesiones.
   - **ElastiCache**: memoria rápida *delante* de la base para respuestas repetidas. Caché ≠ base de datos.
   - DocumentDB (documentos) y Neptune (grafos) en una línea.

## Etapa 4 · El cerebro (31–41 min)
9. **Divisor 4 · Agenda · Arquitectura 4.**
   - **Rekognition** = imágenes. **Textract** = documentos. **Comprehend** = sentimiento del texto.
   - Translate, Polly, Transcribe, Lex: soporte. **SageMaker AI**: cuando el modelo tiene que ser tuyo. **Amazon Q**: para el equipo.
   - Idea clave: *servicios de IA ya entrenados, no necesitas saber de machine learning*.
10. **Número Banlek.** Lee el dato de la lámina.

## Demo (dentro de la etapa 4)
11. **Divisor demo · Flujo.** "Subo un archivo a S3; según la carpeta, Lambda lo manda a un servicio distinto y el resultado queda en DynamoDB."
12. **Pruébalo ahora (QR).** Dales 2–3 min. Pide que prueben las tres pestañas y los botones 🎲.
    - Momento divertido: **"Reseña al azar"** hasta que salga el sarcasmo ("Gracias por nada") → Comprehend dice POSITIVA. *La IA no entiende ironía.*
    - El gato en el teclado: Rekognition ve la laptop, no el gato.
    - Si alguien pregunta: límite 300 pruebas para todos, no guardamos archivos.
    - Plan B: si la red falla, `demo/run.sh subir` en terminal y `demo/run.sh ver`.

## Etapa 5 · Entender el negocio (41–47 min)
13. **Divisor 5 · Agenda · Arquitectura 5.** "El CEO pregunta qué distrito compra más los viernes."
    - Kinesis (datos en tiempo real) → **S3 como data lake** → **Glue** (cataloga y prepara) → **Athena** (SQL directo sobre S3, pagas por consulta) o **Redshift** (data warehouse, consultas frecuentes y pesadas) → **QuickSight** (dashboards).
    - Palabra clave: *"consultas ocasionales sobre S3" = Athena; "data warehouse" = Redshift*.
14. **Número Condolivre · Casos LATAM.** Un caso por etapa, rápido. "No encontramos casos peruanos publicados: ahí hay una oportunidad para ustedes."

## Más allá del examen (47–52 min)
15. **Divisor · Bedrock.** Asistente de soporte con **Amazon Bedrock + Knowledge Base sobre S3 Vectors**. Dilo claro: *no entra al CLF-C02, entra al AI Practitioner.*

## Cierre (52–60 min)
16. **¿Qué servicio elijo?** "Primero pregúntate qué tipo de dato tienes y cómo lo usas." Que le tomen captura.
17. **Pregunta 1 → Respuesta.** Dales 20 s para votar en el chat. Respuesta **B, DynamoDB on-demand**.
18. **Pregunta 2 → Respuesta.** Respuesta **B, Textract**: el especializado en boletas, te da los campos.
19. **QR otra vez** para los que llegaron tarde.
20. **Gracias.** Repo de la demo + LinkedIn **linkedin.com/in/andreszc**. Preguntas.

## Antes de empezar
- `demo/run.sh reiniciar` (cupo a 300).
- Abre `demo.builtbyandres.com` en tu celular y prueba una vez cada pestaña.
- Después de la charla: `demo/run.sh destroy` y borrar los dos CNAME en Cloudflare.
