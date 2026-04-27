# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jsonschema>=4.26.0",
#     "pyld>=2.0.4",
#     "rdflib>=7.0.0",
# ]
# ///
import json
from jsonschema import validate, exceptions
from pyld import jsonld
from rdflib import Graph

OSD_NS = 'https://w3id.org/opensyndrome/ns/'


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

with open('schemas/v1/context.jsonld', encoding='utf-8') as f:
    local_context = json.load(f)

print("\n--- JSON-LD validation ---")
doc_json['@context'] = local_context['@context']
expanded = None
try:
    # check if something was not mapped
    expanded = jsonld.expand(doc_json)
    print("JSON-LD expansion works")

    nquads = jsonld.normalize(doc_json, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    print(f"RFD graph {len(nquads.splitlines())} triplas.")

except Exception as exception:
    print(f"❌ Erro ao processar JSON-LD: {exception}")

print("\n--- Ontology cross-check (context vs ontology) ---")
ontology = Graph().parse('schemas/v1/ontology.ttl', format='turtle')
defined_terms = {str(s) for s in ontology.subjects() if str(s).startswith(OSD_NS) and str(s) != OSD_NS}
print(f"Ontology declares {len(defined_terms)} osd: terms.")

context_terms: set[str] = set()
def collect_osd_terms(value):
    if isinstance(value, str) and value.startswith('osd:'):
        context_terms.add(OSD_NS + value.split(':', 1)[1])
    elif isinstance(value, dict):
        for v in value.values():
            collect_osd_terms(v)
    elif isinstance(value, list):
        for v in value:
            collect_osd_terms(v)

for v in local_context['@context'].values():
    collect_osd_terms(v)

missing_in_ontology = context_terms - defined_terms
if missing_in_ontology:
    print(f"❌ Context references {len(missing_in_ontology)} osd: term(s) not declared in the ontology:")
    for term in sorted(missing_in_ontology):
        print(f"   - {term}")
else:
    print(f"✅ All {len(context_terms)} osd: terms in the context are declared in the ontology.")

unused_in_context = defined_terms - context_terms
if unused_in_context:
    print(f"ℹ️  {len(unused_in_context)} osd: term(s) declared in the ontology but not used by the context:")
    for term in sorted(unused_in_context):
        print(f"   - {term}")

print("\n--- Example document round-trip (example vs ontology) ---")
if expanded is None:
    print("Skipping (JSON-LD expansion failed).")
else:
    used_terms: set[str] = set()
    def collect_used(value):
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(k, str) and k.startswith(OSD_NS):
                    used_terms.add(k)
                collect_used(v)
        elif isinstance(value, list):
            for v in value:
                collect_used(v)
        elif isinstance(value, str) and value.startswith(OSD_NS):
            used_terms.add(value)

    collect_used(expanded)

    missing_for_example = used_terms - defined_terms
    if missing_for_example:
        print(f"❌ Example uses {len(missing_for_example)} osd: term(s) not declared in the ontology:")
        for term in sorted(missing_for_example):
            print(f"   - {term}")
    else:
        print(f"✅ All {len(used_terms)} osd: terms used in the example are declared in the ontology.")
