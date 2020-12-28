import json as js


def save_json(face, eyes, smile, outputPath = 'outputTemp.json'):
    data = {
        'Face': face,
        'Eyes': eyes,
        'Smile': smile
    }
    with open(outputPath, 'w') as json_file:
        js.dump(data, json_file)