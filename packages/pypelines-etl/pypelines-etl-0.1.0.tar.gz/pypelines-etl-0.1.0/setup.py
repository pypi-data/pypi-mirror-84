# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypelines']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypelines-etl',
    'version': '0.1.0',
    'description': 'Simple library to make pipelines or ETL',
    'long_description': "# Pypelines-ETL\n\nSimple library to make pipelines or ETL\n\n## Installation\n```bash\n$ pip install pypelines-etl\n```\n\n## Usage\n`pypelines` allows you to build ETL pipeline. For that, you simply need\nthe combination of an `Extractor`, some `Transformer` or `Filter`, and a `Loader`.\n\n### Extractor\nMaking an extractor is fairly easy. Simply decorate a function that return\nthe data with `Extractor`:\n```python\nimport pandas\nfrom pypelines import Extractor\n\n@Extractor\ndef read_iris_dataset(filepath: str) -> pandas.Dataframe:\n    return pandas.read_csv(filepath)\n```\n\n### Transformer or Filter\nThe `Transformer` and `Filter` decorators are equivalent.\n\nMaking a `Transformer` or a `Filter` is even more easy:\n```python\nimport pandas\nfrom pypelines import Filter, Transformer\n\n@Filter\ndef keep_setosa(df: pandas.DataFrame) -> pandas.DataFrame:\n    return df[df['class'] == 'Iris-setosa']\n\n\n@Filter\ndef keep_petal_length(df: pandas.DataFrame) -> pandas.Series:\n    return df['petallength']\n\n\n@Transformer\ndef mean(series: pandas.Series) -> float:\n    return series.mean()\n```\n\nNote that it is possible to combine the `Transformer` and the `Filter`\nto shorten the pipeline syntax. For example:\n```python\nnew_transformer = keep_setosa | keep_petal_length | mean\npipeline = read_iris_dataset('filepath.csv') | new_transformer\nprint(pipeline.value)\n# 1.464\n```\n\n### Loader\nIn order to build a `Loader`, it suffices to decorate a function that takes at\nleast one `data` parameter. \n```python\nimport json\nfrom pypelines import Loader\n\n@Loader\ndef write_to_json(output_filepath: str, data: float) -> None:\n    with open(output_filepath, 'w') as file:\n        json.dump({'mean-petal-lenght': {'value': data, 'units': 'cm'}}, file)\n```\nA `Loader` can be called without the `data` parameter,\nwhich loads arguments (like an URL or a path). For example, calling `write_to_json(output.json)`\nwill not execute the function, but store the `output_filepath` argument until the `Loader` execution in a pipeline.\nThe standard execution of the function (with the `data` argument) is however still usable `write_to_json(output.json, data=1.464)`.\n\n\n### ETL pipeline\n\nTo make and run the pipeline, simply combine the `Extractor` with the `Transformer`, the `Filter` and the `Loader`\n```python\nread_iris_dataset('filepath.csv') | keep_setosa | keep_petal_length | mean | write_to_json('output.json')\n```\n",
    'author': 'Gabriel Couture',
    'author_email': 'gacou54@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gacou54/pypelines',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
