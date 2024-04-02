from typing import List
from typing import Any
from dataclasses import dataclass
import json
from git import Repo

@dataclass
class HpRepository:
    name: str
    path: str
    excluded_files: List[str]
    repo: Repo = None
    
    def __init__(self, name: str, path: str, excluded_files: List[str]) -> None:
        self.path = path
        self.name = name
        self.excluded_files = excluded_files
        self.repo = Repo(self.path)
    
    def pull(self):
        self.repo.git.execute('git pull --rebase --autostash')

    def diff_short(self):
        self.repo.git.execute('git diff --name-only')
    
    def diff(self):
        self.repo.git.execute('git diff')
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return f'{self.name}'

    @staticmethod
    def from_dict(obj: Any) -> 'HpRepository':
        _name = str(obj.get("name"))
        _path = str(obj.get("path"))
        _excluded_files = [y for y in obj.get("excluded_files")]
        return HpRepository(_name, _path, _excluded_files)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "excluded_files": self.excluded_files
        }
    
    class HpRepositoryEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, HpRepository):
                return obj.to_dict()
            return json.JSONEncoder.default(self, obj)

