# Weakly supervised models

## Installation
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
pip install -e .
```

## Usage
```
python weakly_supervised_method/pipeline.py --train TRAIN --test TEST --plots_dir PLOTS_DIR
```

## Testing
- To run pytest tests:
`python -m pytest tests/ -v`

- To check the code coverage:
`coverage report -m`
