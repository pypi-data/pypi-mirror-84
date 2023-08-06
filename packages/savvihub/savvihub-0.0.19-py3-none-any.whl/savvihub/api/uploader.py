import os

from requests_futures.sessions import FuturesSession

from savvihub.api.file_object import FileObject
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.types import SavviHubFileObject
from savvihub.common.utils import wait_all_futures, calculate_crc32c


def default_hooks():
    def fn(resp, **kwargs):
        resp.raise_for_status()
    return {
        'response': fn,
    }


class Downloader:
    @classmethod
    def get_files_to_download(cls, context, volume_id, *, snapshot='latest', prefix=''):
        client = SavviHubClient(token=context.token)
        files = client.volume_file_list(volume_id, prefix=prefix, snapshot=snapshot, raise_error=True)
        return files

    @classmethod
    def parallel_download(cls, context, path, files, progressable=None):
        if len(files) <= 0:
            return
        session = FuturesSession(max_workers=context.parallel)
        futures = []
        for file in files:
            file_object = FileObject(file, path)
            if file.path.endswith('/'):
                continue

            progress_callback = None
            if progressable:
                progress = progressable(length=file_object.size, label=file_object.path)
                progress_callback = lambda data: progress.update(len(data))

            future = session.get(
                file.download_url.url,
                stream=True,
                hooks=file_object.download_hooks(callback=progress_callback)
            )
            futures.append(future)
        wait_all_futures(futures)


class Uploader:
    @classmethod
    def get_files_to_upload(cls, base_path, hashmap=None):
        results = []
        for root, dirs, files in os.walk(base_path):
            for name in files:
                name = os.path.join(os.path.abspath(root), name)
                name = name[len(base_path) + 1:] if name.startswith(base_path) else name
                if hashmap and hashmap[name] == calculate_crc32c(os.path.join(base_path, name)):
                    continue
                results.append(name)
        return results

    @classmethod
    def get_hashmap(cls, base_path):
        files = cls.get_files_to_upload(base_path)
        hashmap = dict()
        for file in files:
            path = os.path.join(base_path, file)
            hashmap[file] = calculate_crc32c(path)
        return hashmap

    @classmethod
    def parallel_upload(cls, context, base_path, files, volume_id, *, progressable=None):
        if len(files) <= 0:
            return

        session = FuturesSession(max_workers=context.parallel)
        client = SavviHubClient(token=context.token, session=session)

        futures = []
        for file in files:
            future = client.volume_file_create(
                volume_id,
                file,
                is_dir=False,
                hooks=default_hooks()
            )
            futures.append(future)
        resps = wait_all_futures(futures)

        futures = []
        for i, resp in enumerate(resps):
            file_object = FileObject(SavviHubFileObject(resp.json()), base_path)

            progress_callback = None
            if progressable:
                progress = progressable(length=os.path.getsize(file_object.full_path), label=file_object.path)
                progress_callback = lambda data: progress.update(len(data))

            future = session.put(
                file_object.upload_url.url,
                data=file_object.upload_chunks(callback=progress_callback),
                headers={
                    'content-type': 'application/octet-stream',
                },
                hooks=file_object.upload_hooks(),
            )
            futures.append(future)
        wait_all_futures(futures)

        futures = []
        for file in files:
            future = client.volume_file_uploaded(
                volume_id,
                file,
            )
            futures.append(future)
        wait_all_futures(futures)
