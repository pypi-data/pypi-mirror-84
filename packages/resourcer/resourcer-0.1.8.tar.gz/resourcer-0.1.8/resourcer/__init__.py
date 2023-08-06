import requests, json, copy
from string import Formatter


class Response():
    def __init__(self, **kwargs):
        self.status_code = kwargs['status_code']
        self.text = kwargs['text']
    
    def to_dict(self):
        return json.loads(self.text)
        

class Resource():
    def __init__(self, url):
        self._url = url
        self._fields = []
        self._headers = {}
        self._params = {}
        self._data = {}

        for fields in Formatter().parse(url):
            field = fields[1]
            if field:
                self._fields.append(field)
                setattr(self, field, None)

    def is_valid(self):
        for field in self._fields:
            if not getattr(self, field):
                return False
        return True

    @property
    def request_url(self):
        params = []
        for key, value in self._params.items():
            params.append(f'{key}={value}')
        return self.to_url() + '?' + '&'.join(params)


    @property
    def url(self):
        return self.to_url()

    def to_url(self, **kwargs):
        values = {}
        for field in self._fields:
            values[field] = getattr(self, field)
        return self._url.format(**values)

    def set_headers(self, headers):
        self._headers = copy.deepcopy(headers)

    def header(self, key, value):
        self._headers[key] = value
    
    def set_params(self, params):
        self._params = copy.deepcopy(params)

    def param(self, key, value):
        self._params[key] = value
    
    def set_data(self, data):
        self._data = copy.deepcopy(data)

    def data(self, key, value):
        self._data[key] = value

    def get(self):
        if self.is_valid():
            response = requests.get(url=self.to_url(), params=self._params, headers=self._headers)
            return Response(status_code=response.status_code, text=response.text)
    
    def post(self, **kwargs):
        if self.is_valid():
            is_sent = False
            response = None

            if 'form' in kwargs:
                response = requests.post(url=self.to_url(), data=self._data, params=self._params, headers=self._headers)
                is_sent = True
            
            if not is_sent:
                response = requests.post(url=self.to_url(), json=self._data, params=self._params, headers=self._headers)
                
            return Response(status_code=response.status_code, text=response.text)

    def put(self):
        if self.is_valid():
            response = requests.put(url=self.to_url(), json=self._data, params=self._params, headers=self._headers)
            return Response(status_code=response.status_code, text=response.text)

    def patch(self):
        if self.is_valid():
            response = requests.patch(url=self.to_url(), json=self._data, params=self._params, headers=self._headers)
            return Response(status_code=response.status_code, text=response.text)

    def delete(self):
        if self.is_valid():
            response = requests.delete(url=self.to_url(), params=self._params, headers=self._headers)
            return Response(status_code=response.status_code, text=response.text)