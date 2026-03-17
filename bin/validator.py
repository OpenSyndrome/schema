# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jsonschema>=4.26.0",
#     "pyld>=2.0.4",
# ]
# ///
import json
from jsonschema import validate, exceptions
from pyld import jsonld


# TODO download from definitions in the future
with open('bin/extremetemperaturesheat_argentina_jsonld.json') as f:
    doc_json = json.load(f)

with open('schemas/v1/schema.json') as f:
    schema = json.load(f)

print("--- JSON schema validation ---")
try:
    validate(instance=doc_json, schema=schema)
    print("JSON Schema OK")
except exceptions.ValidationError as err:
    print(f"Validation failed: {err.message} - {err.json_path}")

print("\n--- JSON-LD validation ---")
try:
    # check if something was not mapped
    expanded = jsonld.expand(doc_json)
    print("JSON-LD expansion works")

    nquads = jsonld.normalize(doc_json, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    print(f"RFD graph {len(nquads.splitlines())} triplas.")
    print(nquads)

except Exception as e:
    print(f"❌ Erro ao processar JSON-LD: {e}")
