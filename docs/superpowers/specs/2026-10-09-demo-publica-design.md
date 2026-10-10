# Public demo at demo.builtbyandres.com

## Goal
Let the audience try the three "senses" (Rekognition, Textract, Comprehend) from their phone
during the talk, safely and inside the < USD 2 demo budget. Live today, destroyed after.

## Architecture
Same CDK stack. New pieces:
- Lambda `Publico` (same code asset, handler `web.handler`), reserved concurrency 5,
  IAM: the three AI actions + UpdateItem/PutItem on keys `_cupo` and `web/*` only. No S3 access.
- API Gateway HTTP API: `GET /` (page), `POST /analizar` (analysis). `POST /analizar`
  throttled at rate 1.6 rps, burst 5 (about 96 req/min for everyone); GETs at 20 rps, burst 50
  so the whole room can open the page at once. execute-api endpoint disabled.
- AI clients: one attempt, short timeouts, so one quota unit is at most one billed call.
- Custom domain `demo.builtbyandres.com`, ACM cert in us-west-2, DNS validation by hand in
  Cloudflare (validation CNAME DNS only; `demo` CNAME proxied; SSL/TLS mode Full (strict)).
- Optional Cloudflare rate-limit rule: 5 req / 10 s per IP.

The S3-triggered flow stays unchanged for the terminal demo.

## API
`POST /analizar` body `{"tipo": "productos"|"facturas"|"resenas", "contenido": "<base64 | text>"}`.
- 200 `{"resultado": {...}, "quedan": N}`
- 400 unknown tipo, bad base64, image > 1.5 MB, review empty or > 1000 chars
- 429 `agotada` when the global cap is reached; API Gateway throttling also returns 429
Visitors' files are never stored. The result is saved in the table under `web/<uuid>`.

## Global cap
Item `archivo="_cupo"` in the results table, conditional `UpdateItem` (ADD).
300 calls total, at most 100 Textract. Worst case about USD 1.30. Reset: delete the item.

## Page (`lambda/index.html`)
Single file, no framework, neutral Spanish, mobile first. Tabs Foto / Boleta / Reseña,
sample buttons (bundled `boleta-bodega.png`, good/bad review), images resized client-side to
1024 px JPEG 0.85, readable results, "Qué acaba de pasar" path line, "Quedan N pruebas",
"No guardamos tu archivo, solo el resultado".

## Tests
- handler: API routing, oversize rejection, cap returns 429, S3 flow still works.
- stack: reserved concurrency, throttling, custom domain.
