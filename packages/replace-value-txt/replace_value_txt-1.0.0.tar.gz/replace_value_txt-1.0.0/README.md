# Replace values in txt and csv

Library to replace the values in a ".txt" and ".csv" files.

## Install

`pip install replace-value-txt`

## Import:

`import replace_value_txt`

## Function:

`replace_value_txt(input_path, dict_replace, output_path=None, encoding='utf-8')`

- input_path: String with the name of the path you want to replace the value with. Example: `C:/Users/example.csv`
- dict_replace: Dict with the data you want replace. Example: `{';': ',', 'ã':'a'}`
- output_path: String with the name of the path you want to save. Defaults to `input_path`. Example: `C:/Users/example_output.csv`
- encoding: String with the name of the encoding. Defaults to `utf-8`. You can use `utf-8, cp1252, ISO-8859-1`
