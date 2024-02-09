from typing import Literal
from pathlib import Path
from fakturyfy.settings import DATA_DIR


class History:
    def __init__(self, provider_abbrev: str, client_abbrev: str, year: int | Literal['all'] = 'all') -> None:
        assert year == 'all' or (isinstance(year, int) and year > 1900 and year < 9999)
        self.year = year
        self.provider_abbrev = self._sanitize(provider_abbrev)
        self.client_abbrev = self._sanitize(client_abbrev)
        self.history_dir = DATA_DIR / 'history' / f'{self.provider_abbrev}-{self.client_abbrev}'

    @staticmethod
    def _sanitize(fileneame: str) -> str:
        return "".join(filter(str.isalnum, str(fileneame).strip().lower()))

    @property
    def base_dir(self) -> Path:
        if self.year == 'all':
            return self.history_dir
        else:
            return self.history_dir / str(self.year)

    def get_all(self) -> list[Path]:
        """ Get all files in history directory for given year(s) """
        return list(self.base_dir.glob('**/*.pdf'))
        
    def get_count(self) -> int:
        """ Get count of files in history directory for given year(s) """
        return len(self.get_all())
