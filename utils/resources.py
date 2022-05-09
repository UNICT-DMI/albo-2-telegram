import os
from typing import List

def get_last_id (filename: str) -> int:
    with open(filename, "r") as f_id:
        last_id = int(f_id.read())

    return last_id

def get_cached_announcements(filename: str) -> List[int]:
    if not os.path.exists(filename):
        open(filename, "w").close()

    with open(filename, "r") as f_cached:
        cached_announcements = [int(cached_id) for cached_id in f_cached.read().splitlines()]

    return cached_announcements

def update_cached_announcements(cached_announcements: List[int], id: int, number_attachments: int) -> List[int]:
    if number_attachments == 0:
        if id not in cached_announcements:
            cached_announcements.append(id)
    else:
        if id in cached_announcements:
            cached_announcements.remove(id)
    return cached_announcements

def write_new_id(filename: str, new_id: int) -> None:
    with open(filename, "w+") as f_id:
        f_id.write(str(new_id))

def write_cached_announcements(filename: str, cached_announcements: List[int]) -> None:
    text = ''
    for cache_id in cached_announcements:
        text += str(cache_id) + '\n'
  
    with open(filename, "w+") as f_cached:    
        f_cached.write(text)
    
    