"""Build the extra slides in the SBG dark theme (same look as slides/visuals-sbg).

  uv run --with qrcode python slides/nuevas/build.py

Icons are lifted from slides/visuals-sbg; API Gateway and Bedrock come from the AWS icon pack
in ../.claude/skills/talk-visuals. Writes slides/nuevas/*.svg.
"""
import glob
import pathlib
import re

import qrcode

HERE = pathlib.Path(__file__).resolve().parent
SBG = HERE.parent / "visuals-sbg"
PACK = (HERE.parents[2] / ".claude/skills/talk-visuals/assets/aws-icons/pkg/Architecture-Service-Icons_07312026")

BG, CARD, GRID, MUTED = "#161d26", "#1f2731", "#3e434c", "#b8bec8"
ORANGE, PURPLE, MAGENTA, BLUE, GREEN = "#ff9900", "#ad5cff", "#ff57e9", "#42b4ff", "#00e582"
MONO = "'IBM Plex Mono',Menlo,ui-monospace,monospace"

# ---------- icons ----------
ICONS = {}
for f in sorted(glob.glob(str(SBG / "*.svg"))):
    s = open(f).read()
    for m in re.finditer(r'<svg x="[^"]*" y="[^"]*" width="[^"]*" height="[^"]*" viewBox="0 0 80 80">(.*?)</svg>', s, re.S):
        n = re.search(r">([^<]+)</text>", s[m.end():m.end() + 400])
        if n:
            ICONS.setdefault(n.group(1), m.group(1).replace("url(#tv-grad)", ORANGE))


def pack(rel):
    s = (PACK / rel).read_text()
    body = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body)
    body = re.sub(r'(<g id="Icon-Architecture-BG[^"]*" )fill="#[0-9A-Fa-f]+"', rf'\1fill="{ORANGE}"', body)
    body = re.sub(r'(<rect id="Rectangle"[^>]*)fill="#[0-9A-Fa-f]+"', rf'\1fill="{ORANGE}"', body)
    return body.replace("#FFFFFF", BG).replace('fill="white"', f'fill="{BG}"')


ICONS["Amazon API Gateway"] = pack("Arch_Networking-Content-Delivery/64/Arch_Amazon-API-Gateway_64.svg")
ICONS["Amazon Bedrock"] = pack("Arch_Artificial-Intelligence/64/Arch_Amazon-Bedrock_64.svg")
# ponytail: self-drawn phone, the pack has no "user device" service icon
ICONS["phone"] = (f'<rect width="80" height="80" fill="{ORANGE}"/><rect x="26" y="12" width="28" height="56" rx="5" '
                  f'fill="none" stroke="{BG}" stroke-width="3.5"/><line x1="36" y1="60" x2="44" y2="60" stroke="{BG}" '
                  f'stroke-width="3.5" stroke-linecap="round"/>')


def icon(name, x, y, size=80):
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 80 80">{ICONS[name]}</svg>'


# ---------- page chrome ----------
def page(title, body, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" font-family="'Public Sans', 'Helvetica Neue', Arial, sans-serif">
<title>{title}</title>
<defs><pattern id="sbg-grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0V60H0" fill="none" stroke="{GRID}" stroke-width="2"/></pattern></defs>
<style>@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=block');
.h{{font-size:60px;fill:#fff;font-family:{MONO};font-weight:500}}
.k{{font:26px {MONO};fill:#fff}}
.sub{{font-size:30px;fill:{MUTED}}}
.big{{font-size:40px;font-weight:600;fill:#fff}}
.t{{font-size:32px;font-weight:600;fill:#fff}}
.c{{font-size:26px;fill:{MUTED}}}
.m{{font-family:{MONO};font-weight:500}}
.card{{fill:{CARD};stroke:{GRID};stroke-width:1.5}}
{extra_css}</style>
<rect width="1920" height="1080" fill="{BG}"/><rect width="1920" height="1080" fill="url(#sbg-grid)"/><g><rect x="1800" y="0" width="60" height="60" fill="{ORANGE}"/><rect x="1860" y="0" width="60" height="60" fill="{BLUE}"/><rect x="1860" y="60" width="60" height="60" fill="{MAGENTA}"/></g>
{body}
</svg>
"""


def kicker(text, x=96, y=72, bracket=ORANGE):
    return f'<text class="k" x="{x}" y="{y}"><tspan fill="{bracket}">[</tspan>{text}<tspan fill="{bracket}">]</tspan></text>'


def lines(cls, x, y, rows, dy, extra=""):
    return "".join(f'<text class="{cls}" x="{x}" y="{y + i * dy}"{extra}>{r}</text>' for i, r in enumerate(rows))


# ---------- 02 día 1 contra día 500 ----------
def dia1():
    b = [kicker("EL VIAJE"), '<text class="h" x="96" y="142">Día 1 contra día 500</text>']
    # left: one block
    b.append('<rect class="card" x="96" y="220" width="804" height="500" rx="24"/>')
    b.append(f'<text class="m" x="144" y="310" font-size="44" fill="{ORANGE}">Día 1</text>')
    b.append(f'<rect x="144" y="360" width="60" height="60" fill="{ORANGE}"/>')
    b.append(lines("big", 144, 520, ["Una laptop y un Excel."], 0))
    b.append(lines("c", 144, 580, ["Tú, tu idea y una hoja de cálculo", "que ya pesa demasiado."], 38))
    # arrow
    b.append(f'<path d="M920 470 H1000 M980 446 L1004 470 L980 494" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-linecap="square"/>')
    # right: many blocks
    b.append('<rect class="card" x="1020" y="220" width="804" height="500" rx="24"/>')
    b.append(f'<text class="m" x="1068" y="310" font-size="44" fill="{GREEN}">Día 500</text>')
    cols = [ORANGE, PURPLE, MAGENTA, BLUE, GREEN]
    pat = ["1101101011", "0111011110"]
    for r, row in enumerate(pat):
        for c, on in enumerate(row):
            if on == "1":
                b.append(f'<rect x="{1068 + c * 60}" y="{360 + r * 60}" width="60" height="60" fill="{cols[(r * 3 + c) % 5]}"/>')
    b.append(lines("big", 1068, 580, ["Un millón de usuarios."], 0))
    b.append(lines("c", 1068, 640, ["Y el Excel ya no aguanta."], 0))
    # map callout
    b.append(f'<rect x="96" y="780" width="1728" height="200" rx="16" fill="#2a2418" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="10 8"/>')
    b.append(kicker("MAPA", 136, 836))
    b.append(f'<text class="t" x="136" y="896">Lo que en el curso llaman <tspan fill="{ORANGE}">Dominio 4</tspan>, en el examen CLF-C02 es el <tspan fill="{ORANGE}">Dominio 3</tspan> (Tecnología y servicios).</text>')
    b.append('<text class="c" x="136" y="944">El Dominio 4 del examen es facturación, precios y soporte.</text>')
    return page("Día 1 contra día 500", "\n".join(b))


# ---------- 04b pruébalo ----------
def qr_paths(url, x, y, size):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(url)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    d = "".join(f"M{c} {r}h1v1h-1z" for r, row in enumerate(m) for c, v in enumerate(row) if v)
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">'
            f'<path d="{d}" fill="{BG}"/></svg>')


def pruebalo():
    url = "https://demo.builtbyandres.com"
    b = [kicker("DEMO EN VIVO"), '<text class="h" x="96" y="142">Pruébalo ahora</text>',
         '<text class="sub" x="96" y="200">Abre la cámara de tu celular y escanea el código.</text>']
    b.append(f'<text class="m" x="96" y="330" font-size="52" fill="{ORANGE}">demo.builtbyandres.com</text>')
    b.append(lines("big", 96, 440, ["Sube una foto, una boleta o una reseña", "y mira qué responde cada servicio."], 56))
    # note
    b.append(f'<rect x="96" y="560" width="1060" height="150" rx="16" fill="#2a2418" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="10 8"/>')
    b.append(f'<text class="t" x="136" y="622">Límite compartido: <tspan fill="{ORANGE}">300 pruebas</tspan> para todo el público.</text>')
    b.append('<text class="c" x="136" y="672">No guardamos tu archivo, solo el resultado.</text>')
    # QR card
    b.append('<rect x="1260" y="96" width="564" height="640" rx="24" fill="#ffffff"/>')
    b.append(qr_paths(url, 1312, 148, 460))
    b.append(f'<text x="1542" y="680" text-anchor="middle" font-size="30" font-weight="600" fill="{BG}">Escanea y pruébalo</text>')
    # flow
    steps = [("phone", "Tu celular", None), ("Amazon API Gateway", "API Gateway", None), ("AWS Lambda", "AWS Lambda", None),
             (["Amazon Rekognition", "Amazon Textract", "Amazon Comprehend"], "Rekognition,", "Textract o Comprehend"),
             ("Amazon DynamoDB", "DynamoDB", "guarda el resultado")]
    xs = [96, 446, 796, 1146, 1546]
    w = [290, 290, 290, 340, 278]
    for (ic, t, c), x, ww in zip(steps, xs, w):
        b.append(f'<rect class="card" x="{x}" y="800" width="{ww}" height="200" rx="20"/>')
        if isinstance(ic, list):
            for i, name in enumerate(ic):
                b.append(icon(name, x + 28 + i * 76, 828, 64))
        else:
            b.append(icon(ic, x + 28, 828, 64))
        b.append(f'<text class="t" x="{x + 28}" y="{946 if c else 956}" font-size="28">{t}</text>')
        if c:
            b.append(f'<text class="c" x="{x + 28}" y="980" font-size="22">{c}</text>')
    for x in [386, 736, 1086, 1486]:
        b.append(f'<path d="M{x + 12} 900 H{x + 48} M{x + 38} 890 L{x + 50} 900 L{x + 38} 910" fill="none" stroke="{ORANGE}" stroke-width="4"/>')
    return page("Pruébalo ahora", "\n".join(b))


# ---------- 11 bedrock ----------
def bedrock():
    b = [f'<rect x="96" y="40" width="430" height="48" fill="{GREEN}"/>',
         f'<text class="m" x="116" y="74" font-size="26" fill="{BG}">MÁS ALLÁ DEL EXAMEN</text>',
         '<text class="h" x="96" y="170">El asistente de soporte</text>',
         '<text class="sub" x="96" y="230">Un cliente pregunta y el asistente responde con los documentos de tu startup.</text>']
    nodes = [("phone", "El cliente", ["¿Cómo pido un reembolso?"]),
             ("Amazon Bedrock", "Amazon Bedrock", ["el modelo que redacta", "la respuesta"]),
             ("Amazon S3", "Knowledge Base", ["sobre S3 Vectors:", "busca en tus documentos"])]
    xs = [96, 696, 1296]
    for (ic, t, cs), x in zip(nodes, xs):
        b.append(f'<rect class="card" x="{x}" y="320" width="528" height="400" rx="24"/>')
        b.append(icon(ic, x + 48, 368, 104))
        b.append(f'<text class="big" x="{x + 48}" y="560">{t}</text>')
        b.append(lines("c", x + 48, 620, cs, 40, ' font-size="30"'))
    for x in [624, 1224]:
        b.append(f'<path d="M{x + 12} 520 H{x + 60} M{x + 46} 504 L{x + 62} 520 L{x + 46} 536" fill="none" stroke="{ORANGE}" stroke-width="5"/>')
    b.append(f'<rect x="96" y="790" width="1728" height="170" rx="16" fill="#2a2418" stroke="{GREEN}" stroke-width="2" stroke-dasharray="10 8"/>')
    b.append(kicker("PARA TU CERTIFICACIÓN", 136, 846, GREEN))
    b.append(f'<text class="t" x="136" y="910">Bedrock no entra al CLF-C02; entra al <tspan fill="{GREEN}">AWS Certified AI Practitioner</tspan>.</text>')
    return page("Asistente con Bedrock", "\n".join(b))


# ---------- 12 resumen ----------
STAGE = {1: ORANGE, 2: PURPLE, 3: MAGENTA, 4: BLUE, 5: GREEN}
ROWS = [
    (1, "Amazon S3", "Amazon S3", "Guardar fotos y archivos", "archivos, objetos"),
    (1, "S3 Glacier", "S3 Glacier", "Guardar años, abrir casi nunca", "archivo, poco acceso"),
    (1, "Amazon EBS", "Amazon EBS", "El disco de tu servidor", "disco de una instancia EC2"),
    (1, "Amazon EFS", "Amazon EFS", "Varios servidores, los mismos archivos", "archivos compartidos"),
    (2, "Amazon RDS", "RDS / Aurora", "Clientes, pedidos y sus relaciones", "relacional, SQL, Multi-AZ"),
    (3, "Amazon DynamoDB", "DynamoDB", "El carrito en pleno pico", "NoSQL, picos, sin servidores"),
    (3, "Amazon ElastiCache", "ElastiCache", "La misma consulta, mil veces", "caché, respuestas repetidas"),
    (4, "Amazon Rekognition", "Rekognition", "¿Qué hay en esta foto?", "imágenes"),
    (4, "Amazon Textract", "Textract", "Leer boletas y facturas", "documentos"),
    (4, "Amazon Comprehend", "Comprehend", "¿La reseña es buena o mala?", "texto, sentimiento"),
    (5, "Amazon Athena", "Athena", "Preguntar en SQL a tus datos en S3", "SQL sobre S3, pago por consulta"),
    (5, "Amazon Redshift", "Redshift", "Reportes grandes del negocio", "data warehouse"),
]


def resumen():
    b = [kicker("RESUMEN"), '<text class="h" x="96" y="142">¿Qué servicio elijo?</text>']
    legend = [(1, "MVP"), (2, "Primeros clientes"), (3, "Pico viral"), (4, "Cerebro"), (5, "Negocio")]
    x = 96
    for n, name in legend:
        b.append(f'<rect x="{x}" y="180" width="36" height="36" fill="{STAGE[n]}"/>')
        b.append(f'<text class="m" x="{x + 18}" y="207" font-size="22" text-anchor="middle" fill="{BG}">{n}</text>')
        b.append(f'<text class="c" x="{x + 48}" y="208">{name}</text>')
        x += 48 + int(len(name) * 12.5) + 44
    b.append(f'<text class="c" x="1824" y="208" text-anchor="end">en el examen buscan: <tspan class="m" fill="{ORANGE}">palabra clave</tspan></text>')
    for i, (st, ic, name, prob, kw) in enumerate(ROWS):
        col, r = (0, i) if i < 7 else (1, i - 7)
        x0, y0 = 96 + col * 880, 250 + r * 110
        b.append(f'<rect class="card" x="{x0}" y="{y0}" width="848" height="98" rx="14"/>')
        b.append(f'<rect x="{x0}" y="{y0}" width="10" height="98" fill="{STAGE[st]}"/>')
        b.append(icon(ic, x0 + 30, y0 + 17, 64))
        b.append(f'<text class="t" x="{x0 + 116}" y="{y0 + 42}" font-size="30">{name}</text>')
        b.append(f'<text class="c" x="{x0 + 116}" y="{y0 + 80}">{prob}</text>')
        b.append(f'<text class="m" x="{x0 + 824}" y="{y0 + 42}" font-size="24" fill="{ORANGE}" text-anchor="end">{kw}</text>')
    return page("Qué servicio elijo", "\n".join(b))


# ---------- 13/14 preguntas ----------
Q = {
    1: dict(tag="MEMORIA", answer="B",
            scene=["Tu app tiene un carrito de compras. Casi todo el día el tráfico es bajo,",
                   "pero cuando un influencer publica la app, las solicitudes se multiplican",
                   "en minutos. El equipo es pequeño y no quiere planificar capacidad",
                   "ni administrar servidores de base de datos."],
            ask="¿Qué opción cumple mejor?",
            opts=[("Amazon RDS", ["Amazon RDS for PostgreSQL", "en una instancia fija"]),
                  ("Amazon DynamoDB", ["Amazon DynamoDB", "en modo on-demand"]),
                  ("Amazon Redshift", ["Amazon Redshift"]),
                  ("Amazon EC2", ["Una base de datos instalada", "por el equipo en Amazon EC2"])],
            head="B. DynamoDB on-demand",
            sub="Escala sola, cobra por solicitud y nadie tiene que planificar capacidad.",
            why=[["Es gestionada, pero una instancia fija no ajusta", "su capacidad automáticamente."],
                 ["Aguanta el pico sin que toques nada", "y pagas por lo que usas."],
                 ["Es para analítica (data warehouse),", "no para el carrito de una app."],
                 ["El equipo tendría que administrar el servidor:", "justo lo que no quiere."]]),
    2: dict(tag="CEREBRO", answer="B",
            scene=["Tus clientes suben fotos de sus boletas para pedir reembolsos.",
                   "La startup quiere sacar automáticamente el nombre del proveedor,",
                   "la fecha y el total, sin entrenar un modelo propio."],
            ask="¿Qué servicio debe usar?",
            opts=[("Amazon Rekognition", ["Amazon Rekognition"]),
                  ("Amazon Textract", ["Amazon Textract"]),
                  ("Amazon Comprehend", ["Amazon Comprehend"]),
                  ("SageMaker AI", ["Amazon SageMaker AI"])],
            head="B. Amazon Textract",
            sub="Lee boletas sin plantillas y te da proveedor, fecha y total. Como la boleta de la demo.",
            why=[["Entiende imágenes y hasta detecta texto, pero el", "especializado en boletas es Textract: te da los campos."],
                 ["Extrae proveedor, fecha y total de casi", "cualquier boleta o factura, sin plantillas."],
                 ["Analiza texto que ya tienes (sentimiento,", "entidades). No lee imágenes."],
                 ["Sirve para entrenar modelos propios,", "justo lo que el enunciado descarta."]]),
}
LETTERS = "ABCD"


def option_card(i, ic, label, x, y, w, h, state, why=None):
    ok = state == "ok"
    stroke, sw = (GREEN, 4) if ok else (GRID, 1.5)
    tile = GREEN if ok else (GRID if state == "off" else ORANGE)
    txt = MUTED if state == "off" else "#fff"
    iy = y + 28 if why else y + (h - 72) // 2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{CARD}" stroke="{stroke}" stroke-width="{sw}"/>',
           f'<rect x="{x + 28}" y="{iy}" width="72" height="72" fill="{tile}"/>',
           f'<text class="m" x="{x + 64}" y="{iy + 52}" font-size="46" text-anchor="middle" fill="{BG}">{LETTERS[i]}</text>',
           f'<g opacity="{".5" if state == "off" else "1"}">{icon(ic, x + 116, iy, 72)}</g>']
    ty = iy + 30 if len(label) == 2 else iy + 48
    out.append(lines("t", x + 212, ty, label, 40, f' font-size="32" fill="{txt}"'))
    if why:
        out.append(lines("c", x + 28, y + 168, why, 46, ' font-size="32"' + (f' fill="{GREEN}"' if ok else ' fill="#d5d9e0"')))
    return "".join(out)


def pregunta(n):
    q = Q[n]
    b = [kicker(f"PREGUNTA {n} · {q['tag']}")]
    b.append(lines("big", 96, 160, q["scene"], 56, ' font-size="38" font-weight="500"'))
    ya = 160 + len(q["scene"]) * 56 + 50
    b.append(f'<text class="h" x="96" y="{ya}" font-size="52" fill="{ORANGE}">{q["ask"]}</text>')
    top = ya + 70
    h = min(200, (1000 - top - 24) // 2)
    for i, (ic, label) in enumerate(q["opts"]):
        b.append(option_card(i, ic, label, 96 + (i % 2) * 880, top + (i // 2) * (h + 24), 848, h, "plain"))
    return page(f"Pregunta {n}", "\n".join(b))


def respuesta(n):
    q = Q[n]
    b = [kicker(f"PREGUNTA {n} · RESPUESTA", bracket=GREEN),
         f'<text class="h" x="96" y="142" fill="{GREEN}">{q["head"]}</text>',
         f'<text class="sub" x="96" y="200">{q["sub"]}</text>']
    for i, (ic, label) in enumerate(q["opts"]):
        st = "ok" if LETTERS[i] == q["answer"] else "off"
        b.append(option_card(i, ic, label, 96 + (i % 2) * 880, 270 + (i // 2) * 340, 848, 310, st, q["why"][i]))
    return page(f"Respuesta {n}", "\n".join(b))


OUT = {
    "02-dia1-dia500.svg": dia1, "04b-pruebalo.svg": pruebalo, "11-bedrock.svg": bedrock, "12-resumen.svg": resumen,
    "13a-pregunta1.svg": lambda: pregunta(1), "13b-respuesta1.svg": lambda: respuesta(1),
    "14a-pregunta2.svg": lambda: pregunta(2), "14b-respuesta2.svg": lambda: respuesta(2),
}

if __name__ == "__main__":
    for name, fn in OUT.items():
        (HERE / name).write_text(fn())
        print(HERE / name)
