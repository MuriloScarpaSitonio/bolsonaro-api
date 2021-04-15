import React from "react";

import { Col, Container, Row } from "react-bootstrap"
import GitHubIcon from "@material-ui/icons/GitHub"
import MailIcon from '@material-ui/icons/Mail'
import TwitterIcon from "@material-ui/icons/Twitter"

import { ADMIN_EMAIL, BASE_API_URL } from "../consts"

import "./Footer.scss"


export default function Footer() {
    return (
        <section id="footer">
		<Container>
			<Row className="text-center text-xs-center text-sm-left text-md-left">
					<Col xs={12} sm={4}>
					<h5>Ações</h5>
					<ul className="list-unstyled quick-links">
						<li><a className="link" href="/actions">Home</a></li>
						<li><a className="link" href="/actions/query">Pesquise</a></li>
					</ul>
				</Col>
				<Col xs={12} sm={4}>
					<h5>Declarações</h5>
					<ul className="list-unstyled quick-links">
						<li><a className="link" href="/quotes">Home</a></li>
						<li><a className="link" href="/quotes/query">Pesquise</a></li>
					</ul>
				</Col>
				<Col xs={12} sm={4}>
					<h5>Mais informações</h5>
					<ul className="list-unstyled quick-links">
						<li><a className="link" href={`${BASE_API_URL}/docs/`}>Documentação da API</a></li>
						<li><a className="link" href='/contribute'>Contribua</a></li>
						<li><a className="link" href='/legal-infos'>Informações legais</a></li>
					</ul>
				</Col>
			</Row>
			<Row>
				<Col>
					<ul className="list-unstyled list-inline social text-center">
						<li className="list-inline-item">
							<a className="link" href="https://github.com/MuriloScarpaSitonio/bolsonaroAPI/">
								<GitHubIcon />
							</a>
						</li>
						<li className="list-inline-item">
								<a className="link" href={`mailto:${ADMIN_EMAIL}`}>
							<MailIcon />
						</a>
						</li>
						<li className="list-inline-item">
							<a className="link" href="https://twitter.com/ApiBolsonaro">
							<TwitterIcon />
							</a>
						</li>
					</ul>
				</Col>
			</Row>
		</Container>
	</section>
    )

}
