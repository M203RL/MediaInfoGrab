import time
import asyncio
import json
import sys
import subprocess
import pkg_resources

required = {'winsdk'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

    
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import \
    InputStreamOptions

async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)

async def get_media_info():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:  
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

def run():
    while True:
        current_media_info = asyncio.run(get_media_info())
        title = current_media_info['title']
        artist = current_media_info['artist']
        data = {}
        data['title'] = title
        data['artist'] = artist
        jsonFile = open("./js/musicinfo.json", "w")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        time.sleep(1)


if __name__ == '__main__':
    run()
