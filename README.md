# Del Excel al millón: la memoria y el cerebro de una startup en AWS

Charla para el AWS Cloud Club UNI, Sesión 4 de AWS Academy Cloud Fundamentals
(9 de octubre de 2026, virtual, 45–60 min).

Una startup crece en cinco etapas y en cada una entra un servicio: S3 y EBS,
RDS y Aurora, DynamoDB, IA con Rekognition y Textract, y analítica con Athena y
Redshift. De yapa, fuera del examen, un asistente con Bedrock.

## La demo: los tres sentidos de la startup

Subes un archivo a S3 y, según la carpeta, una función Lambda lo manda a un
servicio de IA distinto. El resultado queda guardado en DynamoDB.

| Carpeta | Servicio | Qué devuelve |
|---------|----------|--------------|
| `productos/` | Amazon Rekognition (DetectLabels) | Qué hay en la foto y con qué confianza |
| `facturas/` | Amazon Textract (AnalyzeExpense) | Proveedor, total y fecha de una boleta o factura |
| `resenas/` | Amazon Comprehend (DetectSentiment) | Si la reseña es positiva, negativa, neutral o mixta |

De paso, el bucket mueve las facturas a S3 Glacier a los 90 días y la tabla de
DynamoDB es on-demand: pagas por solicitud, sin capacidad reservada.

### Requisitos

- Una cuenta de AWS con AWS CLI configurada
- Node.js (para la CLI de CDK vía `npx`) y [uv](https://docs.astral.sh/uv/)
- Región `us-west-2` (Oregón). Si es la primera vez que usas CDK en esa cuenta y región:
  `npx aws-cdk@2.1143.0 bootstrap`

### Paso a paso

```bash
export AWS_PROFILE=<tu-perfil-sandbox>   # el nombre debe contener "sandbox"
uv sync
demo/run.sh deploy
demo/run.sh subir demo/muestras/resenas/mala.txt resenas
demo/run.sh subir <foto-de-un-producto>.jpg productos
demo/run.sh subir <foto-de-una-boleta>.jpg facturas
demo/run.sh ver
demo/run.sh destroy   # borra todo, incluido el bucket y la tabla
```

El script solo acepta perfiles cuyo nombre contenga `sandbox`, para no
desplegar por error en una cuenta de trabajo.

Para la boleta sirve cualquier boleta real fotografiada con el celular.

### Pruebas

```bash
uv run pytest
```

Una prueba revisa que la plantilla tenga las piezas (tabla on-demand, Lambda
arm64, regla hacia Glacier, las tres carpetas conectadas) y la otra revisa que
cada carpeta vaya al servicio correcto, con clientes de AWS simulados.
