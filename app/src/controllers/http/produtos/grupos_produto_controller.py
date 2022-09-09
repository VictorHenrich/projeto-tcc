from services import server
from services.database import Database
from services.api import Controller
from src.models import (
    Empresas,
    Usuarios,
    GruposProduto
)
from src.middlewares import (
    AutenticacaoMiddleware,
    ValidacaoCorpoRequisicaoMiddleware,
    ValidacaoParametrosRequisicaoMiddleware
)
from services.api.utils.responses import (
    Response,
    ResponseFailure,
    ResponseSuccess
)



database: Database = server.databases.get_database()



class GruposProdutoController(Controller):
    @AutenticacaoMiddleware.apply()
    def get(
        self,
        auth_company: Empresas,
        auth_user: Usuarios
    ) -> Response:
        try:
            with database.create_session() as session:
                grupos_localizados: GruposProduto = \
                    session\
                        .query(GruposProduto)\
                        .filter(
                            GruposProduto.id_empresa == auth_company.id
                        )\
                        .all()

        except Exception as error:
            return ResponseFailure(data=str(error))

        else:
            pass



