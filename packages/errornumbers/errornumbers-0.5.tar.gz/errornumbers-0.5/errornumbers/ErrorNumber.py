class ErrorNumber:
    value = 0
    absolute_error = 0
    relative_error = 0

    def __init__(self, value, error, relative=False):
        if relative == True:
            self.value = value
            self.relative_error = error
            self.absolute_error = self.relative_error * self.value;
        else:
            self.value = value
            self.absolute_error = error
            self.relative_error = error / value

    def plus(self, other):
        return ErrorNumber(self.value + other.value, self.absolute_error + other.absolute_error)

    def plusc(self, constant):
        return ErrorNumber(self.value + constant, self.absolute_error)

    def minus(self, other):
        return ErrorNumber(self.value - other.value, self.absolute_error + other.absolute_error)

    def minusc(self, constant):
        return ErrorNumber(self.value - constant, self.absolute_error)

    def times(self, other):
        return ErrorNumber(self.value * other.value, self.relative_error + other.relative_error, relative=True)

    def timesc(self, constant):
        return ErrorNumber(self.value * constant, self.relative_error, relative=True)

    def divided_by(self, other):
        return ErrorNumber(self.value / other.value, self.relative_error + other.relative_error, relative=True)

    def divided_byc(self, constant):
        return ErrorNumber(self.value / constant, self.relative_error, relative=True)

    def inverse(self):
        return ErrorNumber((1 / self.value), self.relative_error, relative=True)

    def squared(self):
        return self.times(self)

    def cubed(self):
        return self.times(self).times(self)

    def to_the(self, constant):
        return ErrorNumber((self.value)**constant, self.relative_error, relative=True)

    def __str__(self):
        return "[value={}; error={}; relative_error={}]".format(self.value, self.absolute_error, self.relative_error)
