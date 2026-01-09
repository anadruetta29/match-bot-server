class InvalidOptionError(Exception):
    def __init__(self, option_id):
        self.option_id = option_id
        super().__init__(f"Invalid option")
