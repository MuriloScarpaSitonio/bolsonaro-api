import { Col, Row } from "react-bootstrap"

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { useAsyncQuery } from "../hooks/useQuery"
import { BASE_API_URL } from "../consts"

import "./Home.scss"

import bozoQuote from "../../images/bozoQuote.png"
import bozoAction from "../../images/bozoAction.png"


export default function Home () {
    const [[quotes, actions], isLoaded, error] = useAsyncQuery(['quotes/count', 'actions/count'])
    
    if (error) <Error message={error.message} />
    if (!isLoaded) return <Loader />
    return (
            <>
            <Row className="my-4">
                <Col className="text-center">
                    <h1 className="mt-2">O que Bolsonaro já...</h1>
                </Col>
            </Row>
            <Row className="my-4">
                <Col className="text-center">
                    <a href="/quotes">
                        <img src={bozoQuote} alt="quote home" className="img sm home" />
                    </a>
                    <h3 className="mt-2">...falou?</h3>
                </Col>
                <Col className="text-center">
                    <a href="/actions">
                        <img src={bozoAction} alt="action home" className="img sm home" />
                    </a>
                    <h3 className="mt-2">...fez?</h3>
                </Col>
            </Row>
            <Row className="my-4">
                <Col className="text-center">
                    <h5 className="mt-2">
                        Base de dados e <a className="link" href={`${BASE_API_URL}/docs`}>API</a> com {quotes.total}
                        {''} declarações e {actions.total} ações do presidente Bolsonaro.
                    </h5>
                </Col>
            </Row>
        </>
    )
}

