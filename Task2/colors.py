class Tcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def warning(string: str):
        return f"{Tcolors.WARNING}{string}{Tcolors.ENDC}"

    @staticmethod
    def fail(string: str):
        return f"{Tcolors.FAIL}{string}{Tcolors.ENDC}"
