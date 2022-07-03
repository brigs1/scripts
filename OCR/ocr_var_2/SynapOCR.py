print("\t\t", "<<<SynapOCR Engine operated >>>")

import requests
from collections import defaultdict
import json
from json.decoder import JSONDecodeError

class SynapOcrClient:
    """
    Base class which does requests calls
    """
    API_ENDPOINT = None
    API_KEY = None
    HEADERS = None

    def __init__(self,api_endpoint: str, api_key: str):
        """
        Initiation of SynapOCR Client object
        """
        self.API_ENDPOINT = api_endpoint
        self.API_KEY = api_key
        
        """
        if 1:
            self.HEADERS = {'Content-Type': 'multipart/form-data'}
        else:
            self.HEADERS = {'Content-Type': 'application/json'}
        """
    """
    def get(self, url: str):
        r = requests.get(self.API_ENDPOINT + url, headers=self.HEADERS)
        return r.json()
    """
    def post(self, url: str,  data):
        
        if data.get('image') is not None:
            files ={'image':data['image']}
            file = data.pop('image')
            r = requests.post(self.API_ENDPOINT + url, files={'image':file}, data=data)
        else:
            r = requests.post(self.API_ENDPOINT + url, data=data)
            if r.headers.get('Content-disposition') is not None: 
                if r.headers['Content-disposition'].find('attachment') == 0:
                    return r.content
        try:
            result = r.json()
        except JSONDecodeError:
            result = r.text
        return result

    """
    def delete(self, url: str, data: json = None):
        if data:
            r = requests.delete(self.API_ENDPOINT + url, data=data, headers=self.HEADERS)
        else:
            r = requests.delete(self.API_ENDPOINT + url, headers=self.HEADERS)
        return r.text
    """
class SynapOCR:
    """
    http://localhost:62975/sdk/ocr
    """

    def __init__(self, api_endpoint: str, api_key: str):
        self._synap_ocr_client = SynapOcrClient(api_endpoint=api_endpoint,api_key=api_key)


    def post_ocr(self, **kwargs):
        """
        :param name: 
        :param kwargs:
                - 설명
        :return: JSON response
        """
        data = defaultdict()
        data['api_key'] = self._synap_ocr_client.API_KEY

        for key, value in kwargs.items():
            data[key] = value
        
        r = self._synap_ocr_client.post('/sdk/ocr',data)
        
        return r

    def post_recognize(self, name: str, **kwargs):
        """
        """
        data = defaultdict()
        data['api_key'] = self._synap_ocr_client.API_KEY 
        for key, value in kwargs.items():
            data[key] = value
        r = self._synap_ocr_client.post('/sdk/recognize', data)
        return r

    def post_save(self,file_name=str) -> bytes:
        """
        """
        data = defaultdict()
        data['api_key'] = self._synap_ocr_client.API_KEY
        
        r = self._synap_ocr_client.post('/sdk/out/'+file_name, data)
        
        return r
        """
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        return 
        """
    def post_monitor(self):
        """
        """
        data = defaultdict()
        data['api_key'] = self._synap_ocr_client.API_KEY
        r = self._synap_ocr_client.post('/sdk/monitor', data)
        return r
