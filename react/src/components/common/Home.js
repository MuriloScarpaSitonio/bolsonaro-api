import React, { Component } from "react"
import { Col, Row } from "react-bootstrap"

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { BASE_API_URL } from "../consts"

import "./Home.scss"

import bozoQuote from "../../images/bozoQuote.png"
import bozoAction from "../../images/bozoAction.png"


export default class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            actionsTotal: 0,
            quotesTotal: 0
        }
        this._fetchData()
    }

    _fetchData() {
        Promise.all([
            fetch(`${BASE_API_URL}/quotes/count`),
            fetch(`${BASE_API_URL}/actions/count`)
        ])
            .then(responses => Promise.all(responses.map(response => response.json())))
            .then(
                data => this.setState({ isLoaded: true, quotesTotal: data[0].total, actionsTotal: data[1].total }),
                error => this.setState({ isLoaded: true, error })
            )
            .catch(error => this.setState({ isLoaded: true, error }))
    }

    render() {
        if (this.state.error) <Error message={this.state.error.message} />
        if (!this.state.isLoaded) return <Loader />
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
                            Base de dados e <a className="link" href={`${BASE_API_URL}/docs`}>API</a> com {this.state.quotesTotal} declarações
                            e {this.state.actionsTotal} ações do presidente Bolsonaro.
                        </h5>
                    </Col>
                </Row>
            </>
        )
    }
}
