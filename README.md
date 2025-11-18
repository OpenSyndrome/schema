# schema

[![Validate schema](https://github.com/OpenSyndrome/schema/actions/workflows/validate_schema.yml/badge.svg)](https://github.com/OpenSyndrome/schema/actions/workflows/validate_schema.yml)

[![Dataset on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/dataset-on-hf-md.svg)](https://huggingface.co/datasets/opensyndrome/case-definitions)

The Open Syndrome Definition JSON schema is an open, interoperable format for [case definitions](https://methods.sagepub.com/ency/edvol/encyc-of-epidemiology/chpt/case-definition).

## Contribute

Please feel free to suggest any changes to this format. To ensure that the format is still valid,
do the validation locally. You will need [npm](https://nodejs.org/pt/learn/getting-started/an-introduction-to-the-npm-package-manager).
Then install [ajv-cli](https://github.com/ajv-validator/ajv-cli)
and [ajv-formats](https://github.com/ajv-validator/ajv-formats):

```bash
npm install -g ajv-cli ajv-formats
```

To run the schema validation, run

```bash
ajv compile --spec draft2020 -c ajv-formats -s schemas/v1/schema.json
```

To run your changed schema against a JSON definition:

```bash
ajv validate --spec draft2020 -c ajv-formats -s schemas/v1/schema.json -d brazil_dengue.json
```

If you propose any changes, update the [CHANGELOG](CHANGELOG.md) accordingly.

## Citing & Authors

If you find this repository helpful, feel free to cite our publication: The Open Syndrome Definition

```
@misc{ferreira2025opensyndromedefinition,
      title={The Open Syndrome Definition}, 
      author={Ana Paula Gomes Ferreira and Aleksandar Anžel and Izabel Oliva Marcilio de Souza and Helen Hughes and Alex J Elliot and Jude Dzevela Kong and Madlen Schranz and Alexander Ullrich and Georges Hattab},
      year={2025},
      eprint={2509.25434},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2509.25434}, 
}
```
