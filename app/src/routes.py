from services import server
from src.controllers.http.produtos.produtos_controller import ProdutosController
from src.controllers.http.autenticacao.autenticacao_controller import AutenticacaoController


server.api.add_resource(AutenticacaoController, '/autenticacao')
server.api.add_resource(ProdutosController, '/produtos/crud', '/produtos/crud/<uuid:hash_produto>')
