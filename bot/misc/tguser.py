from dataclasses import dataclass
from collections import namedtuple

Location = namedtuple('Location', 'lat, lon')


@dataclass
class TgUser:
    tg_id: int
    location: Location = None
