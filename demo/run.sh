#!/usr/bin/env bash
# Demo driver. Usage: demo/run.sh deploy | subir <archivo> <productos|facturas|resenas> | ver | reiniciar | destroy
set -euo pipefail
cd "$(dirname "$0")/.."

export AWS_PROFILE="${AWS_PROFILE:?set AWS_PROFILE to your sandbox profile}" AWS_REGION=us-west-2
[[ "$AWS_PROFILE" == *sandbox* ]] || { echo "refusing: AWS_PROFILE=$AWS_PROFILE is not a sandbox profile" >&2; exit 1; }
CDK="npx -y aws-cdk@2.1143.0"
STACK=DelExcelAlMillon
out() { aws cloudformation describe-stacks --stack-name $STACK --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }

case "${1:-}" in
  deploy)  $CDK deploy $STACK ;;
  subir)   aws s3 cp "$2" "s3://$(out BucketName)/$3/$(basename "$2")"
           echo "subido; en unos segundos: demo/run.sh ver" ;;
  ver)     aws dynamodb scan --table-name "$(out TableName)" --output json | python3 -c '
import json, sys
val = lambda v: v.get("S", v.get("N"))
for i in sorted(json.load(sys.stdin)["Items"], key=lambda i: i["archivo"]["S"]):
    if "resultado" not in i:  # the public demo quota item
        usos, tx = (i.get(k, {}).get("N", "0") for k in ("usos", "textract"))
        print(f"cupo web: {usos} usos, {tx} de Textract"); continue
    r = ", ".join(f"{k}: {val(v)}" for k, v in i["resultado"]["M"].items())
    a = i["archivo"]["S"]
    print(f"{a:32} {r}")' ;;
  reiniciar) aws dynamodb delete-item --table-name "$(out TableName)" --key '{"archivo": {"S": "_cupo"}}'
           echo "cupo de la demo web reiniciado" ;;
  destroy) $CDK destroy $STACK --force ;;
  *)       sed -n '2p' "$0"; exit 1 ;;
esac
