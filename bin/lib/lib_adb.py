from ppadb.client import Client as AdbClient

class LibAdb():
    def __init__(self):
        pass


    def list_adb(self):
        data_adb = []
        client = AdbClient(host="127.0.0.1", port=5037)
        if client.devices() != []:
            for name in client.devices():
                data_adb.append(name.serial)
        return data_adb




