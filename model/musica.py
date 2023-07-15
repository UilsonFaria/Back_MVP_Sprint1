from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Musica(Base):
    __tablename__ = 'musicas'

    id = Column(Integer, primary_key=True)
    nome_musica = Column(String(250))
    nome_versao = Column(String(250))
    tempo = Column(String(5))

    # Definição do relacionamento entre a música e o disco.
    # Definido a coluna 'disco_id' que vai guardar
    # a referencia ao disco que a música pertence.
    # A chave estrangeira que relaciona um disco à música.
    disco_id = Column(Integer, ForeignKey('discos.pk_disco'), nullable=False)
    

    def __init__(self, 
                nome_musica:str, 
                nome_versao:str,
                tempo:str):
        """
        Cria uma Música

        Arguments:
            nome_musica: nome da música
            nome_versao: nome da versão da música
            tempo: Tempo de duração da música
        """
        self.nome_musica = nome_musica
        self.nome_versao = nome_versao
        self.tempo = tempo