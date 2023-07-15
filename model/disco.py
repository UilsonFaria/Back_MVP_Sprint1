from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Musica


class Disco(Base):
    __tablename__ = 'discos'

    id = Column("pk_disco", Integer, primary_key=True)
    artista = Column(String(250))
    titulo = Column(String(250), unique=True)
    gravadora = Column(String(100))
    quantidade_faixas = Column(Integer)
    ano_lancamento = Column(Integer)
    origem = Column(String(50))
    promo = Column(String(1))
    valor = Column(Float)
    observacao = Column(String(1000))

    # Definição do relacionamento entre o disco e as músicas contidas em cada disco.
    # Essa relação é implicita, não está salva na tabela 'discos',
    # Fica para SQLAlchemy a responsabilidade de reconstruir esse relacionamento.
    musicas = relationship('Musica', backref="disco", cascade='all, delete, delete-orphan')

    def __init__(self, 
                artista:str, 
                titulo:str, 
                gravadora:str, 
                quantidade_faixas:int, 
                ano_lancamento:int,
                origem:str,
                promo:str,
                valor:float,
                observacao:str):
        """
        Cria um Disco

        Arguments:
            artista: nome do artista 
            titulo: titulo do disco
            gravadora: nome da gravadora do disco
            quantidade_faixas: quantidade de faixas do disco 
            ano_lancamento: ano de lançamento do disco
            origem: país de origem 
            promo: flag que indica se o disco é promocional ou não ("S" ou "N")
            valor: valor do disco para venda
            observacao: observações sobre o disco
        """
        self.artista = artista 
        self.titulo = titulo
        self.gravadora = gravadora 
        self.quantidade_faixas = quantidade_faixas 
        self.ano_lancamento = ano_lancamento
        self.origem = origem
        self.promo = promo
        self.valor = valor
        self.observacao = observacao


    def adiciona_musica(self, musica:Musica):
        """ Adiciona uma nova música ao disco
        """
        self.musicas.append(musica)