"""The startup's three senses: every file uploaded to the bucket is routed by its folder."""
import datetime
import json
import os
import urllib.parse
from decimal import Decimal

import boto3
from botocore.config import Config

s3 = boto3.client("s3")
# One attempt and short timeouts: the public demo counts one quota unit per billed call.
UNA_VEZ = Config(retries={"total_max_attempts": 1}, connect_timeout=3, read_timeout=10)
rekognition = boto3.client("rekognition", config=UNA_VEZ)
textract = boto3.client("textract", config=UNA_VEZ)
comprehend = boto3.client("comprehend", config=UNA_VEZ)
table = boto3.resource("dynamodb").Table(os.environ["TABLE"])

# Textract summary field types we keep, renamed for the demo table.
CAMPOS_FACTURA = {"VENDOR_NAME": "proveedor", "TOTAL": "total", "INVOICE_RECEIPT_DATE": "fecha"}


# Each sense takes an image/document dict ({"S3Object": ...} or {"Bytes": ...}) or, for reviews, text.
def productos(doc):
    r = rekognition.detect_labels(Image=doc, MaxLabels=5, MinConfidence=80)
    return {label["Name"]: round(label["Confidence"], 1) for label in r["Labels"]}


def facturas(doc):
    r = textract.analyze_expense(Document=doc)
    out = {}
    for d in r["ExpenseDocuments"]:
        for field in d["SummaryFields"]:
            nombre = CAMPOS_FACTURA.get(field["Type"]["Text"])
            if nombre and nombre not in out:
                out[nombre] = field.get("ValueDetection", {}).get("Text", "")
    return out


def resenas(texto):
    # ponytail: DetectSentiment caps text at 5,000 UTF-8 bytes; a review never gets close, so truncate.
    texto = texto.encode()[:4900].decode("utf-8", errors="ignore")
    r = comprehend.detect_sentiment(Text=texto, LanguageCode="es")
    return {"sentimiento": r["Sentiment"], **{k.lower(): round(v, 2) for k, v in r["SentimentScore"].items()}}


SENTIDOS = {"productos": productos, "facturas": facturas, "resenas": resenas}


def guardar(archivo, tipo, resultado):
    table.put_item(Item={
        "archivo": archivo,
        "tipo": tipo,
        # DynamoDB rejects Python floats; round-trip through JSON to get Decimals.
        "resultado": json.loads(json.dumps(resultado), parse_float=Decimal),
        "fecha": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    })


def handler(event, _context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        tipo = key.split("/", 1)[0]
        if tipo == "resenas":
            entrada = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8", errors="ignore")
        else:
            entrada = {"S3Object": {"Bucket": bucket, "Name": key}}
        resultado = SENTIDOS[tipo](entrada)
        print(json.dumps({"archivo": key, "tipo": tipo, "resultado": resultado}, ensure_ascii=False))
        guardar(key, tipo, resultado)
