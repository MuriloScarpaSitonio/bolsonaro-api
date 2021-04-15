import MetaTags from 'react-meta-tags'
import { useLocation } from "react-router-dom"

import { SITE_URL } from "./consts"

import bozoQuote from "../images/bozoQuote.png"
import bozoAction from "../images/bozoAction.png"


export default function MetaData({ baseEndpoint, title, description }) {
    const SITE_NAME = "Bolsonaro API"
    let url = SITE_URL + useLocation().pathname
    let image = baseEndpoint === "actions" ? SITE_URL + bozoAction : SITE_URL + bozoQuote
    title = title || SITE_NAME
    description = description || "API pública de ações e declarações do presidente Bolsonaro e seu governo"

    return (
        <MetaTags>
            <title>{title}</title>
            <meta name="description" content={description} />

            <meta property="og:site_name" content={SITE_NAME} />
            <meta property="og:url" content={url} />
            <meta property="og:title" content={title} />
            <meta property="og:description" content={description} />
            <meta property="og:image" content={image} />
            <meta property="og:type" content="website" />
            <meta property="og:locale" content="pt_BR" />
            <meta property="fb:app_id" content="252038679634780" />

            <meta name="twitter:title" content={title} />
            <meta name="twitter:description" content={description} />
            <meta name="twitter:image" content={image} />
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:site" content="@ApiBolsonaro" />
        </MetaTags>
    )
}
