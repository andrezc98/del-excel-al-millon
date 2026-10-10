"""Public demo: the same three senses behind an HTTP API, with a hard global quota."""
import base64
import binascii
import json
import pathlib
import uuid

from botocore.exceptions import BotoCoreError, ClientError

import handler as h

AQUI = pathlib.Path(__file__).parent
MAX_TOTAL = 300
MAX_TEXTRACT = 100
MAX_IMAGEN = 1_500_000  # bytes, after base64 decoding
MAX_RESENA = 1000  # characters
# Sample images: only files that ship in lambda/muestras, so the path can never escape the folder.
MUESTRAS = {f"/muestras/{p.name}" for p in (AQUI / "muestras").glob("*.jpg")}
LISTA_MUESTRAS = json.dumps({tipo: sorted(p.split("/")[-1] for p in MUESTRAS if p.split("/")[-1].startswith(prefijo))
                             for tipo, prefijo in (("productos", "foto-"), ("facturas", "boleta-"))})


def respuesta(status, cuerpo):
    return {"statusCode": status, "headers": {"content-type": "application/json; charset=utf-8"},
            "body": json.dumps(cuerpo, ensure_ascii=False)}


def gastar_cupo(tipo):
    """Atomically count one call; returns how many are left, or None when the demo is used up."""
    textract = tipo == "facturas"
    try:
        r = h.table.update_item(
            Key={"archivo": "_cupo"},
            UpdateExpression="ADD usos :uno" + (", textract :uno" if textract else ""),
            ConditionExpression="(attribute_not_exists(usos) OR usos < :max)"
            + (" AND (attribute_not_exists(textract) OR textract < :maxt)" if textract else ""),
            ExpressionAttributeValues={":uno": 1, ":max": MAX_TOTAL, **({":maxt": MAX_TEXTRACT} if textract else {})},
            ReturnValues="UPDATED_NEW",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return None
        raise
    return MAX_TOTAL - int(r["Attributes"]["usos"])


def leer_entrada(tipo, contenido):
    """Validates the request body; returns the sense's input or raises ValueError with a user message."""
    if not isinstance(contenido, str) or not contenido.strip():
        raise ValueError("Falta el contenido.")
    if tipo == "resenas":
        if len(contenido) > MAX_RESENA:
            raise ValueError(f"La reseña puede tener hasta {MAX_RESENA} caracteres.")
        try:
            contenido.encode()
        except UnicodeEncodeError:
            raise ValueError("La reseña tiene caracteres inválidos.")
        return contenido
    # ponytail: size check on the base64 string first, so a huge body is rejected before decoding.
    if len(contenido) > MAX_IMAGEN * 4 // 3 + 4:
        raise ValueError("La imagen pesa más de 1.5 MB.")
    try:
        return {"Bytes": base64.b64decode(contenido, validate=True)}
    except binascii.Error:
        raise ValueError("La imagen no llegó bien, intenta de nuevo.")


def analizar(body):
    try:
        datos = json.loads(body or "")
    except json.JSONDecodeError:
        return respuesta(400, {"error": "Solicitud inválida."})
    tipo = datos.get("tipo") if isinstance(datos, dict) else None
    if not isinstance(tipo, str) or tipo not in h.SENTIDOS:
        return respuesta(400, {"error": "Tipo desconocido."})
    try:
        entrada = leer_entrada(tipo, datos.get("contenido"))
    except ValueError as e:
        return respuesta(400, {"error": str(e)})

    quedan = gastar_cupo(tipo)
    if quedan is None:
        return respuesta(429, {"error": "Se acabaron las pruebas de la demo. Gracias por participar."})
    try:
        resultado = h.SENTIDOS[tipo](entrada)
    except ClientError as e:
        codigo = e.response["Error"]["Code"]
        if "Throttl" in codigo or "Throughput" in codigo:
            return respuesta(429, {"error": "Hay mucha gente probando, intenta en unos segundos."})
        print(json.dumps({"tipo": tipo, "error": codigo}))
        return respuesta(400, {"error": "No pude leer ese archivo. Prueba con otra imagen."})
    except BotoCoreError as e:  # timeouts and connection errors
        print(json.dumps({"tipo": tipo, "error": type(e).__name__}))
        return respuesta(503, {"error": "El servicio tardó demasiado, intenta de nuevo."})
    h.guardar(f"web/{uuid.uuid4()}", tipo, resultado)
    return respuesta(200, {"resultado": resultado, "quedan": quedan})


def handler(event, _context):
    metodo = event["requestContext"]["http"]["method"]
    ruta = event.get("rawPath", "/")
    if metodo == "GET" and ruta == "/":
        return {"statusCode": 200, "headers": {"content-type": "text/html; charset=utf-8", "cache-control": "public, max-age=300"},
                "body": (AQUI / "index.html").read_text().replace("{{MUESTRAS}}", LISTA_MUESTRAS)}
    if metodo == "GET" and ruta in MUESTRAS:
        return {"statusCode": 200, "headers": {"content-type": "image/jpeg", "cache-control": "public, max-age=3600"},
                "isBase64Encoded": True, "body": base64.b64encode((AQUI / ruta.lstrip("/")).read_bytes()).decode()}
    if metodo == "POST" and ruta == "/analizar":
        body = event.get("body")
        if body and event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8", errors="ignore")
        return analizar(body)
    return respuesta(404, {"error": "No encontrado."})
