from pydantic import BaseModel
from typing import Optional, List
from model.disco import Disco

from schemas import MusicaSchema


class DiscoSchema(BaseModel):
    """ Define como um novo disco a ser inserido deve ser representado
    """
    artista: str = "Legião Urbana"
    titulo: str = "As quatro estações"
    gravadora: str = "EMI"
    quantidade_faixas: int = 11
    ano_lancamento: int = 1989
    origem: str = "Brasil"
    promo: str = "N"
    valor: float = 50.00
    observacao: str = "Capa original"


class DiscoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no título do disco.
    """
    titulo: str = 'Teste'


class ListagemDiscosSchema(BaseModel):
    """ Define como uma listagem de discos será retornada.
    """
    discos:List[DiscoSchema]


def apresenta_discos(discos: List[Disco]):
    """ Retorna uma representação do disco seguindo o schema definido em
        DiscoViewSchema.
    """
    result = []
    for disco in discos:
        result.append({
            "artista": disco.artista,
            "titulo": disco.titulo,
            "gravadora": disco.gravadora,
            "quantidade_faixas": disco.quantidade_faixas,
            "ano_lancamento": disco.ano_lancamento,
            "origem": disco.origem,
            "promo": disco.promo,
            "valor": disco.valor,
            "observacao": disco.observacao
        })

    return {"Discos": result}


class DiscoViewSchema(BaseModel):
    """ Define como um disco será retornado: disco + músicas.
    """
    id: int = 1
    artista: str = "Legião Urbana"
    titulo: str = "As quatro estações"
    gravadora: str = "EMI"
    quantidade_faixas: int = 11
    ano_lancamento: int = 1989
    origem: str = "Brasil"
    promo: str = "N"
    valor: float = 50.00
    observacao: str = "Capa original"
    total_musicas: int = 11
    musicas:List[MusicaSchema]


class DiscoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str


def apresenta_disco(disco: Disco):
    """ Retorna uma representação do disco seguindo o schema definido em
        DiscoViewSchema.
    """
    return{
        "id": disco.id,
        "artista": disco.artista,
        "titulo": disco.titulo,
        "gravadora": disco.gravadora,
        "quantidade de faixas": disco.quantidade_faixas,
        "ano de lançamento": disco.ano_lancamento,
        "origem": disco.origem,
        "promo": disco.promo,
        "valor": disco.valor,
        "Observação": disco.observacao,
        "total de musicas": len(disco.musicas),
        "musicas": [{"Tempo": c.tempo, "Nome Versão": c.nome_versao, "Nome Música": c.nome_musica} for c in disco.musicas]
    }