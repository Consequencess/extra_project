class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print('Hello!')
        response = self.get_response(request)
        response.hello = 'My name is John'
        print(response.data)

        return response
