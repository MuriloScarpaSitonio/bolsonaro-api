import React, { useState } from "react"

import { Button, Container, Modal } from "react-bootstrap"
import { useParams } from "react-router-dom"

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { ActionForm } from "../forms/ActionForm"
import { QuoteForm } from "../forms/QuoteForm"
import MetaData from "../MetaData"
import SocialShareButtons from "../common/SocialShareButtons"
import { useQuery } from "../hooks/useQuery"
import { convertDateStringLocaleToRegularFormat, getVariant, getDateString, toSlug } from "../helpers"

import "./Entity.scss"


function getAdjustedDateString(date, dateIsEstimated) {
    let quote_date = getDateString(date)
    quote_date = dateIsEstimated ? (quote_date + " (estimada)") : quote_date
    return quote_date
}

function getDynamicQuoteInfosHTML(data, baseEndpoint) {
    let entityAdjustedData = getEntityAdjustedData(data)
    let allQuoteInfosHTML = []

    for (const [prop, propInfos] of Object.entries(entityAdjustedData)) {
        if (prop === "description") continue
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

function getInitialValues(data) {
    data.date = convertDateStringLocaleToRegularFormat(data.date)
    data.additional_infos = data.additional_infos || ""

    if (data.fake_news_source) {
        data.is_fake_news = data.fake_news_source || false
        data.fake_news_source = data.fake_news_source || ""
    }
    return data
}

function getEntityForm(data) {
    return 'fake_news_source' in data ?
        <QuoteForm initialValues={getInitialValues(data)} />
        : <ActionForm initialValues={getInitialValues(data)} />


}

function ModalContainer({ data }) {
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
                    {getEntityForm(data)}
                </Modal.Body>
            </Modal>
        </>
    )

}

function getEntityAdjustedData(data) {
    let entityAdjustedData = {
        id: data.id,
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
        entityAdjustedData.fakeNewsSource = {
            value: data.fake_news_source,
            header: "Fake news?",
            linkText: "sim"
        }
    }
    return entityAdjustedData
}

function getShareText(description, baseEndpoint) {
    const verb = baseEndpoint === "quotes" ? "falou" : "fez"
    const quote = baseEndpoint === "quotes" ? `"${description}"` : description
    return `Lembre-se do que Bolsonaro já ${verb}: ${quote}`
}

export default function Entity({ image, baseEndpoint }) {
    let { id } = useParams()
    const [data, isLoaded, error] = useQuery(`${baseEndpoint}/${id}`)

    if(error) return <Error message={error.message} badRequest={error.badRequest} />
    if (!isLoaded) return <Loader />
    return (
            <>
                <MetaData baseEndpoint={baseEndpoint} description={data.description} />
                <div className="text-center mb-4">
                    <a href={`/${baseEndpoint}`}><img src={image} alt={baseEndpoint} className='img' />
                    </a>
                </div>
                <Container className="entities__list">
                    <blockquote className={baseEndpoint}>
                        <p>{data.description}</p>
                    </blockquote>
                    <SocialShareButtons text={getShareText(data.description, baseEndpoint)} />
                    <dl key="entity-props">
                        {getDynamicQuoteInfosHTML(data, baseEndpoint)}
                    </dl>
                    <ModalContainer data={data} />
                </Container>
            </>
        );
}