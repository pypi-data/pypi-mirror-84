import win32com.client


class COM:
    """COM Interface singleton implementation

    Program     | Prog ID
    ----------- | -------
    Solidworks  | SldWorks.Application
    Excel       | Excel.Application

    """

    class __COM:
        def __init__(self, prog_id):
            self.prog_id = prog_id
            self.com = win32com.client.Dispatch(self.prog_id)

    instance = None

    def __new__(cls, prog_id):
        if not cls.instance:
            cls.instance = cls.__COM(prog_id).com
        return cls.instance
