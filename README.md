# Tests unitaires et CI/CD

![Tests](https://github.com/voirinprof/start_your_tests_and_actions/actions/workflows/ci.yml/badge.svg)

Petit projet d'exemple pour s'exercer aux tests unitaires (`pytest`) et à
l'intégration continue (CI/CD) sur un cas simple : des fonctions de calcul (NDVI, conversion de surface).

## Objectifs d'apprentissage

- Écrire des tests unitaires avec `pytest` (cas normaux, cas limites, erreurs).
- Mesurer la couverture de code (`pytest-cov`) et interpréter le rapport.
- Comprendre le rôle d'un pipeline CI/CD (GitHub Actions) : exécuter les tests
  automatiquement à chaque `push`/`pull request`.

## Structure du projet

```
.
├── src/
│   └── calculs.py         # Fonctions à tester (NDVI, conversion de surface)
├── tests/
│   └── test_calculs.py    # Tests unitaires correspondants
├── requirements.txt        # Dépendances (pytest, pytest-cov)
└── README.md
```

## Installation

Il est recommandé de travailler dans un environnement virtuel, avec `venv` ou
avec `conda` :

**Avec `venv`**

```bash
python -m venv venv
source venv/bin/activate      # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
```

**Avec `conda`**

```bash
conda create -n gmq580 python=3.10
conda activate gmq580
pip install -r requirements.txt
```

## Lancer les tests localement

```bash
pytest tests/ -v
```

`-v` (verbose) affiche le nom de chaque test et son résultat (`PASSED`/`FAILED`),
utile pour comprendre exactement ce qui a été vérifié.

### Couverture de code

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

Cette commande indique le **pourcentage de lignes de `src/` exécutées par les tests**, et liste (`missing`) les lignes qui ne sont couvertes par aucun test.
Une couverture élevée ne garantit pas l'absence de bugs, mais une ligne non couverte signifie qu'elle n'a jamais été vérifiée.

## Comprendre les tests existants

Le fichier [tests/test_calculs.py](tests/test_calculs.py) illustre trois types de cas à tester pour chaque fonction :

1. **Cas normal** — `test_ndvi_healthy_vegetation`, `test_surface_conversion` :
   la fonction retourne bien la valeur attendue.
2. **Cas limite** — `test_ndvi_exact_calculation` compare à une valeur précise
   avec `pytest.approx()` (utile pour les flottants, où `==` strict est
   risqué à cause des arrondis).
3. **Cas d'erreur** — `test_ndvi_division_by_zero`, `test_surface_negative` :
   on vérifie qu'une entrée invalide lève bien une exception
   (`pytest.raises(ValueError)`), pas seulement que le code « ne plante pas ».

Un bon test suit généralement le patron **Arrange / Act / Assert** : préparer
les données d'entrée, appeler la fonction, puis vérifier le résultat.

## Intégration continue (CI/CD)

Le badge en haut de ce README reflète l'état du workflow GitHub Actions défini
dans [.github/workflows/ci.yml](.github/workflows/ci.yml). Ce fichier décrit,
au format YAML, une suite d'étapes que GitHub exécute automatiquement pour
vous — sur ses propres serveurs, pas sur votre machine.

### Quand le workflow se déclenche-t-il ?

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

Le bloc `on:` définit les évènements déclencheurs : ici, chaque `push` sur
`main` et chaque *pull request* ciblant `main`. C'est ce qui permet de
détecter immédiatement si un changement casse un test, sans attendre qu'un
correcteur (ou vous-même) le remarque manuellement.

### Que fait le job `tests` ?

Un *job* s'exécute sur une machine neuve (`runs-on: ubuntu-latest`), qui ne
contient rien de votre environnement local. Chaque étape (`steps`) doit donc
reconstruire ce dont elle a besoin, dans l'ordre :

1. **`actions/checkout@v4`** — récupère le code du dépôt sur la machine
   virtuelle (sans cette étape, il n'y aurait aucun fichier à tester).
2. **`actions/setup-python@v5`** — installe Python 3.10.
3. **Installer les dépendances** — `pip install pytest pytest-cov`, comme vous
   le faites localement avec `requirements.txt`.
4. **Lancer les tests avec couverture** — la même commande
   `pytest tests/ --cov=src --cov-report=term-missing -v` que vous utilisez
   sur votre machine. C'est là que le workflow échoue (❌) ou réussit (✅) :
   si un seul test échoue, `pytest` retourne un code d'erreur et le job est
   marqué en échec.
5. **`actions/upload-artifact@v4`** (`if: always()`, donc exécutée même si les
   tests échouent) — sauvegarde un fichier `coverage.xml` téléchargeable
   depuis l'onglet *Actions* du dépôt GitHub, pour consulter le rapport de
   couverture après coup.

> ⚠️ Avec la commande actuelle (`--cov-report=term-missing`), `coverage.xml`
> n'est pas généré : cette étape échouera. Pour qu'elle fonctionne, ajoutez
> `xml` au rapport, par exemple `--cov-report=term-missing --cov-report=xml`.

