
import requests

import json


# Classe OCRDriver Responsável pela automatização do site do Banco Itaú
class OcrSpace:

    api_key = 'edc04793d988957'
    language = 'por'


    def ocr_space_file(self ,filename, overlay=False):
        """ OCR.space API request with local file.
            Python3.5 - not tested on 2.7
        :param filename: Your file path & name.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param api_key: OCR.space API key.
                        Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                        List of available language codes can be found on https://ocr.space/OCRAPI
                        Defaults to 'en'.
        :return: Result in JSON format.
        """

        payload = {'isOverlayRequired': overlay,
                   'apikey': self.api_key,
                   'language': self.language,
                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        return r.content.decode()

    def returnTextOCR(self ,filepath):
        test_file = self.ocr_space_file(filename=filepath)
        print(test_file)
        load = json.loads(test_file)
        dump = json.dumps(load['ParsedResults'][0])

        load = json.loads(dump)
        dump = json.dumps(load)


        dump = json.dumps(load['ParsedText'])

        return json.loads(dump)