import React, { Component, useState } from "react"
import { Col, Row } from "react-bootstrap"
import CachedIcon from '@material-ui/icons/Cached'
import IconButton from '@material-ui/core/IconButton'
import Cookies from 'universal-cookie'

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { BASE_API_URL } from "../consts"

import fakeNews from "../../images/fakeNews.png"

import "./EntityHome.scss"

const EntityInfos = ({ initialInfos, baseEndpoint, onReload }) => {
    const [infos, setInfos] = useState(initialInfos)
    const [error, setError] = useState(null)
    const [isLoaded, setIsLoaded] = useState(true)

    const reload = () => {
        setIsLoaded(false)
        fetch(`${BASE_API_URL}/${baseEndpoint}/random`)
            .then(response => {
                if (!response.ok) {
                    response.json().then(
                        data => setError(data.errorMessage)
                    )
                }
                else {
                    response.json().then(
                        data => {
                            onReload(data)
                            setInfos(data)
                            setIsLoaded(true)
                        },
                        error => {
                            setError(error)
                            setIsLoaded(true)
                        }
                    )
                }
            }
            )
            .catch(error => {
                setError(error)
                setIsLoaded(true)
            })
    }

    if (error) return <Error message={error} />
    if (!isLoaded) return <Loader />
    return (
        <div className="entity__main-wrapper mt-3">
            <blockquote className={baseEndpoint}>
                <p>{infos.description}</p>
            </blockquote>
            <div className="text-center">
                <IconButton id="reload-icon" onClick={reload}><CachedIcon fontSize="large" /></IconButton>
            </div>
            <Row>
                <Col xs={7} sm={7} md={9} lg={9} xl={9}>
                    <p className="entity__additional-infos">
                        {infos.additional_infos}
                    </p>
                </Col>
                <Col xs={5} sm={5} md={3} lg={3} xl={3}>
                    <p className="entity__source">Fonte: <a className="link" href={infos.source}
                        target="_blank" rel="noopener noreferrer">
                        aqui</a>
                    </p>
                </Col>
            </Row>
        </div>
    )
}

export default class EntityHome extends Component {
    constructor(props) {
        super(props)
        this.state = {
            error: null,
            isLoaded: false,
            entity: null,
            tags: null,
            isFakeNews: false,
        }
        this._fetchData()
    }

    _fetchData() {
        Promise.all([
            fetch(`${BASE_API_URL}/${this.props.baseEndpoint}/random`),
            fetch(`${BASE_API_URL}/${this.props.baseEndpoint}/tags/main`)
        ])
            .then(responses => Promise.all(responses.map(response => response.json())))
            .then(
                data => this.setState({
                    isLoaded: true,
                    entity: data[0],
                    tags: data[1],
                    isFakeNews: data[0].tags.includes("Fake news")
                }, this._setCookies),
                error => this.setState({ isLoaded: true, error })
            )
            .catch(error => this.setState({ isLoaded: true, error }))
    }

    _setCookies = () => {
        const cookies = new Cookies()
        cookies.set('tags', JSON.stringify(this.state.tags), {path: `/${this.props.baseEndpoint}/query`})
    }
    _getTagsHTML() {
        let tagsHTML = []
        for (var i = 0; i < this.state.tags.length; i++) {
            tagsHTML.push(
                <a
                    key={this.state.tags[i].slug}
                    href={`/${this.props.baseEndpoint}/query?tags=${this.state.tags[i].slug}`}
                >
                    <div className="tag text-center">{this.state.tags[i].name}</div>
                </a>
            )
        }
        return tagsHTML
    }

    handleEntityReload = data => {
        this.setState({ entity: data, isFakeNews: data.tags.includes("Fake news") })
    }

    render() {
        if (this.state.error) return <Error message={this.state.error.message} />
        if (!this.state.isLoaded) return <Loader />
        return (
            <>
                <div className="text-center mb-4">
                    <a href={`/${this.props.baseEndpoint}/${this.state.entity.id}`}>
                        <img
                            src={this.props.image}
                            alt={`${this.props.baseEndpoint} main`}
                            className="img"
                        />
                        <img
                            src={fakeNews}
                            alt="fake-news"
                            className={`img__fake-news ${this.state.isFakeNews ? "" : "d-none"}`}
                        />
                    </a>
                </div>
                <EntityInfos
                    initialInfos={this.state.entity}
                    baseEndpoint={this.props.baseEndpoint}
                    onReload={this.handleEntityReload}
                />
                <hr />
                <Row className="d-flex justify-content-center mt-3">
                    <h3 className="text-center mb-3">
                        O que Bolsonaro {this.props.baseEndpoint === "quotes" ? "pensa" : "fez"} sobre...
                    </h3>
                    <Col md={10} className="d-flex flex-wrap justify-content-center">
                        {this._getTagsHTML()}
                    </Col>
                </Row>
            </>
        );
    }
}
