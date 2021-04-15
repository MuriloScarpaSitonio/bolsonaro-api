import { useState } from "react";

import { Button, Col, Container, Modal, Row, Tab, Tabs } from "react-bootstrap"

import { getVariant } from "../helpers"

import ActionForm from "../forms/ActionForm"
import QuoteForm from "../forms/QuoteForm"
import { PIX_KEY } from "../consts"

import "./Contribute.scss"



export const Contribute = () => {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <Row className="contribute mt-5" >
                <Col>
                    <h5 className="text-center mb-4">Você pode contribuir com este projeto de três maneiras:</h5>
                    <div className="contribute ml-5">
                        <ol>
                            <li>
                                <strong>Doações</strong>: Manter este site e seus serviços ativos custa {''}
                                <strong>$$$$</strong>. Logo, toda e qualquer {''}
                                <strong className="link" onClick={handleShow}>doação</strong> é muito bem-vinda :)
                        </li>
                            <li>
                                <strong>Correções</strong>: Viu alguma informação errada? Clique no botão
                            <Button variant={getVariant()} size="sm">Sugerir alterações</Button>, na página de uma declaração ou ação,
                            que avaliaremos e, eventualmente, ajustaremos as informações.
                        </li>
                            <li>
                                <strong>Inclusões</strong>: Selecione "Declaração" ou "Ação" e preencha as informações.
                        </li>
                        </ol>
                    </div>
                </Col>
                <Modal
                    show={show}
                    onHide={handleClose}
                    size="lg"
                >
                <Modal.Header closeButton>
                    <Modal.Title>Muito obrigado por contribuir!</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className='text-center'>
                        <h4>Faça um PIX com qualquer valor para a chave <strong>{PIX_KEY}</strong></h4>
                        <br />
                        <h4>Obrigado mais uma vez!</h4>
                    </div>
                </Modal.Body>
            </Modal>
            </Row>
            <Row>
                <Col>
                    <Tabs defaultActiveKey="quote" transition={false} id="tabs">
                        <Tab eventKey="quote" title="Declaração">
                            <Container className="my-4 ml-3">
                                <QuoteForm />
                            </Container>
                        </Tab>
                        <Tab eventKey="action" title="Ação">
                            <Container className="my-4 ml-3">
                                <ActionForm />
                            </Container>
                        </Tab>
                    </Tabs>
                </Col>
            </Row>
        </>

    )
}
