import React, { useEffect, useState } from "react"

import { Button, Container, Modal } from "react-bootstrap"
import { useParams } from "react-router-dom"

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import ActionForm from "../forms/ActionForm"
import QuoteForm from "../forms/QuoteForm"
import MetaData from "../MetaData"
import SocialShareButtons from "../common/SocialShareButtons"
import { BASE_API_URL } from "../consts"
import { convertDateStringLocaleToRegularFormat, getVariant, getDateString, toSlug } from "../helpers"

import "./Entity.scss"


function getAdjustedDateString(date, dateIsEstimated) {
    let quote_date = getDateString(date)
    quote_date = dateIsEstimated ? (quote_date + " (estimada)") : quote_date
    return quote_date
}

function getDynamicQuoteInfosHTML(entityProps, baseEndpoint) {
    let allQuoteInfosHTML = []
    for (const [prop, propInfos] of Object.entries(entityProps)) {
        let skippableProps = ["description", "isLoaded"]
        if (skippableProps.includes(prop)) {
            continue
        }
        if (propInfos.value) {
            let quoteInfosHTML = []
            quoteInfosHTML.push(<dt key={prop}>{propInfos.header}</dt>)
            if (prop === "date") {
                quoteInfosHTML.push(
                    <dd key={prop + "-child"}>
                        {getAdjustedDateString(
                            propInfos.value,
                            propInfos.isEstimated
                        )}
                    </dd>
                )
            }
            else if (propInfos.linkText !== undefined) {
                if (prop === "tags") {
                    for (var i = 0; i < propInfos.value.length; i++) {
                        let tag = propInfos.value[i]
                        quoteInfosHTML.push(
                            <dd key={prop + `-child-${i}`}>
                                <a className="link" href={`/${baseEndpoint}/query?tags=${toSlug(tag)}`}
                                    target="_blank"
                                    rel="noopener noreferrer">
                                    {tag}
                                </a>
                            </dd>)
                    }
                } else {
                    quoteInfosHTML.push(
                        <dd key={prop + "-child"}>
                            <a className="link" href={propInfos.value}
                                target="_blank"
                                rel="noopener noreferrer">
                                {propInfos.linkText}
                            </a>
                        </dd>)
                }
            }
            else {
                quoteInfosHTML.push(<dd key={prop + "-child"}>{propInfos.value}</dd>)
            }
            quoteInfosHTML.push(<hr />)
            allQuoteInfosHTML.push(quoteInfosHTML)
        }
    }

    return allQuoteInfosHTML

}

function getInitialValues(entityProps) {
    let initialValues = {
        id: Number(entityProps.id),
        description: entityProps.description,
        source: entityProps.source.value,
        tags: entityProps.tags.value,
        date: convertDateStringLocaleToRegularFormat(entityProps.date.value),
        date_is_estimated: entityProps.date.isEstimated,
        additional_infos: entityProps.additionalInfos.value ? entityProps.additionalInfos.value : ""
    }
    if (entityProps.fakeNewsSource) {
        initialValues.is_fake_news = entityProps.fakeNewsSource.value ? true : false
        initialValues.fake_news_source = entityProps.fakeNewsSource.value ? entityProps.fakeNewsSource.value : ""
    }
    return initialValues
}

function getEntityForm(entityProps) {
    return entityProps.fakeNewsSource ?
        <QuoteForm initialValues={getInitialValues(entityProps)} />
        : <ActionForm initialValues={getInitialValues(entityProps)} />


}

function ModalContainer({ entityProps }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <div className="d-flex justify-content-center">
                <Button variant={getVariant()} onClick={handleShow} size="lg">
                    Sugerir alterações
                </Button>
            </div>
            <Modal
                show={show}
                onHide={handleClose}
                size="lg"
            >
                <Modal.Header closeButton>
                    <Modal.Title>
                        Viu algum erro? Sugira uma mudança pra gente :)
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {getEntityForm(entityProps)}
                </Modal.Body>
            </Modal>
        </>
    )

}

function getEntityState(id, data) {
    let entityState = {
        isLoaded: true,
        id: id,
        description: data.description,
        additionalInfos: {
            value: data.additional_infos,
            header: "Informações adicionais:"
        },
        date: {
            value: data.date,
            header: "Quando:",
            isEstimated: data.date_is_estimated
        },
        source: {
            value: data.source,
            header: "Fonte:",
            linkText: "aqui"
        },
        tags: {
            value: data.tags,
            header: "Tags:",
            linkText: ""
        }
    }
    if (data.fake_news_source !== undefined) {
        entityState.fakeNewsSource = {
            value: data.fake_news_source,
            header: "Fake news?",
            linkText: "sim"
        }
    }
    return entityState
}

function getShareText(description, baseEndpoint) {
    const verb = baseEndpoint === "quotes" ? "falou" : "fez"
    const quote = baseEndpoint === "quotes" ? `"${description}"` : description
    return `Lembre-se do que Bolsonaro já ${verb}: ${quote}`
}

export default function Entity({ image, baseEndpoint }) {
    let { id } = useParams()
    const [entityProps, setEntityProps] = useState({})

    useEffect(() => {
        const fetchQuote = () => {
            fetch(`${BASE_API_URL}/${baseEndpoint}/${id}`)
                .then(response => {
                    if (!response.ok) {
                        response.json().then(
                            data => setEntityProps(() => ({
                                error: { message: data.errorMessage, badRequest: true }
                            }))
                        )
                    }
                    else {
                        response.json().then(
                            data => setEntityProps(() => getEntityState(id, data)),
                            error => setEntityProps(() => ({ isLoaded: true, error }))
                        )
                    }
                }
                )
                .catch(error => setEntityProps(() => ({ isLoaded: true, error })))
        }
        fetchQuote()
    }, [id, baseEndpoint])

    if(entityProps.error) return <Error message={entityProps.error.message}
                                        badRequest={entityProps.error.badRequest} />
    if (!entityProps.isLoaded) return <Loader />
    return (
            <>
                <MetaData baseEndpoint={baseEndpoint} description={entityProps.description} />
                <div className="text-center mb-4">
                    <a href={`/${baseEndpoint}`}><img src={image} alt={baseEndpoint} className='img' />
                    </a>
                </div>
                <Container className="entity__wrapper">
                    <blockquote className={baseEndpoint}>
                        <p>{entityProps.description}</p>
                    </blockquote>
                    <SocialShareButtons text={getShareText(entityProps.description, baseEndpoint)} />
                    <dl key="entity-props">
                        {getDynamicQuoteInfosHTML(entityProps, baseEndpoint)}
                    </dl>
                    <ModalContainer entityProps={entityProps} />
                </Container>
            </>
        );
}