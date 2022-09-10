from services import server
from src.controllers.http.produtos import (
    CrudProdutosController,
    CrudGruposProdutoController
)

from src.controllers.http.autenticacao import AutenticacaoController


server.api.add_resource(AutenticacaoController, '/autenticacao')
server.api.add_resource(CrudProdutosController, '/produtos/crud', '/produtos/crud/<uuid:hash_produto>')
server.api.add_resource(CrudGruposProdutoController, '/grupos_produto/crud', '/grupos_produto/crud/<uuid:hash_grupo>')
