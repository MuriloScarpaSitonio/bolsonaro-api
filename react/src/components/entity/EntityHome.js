import React, { useState } from "react"
import { Col, Row } from "react-bootstrap"
import CachedIcon from '@material-ui/icons/Cached'
import IconButton from '@material-ui/core/IconButton'
import Cookies from 'universal-cookie'

import Error from "../static/Error"
import {Loader} from "../static/Loader"
import { useQuery } from "../hooks/useQuery"

import fakeNews from "../../images/fakeNews.png"

import "./EntityHome.scss"

const EntityInfos = ({baseEndpoint, image}) => {
    const [shouldFetch, setShouldFetch] = useState(true)
    const [data, isLoaded, error] = useQuery(`${baseEndpoint}/random`, shouldFetch, setShouldFetch)

    if (error) return <Error message={error} />
    if (!isLoaded) return <Loader />
    return (
        <>
            <div className="text-center mb-4">
                    <a href={`/${baseEndpoint}/${data.id}`}>
                        <img
                            src={image}
                            alt={`${baseEndpoint} main`}
                            className="img"
                        />
                        <img
                            src={fakeNews}
                            alt="fake-news"
                            className={`img__fake-news ${data.tags.includes("Fake news") ? "" : "d-none"}`}
                        />
                    </a>
                </div>
            <div className="entity__main-wrapper mt-3">
                <blockquote className={baseEndpoint}>
                    <p>{data.description}</p>
                </blockquote>
                <div className="text-center">
                    <IconButton id="reload-icon" onClick={() => setShouldFetch(true)}>
                        <CachedIcon fontSize="large" />
                    </IconButton>
                </div>
                <Row>
                    <Col xs={7} sm={7} md={9} lg={9} xl={9}>
                        <p className="entity__additional-infos">
                            {data.additional_infos}
                        </p>
                    </Col>
                    <Col xs={5} sm={5} md={3} lg={3} xl={3}>
                        <p className="entity__source">Fonte: <a className="link" href={data.source}
                            target="_blank" rel="noopener noreferrer">
                            aqui</a>
                        </p>
                    </Col>
                </Row>
            </div>
        </>
    )
}

export const EntityHome = (props) => {
    const [tags, isLoaded, error] = useQuery(`${props.baseEndpoint}/tags/main`)
    const cookies = new Cookies()
    cookies.set('tags', JSON.stringify(tags), {path: `/${props.baseEndpoint}/query`})

    const getTagsHTML = () => {
        let tagsHTML = []
        for (var i = 0; i < tags.length; i++) {
            tagsHTML.push(
                <a
                    key={tags[i].slug}
                    href={`/${props.baseEndpoint}/query?tags=${tags[i].slug}`}
                >
                    <div className="tag text-center">{tags[i].name}</div>
                </a>
            )
        }
        return tagsHTML
    }

    if (error) return <Error message={error.message} />
    if (!isLoaded) return <Loader />
    return (
            <>
                <EntityInfos baseEndpoint={props.baseEndpoint} image={props.image} />
                <hr />
                <Row className="d-flex justify-content-center mt-3">
                    <h3 className="text-center mb-3">
                        O que Bolsonaro {props.baseEndpoint === "quotes" ? "pensa" : "fez"} sobre...
                    </h3>
                    <Col md={10} className="d-flex flex-wrap justify-content-center">
                        {getTagsHTML()}
                    </Col>
                </Row>
            </>
        );
    }
