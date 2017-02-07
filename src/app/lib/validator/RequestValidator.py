from django.shortcuts import render_to_response


class RequestValidator(object):

    def __init__(self, function):
        self.function = function

    def __call__(self, request):
        try:
            self.validate(request)
            return self.function(request)
        except Exception as e:
            error = e[0]
            try:
                error += e[1]
            except:
                pass
            return render_to_response("general/error.html", {"cause": error})

    def validate(self, request):
        raise NotImplementedError()

    def raise_exception(self, message):
        raise Exception(str(type(self).__name__), message)