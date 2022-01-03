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

## Clickbait models

The model is built on [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert) using the [Webis-Clickbait-17](https://webis.de/data/webis-clickbait-17.html) dataset.

- First download the pretrained model folder from https://uoe-my.sharepoint.com/:f:/g/personal/s2063031_ed_ac_uk/Emnyjc9-Gz1CthtXoCzkppIB2DeSnEpTxBNmlSBElpbqQw?e=aQ6s9e.
- Create a folder named 'clickbait_models' under the current directory and put the downloaded files under it. The directory structure should be:
  -- straplines
     -- clickbait_models
        -- DistilBert4ClickBait.model
        -- DistilBert4ClickBait.tokenizer
