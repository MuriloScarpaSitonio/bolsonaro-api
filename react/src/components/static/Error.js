import { ADMIN_EMAIL } from "../consts"

import "./Error.css"

function Error({ badRequest, message }) {
    if (badRequest) {
        return (
            <div className="error__wrapper mt-5">
                <div className="my-1">
                    <h3>Solicitação inválida</h3>
                </div>
                <div className="my-1">
                    <h4 className="error__strong">Erro: {message}</h4>
                </div>
            </div>
        )
    }
    return (
        <div className="error__wrapper mt-5">
            <div className="my-1">
                <div><h4>Um erro inesperado aconteceu :(</h4></div>
                <h4>Por favor, volte em alguns minutos.</h4>
            </div>
            <div className="my-4">
                <h5>
                    Caso queira ajudar a solucionar este problema mais rapidamente, envie um
                        e-mail para <a href={`mailto:${ADMIN_EMAIL}`}>{ADMIN_EMAIL}</a> com a mensagem abaixo:
                    </h5>
            </div>
            <div className="my-1">
                <h5 className="error__strong">Erro: {message}</h5>
            </div>
        </div>
    )
}

Error.defaultProps = {
    badRequest: false,
}

export default Error