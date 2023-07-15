from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session, Disco, Musica
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="Cadastro de Discos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
disco_tag = Tag(name="Disco", description="Adição, visualização e remoção de discos na base")
musica_tag = Tag(name="Musica", description="Adição de uma música à um disco cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/disco', tags=[disco_tag],
          responses={"200": DiscoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_disco(form: DiscoSchema):
    """Adiciona um novo Disco à base de dados

    Retorna uma representação dos discos e músicas associadas.
    """
    disco = Disco(
        artista = form.artista,
        titulo = form.titulo,
        gravadora = form.gravadora,
        quantidade_faixas = form.quantidade_faixas,
        ano_lancamento = form.ano_lancamento,
        origem = form.origem,
        promo = form.promo,
        valor = form.valor,
        observacao = form.observacao)

    logger.debug(f"Adicionando disco de nome: '{disco.titulo}'")
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando disco
        session.add(disco)
        # efetivando o camando de adição de novo disco na tabela
        session.commit()
        logger.debug("Disco adicionado com sucesso!")
        return apresenta_disco(disco), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Disco com o mesmo título já salvo na base."
        logger.warning(f"Erro ao adicionar disco '{disco.titulo}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso aconteça um erro fora do previsto
        error_msg = "Não foi possível salvar novo disco."
        logger.warning(f"Erro ao adicionar disco '{disco.titulo}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/discos', tags=[disco_tag],
         responses={"200": ListagemDiscosSchema, "404": ErrorSchema})
def get_discos():
    """Faz a busca por todos os discos cadastrados

    Retorna uma representação da listagem de discos.
    """
    logger.debug(f"Coletando discos")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    discos = session.query(Disco).all()

    if not discos:
        # se não há discos cadastrados
        return {"discos": []}, 200
    else:
        logger.debug(f"Discos econtrados: %d" % len(discos))
        # retorna a representação do disco
        print(discos)
        return apresenta_discos(discos), 200


@app.get('/disco', tags=[disco_tag],
         responses={"200": DiscoViewSchema, "404": ErrorSchema})
def get_disco(query: DiscoBuscaSchema):
    """Faz a busca por um Disco a partir do título do disco

    Retorna uma representação dos discos e músicas associadas.
    """
    titulo_disco = query.titulo
    logger.debug(f"Coletando dados sobre o disco #{titulo_disco}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    disco = session.query(Disco).filter(func.lower(Disco.titulo) == func.lower(titulo_disco)).first()

    if not disco:
        # se o disco não foi encontrado
        error_msg = "Título não encontrado na base."
        logger.warning(f"Erro ao buscar disco com o título '{titulo_disco}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug("Título econtrado!")
        # retorna a representação do disco
        return apresenta_disco(disco), 200


@app.delete('/disco', tags=[disco_tag],
            responses={"200": DiscoDelSchema, "404": ErrorSchema})
def del_disco(query: DiscoBuscaSchema):
    """Deleta um Disco a partir do título informado

    Retorna uma mensagem de confirmação da remoção.
    """
    titulo_disco = unquote(unquote(query.titulo))
    print(titulo_disco)
    logger.debug(f"Deletando dados sobre o disco #{titulo_disco}")
    # criando conexão com a base
    session = Session()
    # busca o disco e as músicas associadas para remoção
    count = session.query(Disco).filter(func.lower(Disco.titulo) == func.lower(titulo_disco)).all()
    # fazendo a remoção
    # teve que ser implementada com "for", pois o session.delete só executa 1 delete por vez
    for item in count:
        session.delete(item)
    # efetiva a remoção
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug("Disco deletado com sucesso!")
        return {"message": "Disco removido", "Título": titulo_disco}
    else:
        # se o disco não foi encontrado
        error_msg = "Disco não encontrado na base."
        logger.warning(f"Erro ao deletar disco #'{titulo_disco}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/musica', tags=[musica_tag],
          responses={"200": DiscoViewSchema, "409": ErrorSchema, "404": ErrorSchema})
def add_musica(form: MusicaSchema):
    """Adiciona uma música à um disco cadastrado na base identificado pelo id

    Retorna uma representação dos discos e músicas associadas.
    """
    disco_id  = form.disco_id
    logger.debug(f"Adicionando música ao disco #{disco_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo disco
    disco = session.query(Disco).filter(Disco.id == disco_id).first()

    if not disco:
        # se o disco não for encontrado
        error_msg = f"Esta música não poderá ser incluída, pois o Disco com ID:'{disco_id}' não foi encontrado na base."
        logger.warning(f"Erro ao adicionar música ao disco '{disco_id}', {error_msg}")
        return {"message": error_msg}, 404

    # Obtendo a nova música
    nome_musica = form.nome_musica
    nome_versao = form.nome_versao
    tempo = form.tempo
    musica = Musica(nome_musica, nome_versao, tempo)

    # verificando se a música + versão já foi incluída no disco
    existe_musica = session.query(Musica).filter(Musica.disco_id == disco_id, \
                                                 Musica.nome_musica == nome_musica, \
                                                 Musica.nome_versao == nome_versao).first()

    if existe_musica:
        # A música + versão já foi incluída no disco
        error_msg = f"Música já incluída no Disco com ID:'{disco_id}'"
        logger.warning(f"Erro ao adicionar música ao disco '{disco_id}', {error_msg}")
        return {"message": error_msg}, 409        

    # adicionando a música ao disco
    disco.adiciona_musica(musica)
    session.commit()

    logger.debug(f"Música adicionada com sucesso!")

    # retorna a representação de produto
    return apresenta_disco(disco), 200