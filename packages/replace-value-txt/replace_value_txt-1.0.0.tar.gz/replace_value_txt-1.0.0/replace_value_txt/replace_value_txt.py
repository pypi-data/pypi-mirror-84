def replace_value_txt(input_path, dict_replace, output_path=None, encoding='utf-8'):
    """
    This function replaces values in the txt and csv files.

    Args:
        input_path (str): Input the name document.
        dict_replace (dict): Dictionary with the data to replace. Example: {';',','}
        output_path (str, optional): Output the name document. Defaults to None.
        encoding (str, optional): Choice the encoding in [utf-8,cp1252,ISO-8859-1]. Defaults to 'utf-8'.
    """

    # Test output_path
    if output_path == None:
        output_path = input_path

    # Read in the file
    with open(input_path, 'r', encoding=encoding) as file:
        filedata = file.read()

    # Replace the target string
    for key, value in dict_replace.items():
        filedata = filedata.replace(key, value)

    # Write the file out again
    with open(output_path, 'w', encoding=encoding) as file:
        file.write(filedata)

    # Close
    file.close()

    return
