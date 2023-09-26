from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError


from model import Session, VendasProduto
from logger import logger
from schemas import *
from flask_cors import CORS, cross_origin

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Documentação em Swagger")
vendas_tag = Tag(name="Vendas ", description="Adição, visualização, edição e remoção de produtos a tabela de vendas")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, que é a documentação swagger.
    """
    return redirect('/openapi/swagger')


@app.get('/vendas', tags=[vendas_tag],
         responses={"200": ListagemVendasSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os produtos vendidos.

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(VendasProduto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d produtos encontrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_vendas(produtos), 200

@app.get('/produto', tags=[vendas_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: VendasBuscaSchema):
    """Faz a busca por um produto vendido a partir do id.

    Retorna uma representação do produto.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(VendasProduto).filter(VendasProduto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.modelo}'")
        # retorna a representação de produto
        return apresenta_venda(produto), 200

@app.post('/venda', tags=[vendas_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: VendasSchema):
    """Adiciona um novo produto a tabela vendas.

    Retorna uma representação do produto.
    """
    produto = VendasProduto(        
        modelo = form.modelo,
        id_estoque = form.id_estoque,
        preco = form.preco,
        custo_frete = form.custo_frete,
        cep_origem = form.cep_origem,
        cep_destino = form.cep_destino) 

    logger.debug(f"Adicionando venda: '{produto.modelo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado venda: '{produto.modelo}'")
        return apresenta_venda(produto), 200

    except IntegrityError as e:
        # como a duplicidade do código é a provável razão do IntegrityError
        error_msg = "Produto de mesmo código já salvo na base:/"
        logger.warning(f"Erro ao adicionar produto '{produto.modelo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo item:/"
        logger.warning(f"Erro ao adicionar produto '{produto.modelo}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.delete('/venda', tags=[vendas_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: VendasBuscaSchema):
    """Deleta um registro de venda a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    id_produto = query.id
    print(id_produto)
    logger.debug(f"Deletando dados sobre produto #{id_produto}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(VendasProduto).filter(VendasProduto.id == id_produto).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado venda de id {id_produto}")
        return {"mesage": "Venda removida", "id": id_produto}
    else:
        # se o produto não foi encontrado
        error_msg = "Venda não encontrada na base:/"
        logger.warning(f"Erro ao deletar produto código '{id_produto}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.put('/venda/<string:id>', tags=[vendas_tag],
            responses={"200":ProdutoViewSchema, "404":ErrorSchema})
def merge_produto(path:VendasBuscaSchema, form:VendasSchema):
    """Edita uma venda, com base no id.

    Retorna uma representação do produto.
    """
    produto = VendasProduto(
        modelo = form.modelo,
        id_estoque = form.id_estoque,
        preco = form.preco,
        custo_frete = form.custo_frete,
        cep_origem = form.cep_origem,
        cep_destino = form.cep_destino) 
    
    logger.debug(f"Editando venda: '{produto.modelo}'")
    try:
        # criando conexão com a base
        session = Session()
        vendaUpdate = session.query(VendasProduto).get(path.id) 
        vendaUpdate.modelo = form.modelo
        vendaUpdate.id_estoque = form.id_estoque        
        vendaUpdate.preco = form.preco     
        vendaUpdate.custo_frete = form.custo_frete     
        vendaUpdate.cep_origem = form.cep_origem     
        vendaUpdate.cep_destino = form.cep_destino     
        # atualizando venda
        session.commit()
        logger.debug(f"Atualizado venda: '{produto.modelo}'")
        return apresenta_venda(produto), 200

    except IntegrityError as e:
        # como a duplicidade do código é a provável razão do IntegrityError
        error_msg = "Produto de mesmo código já salvo na base:/"
        logger.warning(f"Erro ao adicionar produto '{produto.modelo}', {error_msg}")
        return {"mesage": 'error_msg'}, 409

    except Exception as e:
        # # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item:/"
        # logger.warning(f"Erro ao adicionar produto '{produto.modelo}', {error_msg}")
        logger.warning(f"Erro: {e} \n")
        return {"mesage": error_msg}, 400