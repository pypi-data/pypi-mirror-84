from fwiffos.core import admin

class AdminCLI():
    def __init__(self):
        pass

    def list(self):
        r = admin.list_admins()
        print(r)
