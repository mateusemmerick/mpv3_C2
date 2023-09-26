from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Float
from model.base import Base

class VendasProduto(Base):
    __tablename__ = 'vendas'

    id = Column("pk_produto", Integer, primary_key=True)        
    modelo = Column(String(50))
    id_estoque = Column(Integer)
    preco = Column(Float)
    custo_frete = Column(Float)
    cep_origem = Column(String(8))
    cep_destino = Column(String(8))
           
    def __init__(self, modelo:str, id_estoque:int, preco:float, custo_frete:float, cep_origem:int, cep_destino:int):    
        """
        Cadastra um produto vendido na tabela de vendas

        Argumentos:        
        id: id do produto na base de vendas
        modelo: modelo do iphone
        id_estoque: id do produto no banco de dados de estoque
        preco: preco de venda do produto
        custo_frete: custo do frete
        cep_origem: cep do vendedor
        cep_destino: cep do comprador       
    
        """        
        self.modelo = modelo
        self.id_estoque = id_estoque
        self.preco = preco
        self.custo_frete = custo_frete
        self.cep_origem = cep_origem
        self.cep_destino = cep_destino