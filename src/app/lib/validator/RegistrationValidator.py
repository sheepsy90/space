from lib.validator.RequestValidator import RequestValidator


class RegistrationValidator(RequestValidator):

    def validate(self, request):
        if not request.POST:
            self.raise_exception("Not a POST request!")

        if not ("password_first" in request.POST and "password_again" in request.POST and "user" in request.POST):
            self.raise_exception("Not all arguments given!")

        password_first_empty = request.POST["password_first"] == ""
        password_again_empty = request.POST["password_again"] == ""
        user_empty = request.POST["user"] == ""

        if password_again_empty or password_first_empty or user_empty:
            self.raise_exception("Arguments empty!")

        return True