from lib.validator.RequestValidator import RequestValidator


class ConsumeValidator(RequestValidator):

    def validate(self, request):
        if not request.POST:
            self.raise_exception("Not a POST request!")

        if not ("backpack_slot" in request.POST):
            self.raise_exception("Not all arguments given!")

        if request.POST["backpack_slot"] == "":
            self.raise_exception("Arguments empty!")

        if "bp_slot_" not in request.POST["backpack_slot"]:
            self.raise_exception("Argument formatting not correct!")

        return True