class NoMinesProvidedError(ValueError):
    def __init__(self):
        super().__init__("Either mines_count or mines must be provided")
