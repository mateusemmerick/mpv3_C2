import sys
sys.path.append('meu_app_api\model')
from pydantic import BaseModel
from typing import Optional, List
from model.vendas import VendasProduto


class VendasSchema(BaseModel):
    """ Define como uma nova entrada na tabela de vendas deve ser representada
    """   
    id: int = 1  
    modelo: str = "iPhone 11 256 Gb Excelente 95%"
    id_estoque: int = 1
    preco: float = 2300
    custo_frete: float = 27.90
    cep_origem: str = "01025020"
    cep_destino: str = "89258000"
  

class VendasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será feita apenas com base no id do produto
    """
    id: int = 1


class ListagemVendasSchema(BaseModel):
    """ Define como uma listagem de produtos vendidos será retornada.
    """
    venda:List[VendasSchema]


def apresenta_vendas(venda: List[VendasSchema]):
    """ Retorna uma representação do produto vendido seguindo o schema definido em
        VendasSchema.
    """
    result = []
    for prod in venda:
        result.append({
            "id": prod.id,
            "modelo": prod.modelo,
            "id_estoque": prod.id_estoque,
            "preco": prod.preco,
            "custo_frete": prod.custo_frete,            
            "cep_origem": prod.cep_origem,
            "cep_destino": prod.cep_destino,    
        })

    return {"vendas": result}


class ProdutoViewSchema(BaseModel):
    """ Define como uma entrada de um produto será retornada
    """   
    id: int = 1
    modelo: str = "iPhone 11 256 Gb Excelente 95%"
    id_estoque: int = 1
    preco: float = 2300
    custo_frete: float = 27.90
    cep_origem: str = "01025020"
    cep_destino: str = "89258000"

class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

def apresenta_venda(prod: VendasProduto):
    """ Retorna uma representação da entrada do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id":prod.id,
        "modelo": prod.modelo,
        "id_estoque": prod.id_estoque,
        "preco": prod.preco,
        "custo_frete": prod.custo_frete,            
        "cep_origem": prod.cep_origem,
        "cep_destino": prod.cep_destino,    
    }