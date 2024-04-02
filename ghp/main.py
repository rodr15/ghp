import typer
import json
from .hp_repo import HpRepository

app = typer.Typer()

def _get_repos() -> set[HpRepository]:
     response = json.load(open('ghp/repositories.json', 'r'))
     return set([HpRepository.from_dict(repo) for repo in response])

def _get_repo(name: str) -> HpRepository:
    repos: set[HpRepository] = _get_repos()
    for repo in repos:
        if repo.name == name:
            return repo

def _save_repos(repos: set[HpRepository]) -> None:
    with open('ghp/repositories.json', 'w') as f:
        json.dump(list(repos), f, ensure_ascii=False, indent=4,cls= HpRepository.HpRepositoryEncoder)


@app.command()
def add_repo(name:str, path:str):
    repo: HpRepository = HpRepository(name, path, [])
    
    repos: set[HpRepository] = _get_repos()
    repos.add(repo)

    _save_repos(repos)
    
@app.command()
def configure():
    repos: set[HpRepository] = _get_repos()

    if(len(repos) == 0):
        typer.echo('No hay repositorios configurados')
        return
    
    msg = 'Selecciona un repositorio: \n'
    for i,repo in enumerate(repos):
        msg += f'{i}. {repo}\n'
    
    choice = list(repos)[int(typer.prompt(msg))]
    
    excluded_files:list = []
    while(True):
        typer.echo('Para salir escribe exit')
        file:str = typer.prompt('Ingresa un archivo ')

        if file.strip() == 'exit':
            break
        excluded_files.append(file)

    choice = choice.excluded_files.extend(excluded_files)
    
    _save_repos(repos)

@app.command()
def list():
    repos: set[HpRepository] = _get_repos()

    if(len(repos) == 0):
        typer.echo('No hay repositorios configurados')
        return
    
    for repo in repos:
        typer.echo(repo)
    
@app.command()
def pull_all():
    repos: set[HpRepository] = _get_repos()

    if(len(repos) == 0):
        typer.echo('No hay repositorios configurados')
        return
    
    for repo in repos:
        typer.echo(f'Pulling {repo}...')
        repo.repo.pull()


@app.command()
def diff(name:str):
    repo: HpRepository = _get_repo(name)
    typer.echo(repo.diff())

@app.command()
def status(name:str):
    repo: HpRepository = _get_repo(name)
    typer.echo(repo.status())