from pydantic import BaseModel


class MusicaSchema(BaseModel):
    """ Define como uma nova música a ser inserida deve ser representada
    """
    disco_id: int = 1
    nome_musica: str = "Pais e filhos"
    nome_versao: str = "Album"
    tempo: str = "05:06"