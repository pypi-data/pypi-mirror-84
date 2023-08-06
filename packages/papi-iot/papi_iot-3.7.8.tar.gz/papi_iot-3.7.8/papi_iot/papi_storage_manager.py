from papi_iot.papi_storage_online import OnlineStorage
from papi_iot.papi_storage_offline import OfflineStorage 

class StorageManager:
    
    def __init__(self):
        self.onlineStorage = OnlineStorage()
        self.offlineStorage = OfflineStorage()
    
