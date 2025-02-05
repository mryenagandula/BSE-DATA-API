def getDictkeyAndValue(key,data):
    if key in data:
        formated_data = data[key] if data[key]  else "";
        if isinstance(formated_data, str):
            formated_data = formated_data.replace("\r\n\r\n", "")
        return formated_data;
    else:
        return '';

