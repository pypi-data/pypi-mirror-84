def request(request):
    print(f'{request.method} {request.path} {request.get_json(silent=True)}')

def response(response):
    print(f'{response[0]} {response[1]} {response[2])