from platform import system

# Checks if operating system is Windows as formatting for text doesn't work in Windows without windll.
if "wind" in system().lower():
    try:
        from ctypes import windll
        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except ImportError:
        windll = None
        print("\n\nImport error whilst attempting to import module[windll]. This should not cause a problem"
              " if using unix-based platforms. Contact author for help.")


class Colours:
    """Enum-styled selection of text formats"""

    BOLD = '\033[1m'
    NOTIFY = '\033[36m'
    PASS = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    END = '\033[0m'


class TerminalLog:
    """Prints styled text to console"""

    @staticmethod
    def bold(message):
        print(Colours.BOLD, message, Colours.END)

    @staticmethod
    def notify(message):
        print(Colours.NOTIFY, message, Colours.END)

    @staticmethod
    def confirm(message):
        print(Colours.PASS, message, Colours.END)

    @staticmethod
    def warning(message):
        print(Colours.WARNING, message, Colours.END)

    @staticmethod
    def fail(message):
        print(Colours.FAIL,
              message,
              '''\n\n===========================================================
                   \n                     ERROR: EXITING...
                   \n===========================================================''',
              Colours.END)

    @staticmethod
    def start():
        TerminalLog.bold("\n\nThis is NotSoFastQC!\n\tCreated by James Fox\n\n")

    @staticmethod
    def complete():
        TerminalLog.notify(
             '''\n\n===========================================================
                  \n    Analysis Complete. Thank you for using NotSoFastQC!
                  \n===========================================================''')
