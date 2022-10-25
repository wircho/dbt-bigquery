from threading import Thread

import google.cloud.bigquery
import queue

DATASET_UPDATE_QUEUE = queue.SimpleQueue()
__DATASET_UPDATE_THREAD = {}


class DatasetAsyncUpdater(Thread):
    client: google.cloud.bigquery.Client

    def __init__(self, client):
        super().__init__()
        self.daemon = True
        self.client = client

    def run(self):
        while True:
            val = DATASET_UPDATE_QUEUE.get()
            if val:
                self.client.update_dataset(**val)


def start_dataset_update_thread(client):
    if "thread" in __DATASET_UPDATE_THREAD:
        dataset_update_thread: DatasetAsyncUpdater = __DATASET_UPDATE_THREAD["thread"]
        if not dataset_update_thread.is_alive():
            dataset_update_thread.start()
    dataset_update_thread = DatasetAsyncUpdater(client=client)
    dataset_update_thread.start()
    __DATASET_UPDATE_THREAD["thread"] = dataset_update_thread
