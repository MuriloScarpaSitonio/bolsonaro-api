import { useLocation } from "react-router-dom"
import {
    FacebookShareButton,
    TwitterShareButton,
    WhatsappShareButton,

    FacebookIcon,
    TwitterIcon,
    WhatsappIcon,
} from "react-share"

import { SITE_URL } from "../consts"

import "./SocialShareButtons.css"


export default function SocialShareButtons({ text }) {
    let url = SITE_URL + useLocation().pathname
    return (
        <div className="d-flex justify-content-center social">
            <FacebookShareButton quote={text} url={url} >
                <FacebookIcon size={32} round bgStyle={{ fill: "#4e4e4e" }} />
            </FacebookShareButton>
            <WhatsappShareButton title={text} url={url} separator={"\n"}>
                <WhatsappIcon size={32} round bgStyle={{ fill: "#4e4e4e" }} />
            </WhatsappShareButton>
            <TwitterShareButton title={text + "\n\n"} url={url} via={"ApiBolsonaro"}>
                <TwitterIcon size={32} round bgStyle={{ fill: "#4e4e4e" }} />
            </TwitterShareButton>
        </div>
    )
}
