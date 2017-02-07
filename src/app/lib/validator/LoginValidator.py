from lib.validator.RequestValidator import RequestValidator


class LoginValidator(RequestValidator):

    def validate(self, request):
        if not request.POST:
            self.raise_exception("Not a POST request!")

        if not ("user" in request.POST and "password" in request.POST):
            self.raise_exception("Not all arguments given!")

        if request.POST["user"] == "" or request.POST["password"] == "":
            self.raise_exception("Arguments empty!")

        return True