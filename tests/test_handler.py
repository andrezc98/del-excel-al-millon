import io
import os
from decimal import Decimal

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ["TABLE"] = "t"
import base64, json, pathlib, sys  # noqa: E401
sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "lambda"))
import handler as h  # noqa: E402
import web  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402


class Fake:
    def __init__(self, **responses): self.__dict__.update({k: (lambda v: lambda **_: v)(v) for k, v in responses.items()})


def event(key): return {"Records": [{"s3": {"bucket": {"name": "b"}, "object": {"key": key}}}]}


def test_routes_each_folder_and_stores_decimals():
    saved = []
    h.table = Fake(); h.table.put_item = lambda Item: saved.append(Item)
    h.rekognition = Fake(detect_labels={"Labels": [{"Name": "Shoe", "Confidence": 98.76}]})
    h.textract = Fake(analyze_expense={"ExpenseDocuments": [{"SummaryFields": [
        {"Type": {"Text": "TOTAL"}, "ValueDetection": {"Text": "S/ 42.50"}},
        {"Type": {"Text": "OTHER"}, "ValueDetection": {"Text": "x"}}]}]})
    h.s3 = Fake(get_object={"Body": io.BytesIO("Llegó rápido, muy bueno".encode())})
    h.comprehend = Fake(detect_sentiment={"Sentiment": "POSITIVE", "SentimentScore": {"Positive": 0.97, "Negative": 0.01}})

    for key in ("productos/zapatilla+roja.jpg", "facturas/f1.png", "resenas/r1.txt"):
        h.handler(event(key), None)

    assert saved[0]["archivo"] == "productos/zapatilla roja.jpg"
    assert saved[0]["resultado"] == {"Shoe": Decimal("98.8")}
    assert saved[1]["resultado"] == {"total": "S/ 42.50"}
    assert saved[2]["resultado"]["sentimiento"] == "POSITIVE"
    assert all(isinstance(v, Decimal) for k, v in saved[2]["resultado"].items() if k != "sentimiento")


class Cupo:
    """In-memory stand-in for the conditional UpdateItem on the _cupo item."""
    def __init__(self, usos=0, textract=0): self.n = {"usos": usos, "textract": textract}

    def update_item(self, ExpressionAttributeValues, UpdateExpression, **_):
        v = ExpressionAttributeValues
        if self.n["usos"] >= v[":max"] or (":maxt" in v and self.n["textract"] >= v[":maxt"]):
            raise ClientError({"Error": {"Code": "ConditionalCheckFailedException"}}, "UpdateItem")
        self.n["usos"] += 1
        if "textract" in UpdateExpression: self.n["textract"] += 1
        return {"Attributes": {"usos": Decimal(self.n["usos"])}}


def post(tipo, contenido):
    r = web.handler({"requestContext": {"http": {"method": "POST"}}, "rawPath": "/analizar",
                     "body": json.dumps({"tipo": tipo, "contenido": contenido})}, None)
    return r["statusCode"], json.loads(r["body"])


def test_web_routes_counts_and_never_touches_s3():
    saved, cupo = [], Cupo()
    h.table = cupo; cupo.put_item = lambda Item: saved.append(Item)
    h.s3 = None  # any S3 call would blow up
    seen = {}
    h.rekognition = Fake(); h.rekognition.detect_labels = lambda **kw: seen.setdefault("img", kw["Image"]) and {"Labels": []}
    h.comprehend = Fake(detect_sentiment={"Sentiment": "NEGATIVE", "SentimentScore": {"Negative": 0.9}})

    assert post("productos", base64.b64encode(b"jpg").decode()) == (200, {"resultado": {}, "quedan": web.MAX_TOTAL - 1})
    assert seen["img"] == {"Bytes": b"jpg"}
    code, body = post("resenas", "Llegó tarde")
    assert code == 200 and body["resultado"]["sentimiento"] == "NEGATIVE" and body["quedan"] == web.MAX_TOTAL - 2
    assert [i["archivo"][:4] for i in saved] == ["web/", "web/"]


def test_web_rejects_bad_input_without_spending_quota():
    cupo = Cupo(); h.table = cupo
    assert post("otra", "x")[0] == 400
    assert post("resenas", "a" * (web.MAX_RESENA + 1))[0] == 400
    assert post("productos", "A" * (web.MAX_IMAGEN * 2))[0] == 400
    assert post("productos", "no es base64!")[0] == 400
    assert post("resenas", "   ")[0] == 400
    assert post([], "x")[0] == 400  # unhashable tipo used to raise TypeError
    assert post("resenas", "hola \ud800")[0] == 400  # lone surrogate used to spend quota then crash
    assert cupo.n["usos"] == 0


def test_web_quota_returns_429():
    h.table = Cupo(usos=web.MAX_TOTAL)
    assert post("resenas", "hola") == (429, {"error": "Se acabaron las pruebas de la demo. Gracias por participar."})
    h.table = Cupo(usos=0, textract=web.MAX_TEXTRACT)
    assert post("facturas", base64.b64encode(b"png").decode())[0] == 429


def test_web_service_throttle_is_429_not_500():
    h.table = Cupo(); h.table.put_item = lambda Item: None
    def lento(**_): raise ClientError({"Error": {"Code": "ThrottlingException"}}, "DetectLabels")
    h.rekognition = Fake(); h.rekognition.detect_labels = lento
    assert post("productos", base64.b64encode(b"jpg").decode())[0] == 429


def test_web_service_timeout_is_503():
    from botocore.exceptions import ReadTimeoutError
    h.table = Cupo()
    def colgado(**_): raise ReadTimeoutError(endpoint_url="x")
    h.textract = Fake(); h.textract.analyze_expense = colgado
    assert post("facturas", base64.b64encode(b"png").decode())[0] == 503


def test_web_serves_page_and_sample():
    get = lambda ruta: web.handler({"requestContext": {"http": {"method": "GET"}}, "rawPath": ruta}, None)
    pagina = get("/")["body"]
    assert "Los tres sentidos" in pagina and "{{MUESTRAS}}" not in pagina and '"productos": ["foto-0.jpg"' in pagina
    assert web.MUESTRAS >= {"/muestras/foto-0.jpg", "/muestras/boleta-0.jpg"}
    for ruta in web.MUESTRAS:
        img = get(ruta)
        assert img["isBase64Encoded"] and base64.b64decode(img["body"])[:3] == b"\xff\xd8\xff"
    assert get("/muestras/../web.py")["statusCode"] == 404
    assert get("/muestras/no-existe.jpg")["statusCode"] == 404
    assert get("/otra")["statusCode"] == 404
