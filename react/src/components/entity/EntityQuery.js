import React, { Component, Fragment, useState } from "react"

import { Accordion, Button, Container, useAccordionToggle } from "react-bootstrap"

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { QueryForm } from "../forms/QueryForm"
import { BASE_API_URL } from "../consts"
import { getVariant, getDateString } from "../helpers"

import "./EntityQuery.scss"


const Entities = ({ data, baseEndpoint }) => {
    let entitiesHTML = []
    for (var i = 0; i < data.length; i++) {
        let entityDate = getDateString(data[i].date)
        entitiesHTML.push(
            <Fragment key={data[i].id}>
                <blockquote className={baseEndpoint}>
                    <p>{data[i].description}</p>
                    <footer className="d-flex justify-content-end">
                        <cite> - <a className="link" href={`/${baseEndpoint}/${data[i].id}`}>
                            {entityDate}</a>
                        </cite>
                    </footer>
                </blockquote>
            </Fragment>
        )
    }
    if (entitiesHTML.length > 0) {
        entitiesHTML
            .map(entity => <span>{entity}</span>)
            .reduce((prev, curr) => [prev, <hr />, curr])
    }
    else {
        let entityVerbosName = baseEndpoint === "quotes" ? "declaração" : "ação"
        entitiesHTML = (
            <div className="error__wrapper mt-5">
                <h3 className="error__strong">Nenhuma {entityVerbosName} encontrada com os filtros selecionados...</h3>
            </div>
        )
    }
    return <div className="entities">{entitiesHTML}</div>

}

const LoadMore = ({hasMore,fetchMore}) => {
    const [isLoaded, setisLoaded] = useState(true)

    const handleClick = () => {
        setisLoaded(false)
        fetchMore()
        setisLoaded(true)
    }

    if (!isLoaded) return <Loader />
    return (
        hasMore ? (
            <div className="d-flex justify-content-center">
                <Button variant={getVariant()} size="lg" onClick={handleClick}>
                    Carregar mais
                </Button>
            </div>
        ) : null
    )
}

function CustomToggle({eventKey}) {
    const [children, setChildren] = useState('Mais filtros 🠗')
    const decoratedOnClick = useAccordionToggle(eventKey, () =>
        setChildren(children === 'Mais filtros 🠗' ? 'Menos filtros 🠕' : 'Mais filtros 🠗')
    )
  
    return (
        <div className="text-center">
            <div className="tag text-center" onClick={decoratedOnClick}>
                {children}
            </div>
        </div>
    )
  }

export default class EntityQuery extends Component {
    constructor(props) {
        super(props)
        this.state = {
            error: null,
            isLoaded: false,
            hasMore: false,
            searchParams: { page: 1, tags: '', description: '' },
            entities: []
        }
    }
    
    componentDidMount() {
        this.setInitialSearchParams()
    }

    setInitialSearchParams = () => {
        let initialTag = this.props.location.search.includes("tags")
          ? this.props.location.search.split("?tags=")[1]
          : ""
        let initialText = this.props.location.search.includes("description")
          ? this.props.location.search.split("?description=")[1]
          : ""
    
          this.setState({
            searchParams: { page: 1, tags: initialTag, description: initialText },
            isLoaded: false,
            entities: []
        }, this.fetchMore)
      }
    
    componentDidUpdate(prevProps) {
        if (prevProps.location.search.split("?description=")[1] !==
            this.props.location.search.split("?description=")[1]) {
                this.setInitialSearchParams()
        }
        
    }

    setSearchParams = (params) => {
        this.setState({ searchParams: params, isLoaded: false, entities: [] })
        this.fetchMore()
    }

    fetchMore = () => {
        let url = `${BASE_API_URL}/${this.props.baseEndpoint}?`
        fetch(url + new URLSearchParams(this.state.searchParams).toString())
            .then(response => {
                if (!response.ok) {
                    response.json().then(
                        data => {
                            this.setState({
                                error: { message: data.errorMessage, badRequest: true },
                            })
                        }
                    )
                }
                else {
                    response.json().then(
                        data => {
                            this.setState({
                                isLoaded: true,
                                entities: [...this.state.entities, ...data.results],
                                hasMore: data.hasMore,
                                searchParams: {...this.state.searchParams, page: this.state.searchParams.page + 1}
                            })
                        },
                        error => {
                            this.setState({
                                isLoaded: true,
                                error
                            })
                        }

                    )
                }
            })
    }

    _getEntities = () => {
        if (this.state.error) {
            return <Error message={this.state.error.message} badRequest={this.state.error.badRequest} />
        }
        if(!this.state.isLoaded) return <Loader />

        return <Entities data={this.state.entities} baseEndpoint={this.props.baseEndpoint} />
    }

    render() {
        return (
            <Container>
                <a href={`/${this.props.baseEndpoint}`}>
                        <img
                            className='img sm' src={this.props.image}
                            alt={`${this.props.baseEndpoint} query`}
                        />
                    </a>
                <div className="text-center mb-4">
                    <h3 className='text-center mt-4'>
                        PESQUISAR {this.props.baseEndpoint === "quotes" ? "DECLARAÇÕES" : "AÇÕES"}
                    </h3>
                </div>
                <Accordion>
                    <CustomToggle eventKey="0" />
                    <Accordion.Collapse eventKey="0">
                        <QueryForm
                            baseEndpoint={this.props.baseEndpoint}
                            tagsInitialValues={this.state.searchParams.tags}
                            textInitialValue={this.state.searchParams.description}
                            setSearchParams={this.setSearchParams}
                        />
                    </Accordion.Collapse>
                </Accordion>
                <hr/>
                {this._getEntities()}
                <LoadMore hasMore={this.state.hasMore} fetchMore={this.fetchMore} />
            </Container>
        )
    }
}


