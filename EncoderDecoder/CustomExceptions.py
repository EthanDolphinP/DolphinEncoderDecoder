

class SecurityError(Exception):
    def __init__(self, err_msg = "Security Level To Low"):
        super().__init__(err_msg)
    def get_err_msg(self):
        return self.err_msg

class KeyError(Exception):
    def __init__(self, err_msg = "Key(s) are missing or not provided"):
        super().__init__(err_msg)
    def get_err_msg(self):
        return self.err_msg


if __name__ == "__main__":
    raise SecurityError
