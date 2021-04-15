import React, { Component, createRef, useState } from "react"

import ReCAPTCHA from "react-google-recaptcha"
import { Field, Formik } from "formik"
import * as yup from "yup"
import { Button, Col, Form, Modal, Row } from "react-bootstrap"

import actionFormData from "./actionFormData"
import Error from "../static/Error"
import { Loader } from "../static/Loader"
import TagsInput from "./TagsInput"
import { BASE_API_URL, RECAPTCHA_SITE_KEY } from "../consts"
import {
    convertDateStringToLocaleFormat,
    createYupSchema,
    getVariant,
    getCookie,
    formHasChanges
} from "../helpers"

import "./Forms.scss"


const CustomSwitch = ({ name, setFieldValue, value }) => {
    const [label, setLabel] = useState(value ? "Sim" : "Não")
    return (
        <Form.Switch
            name={name}
            label={label}
            id={`custom-switch-${name}`}
            checked={value}
            value={value}
            onChange={() => label === "Não" ? setLabel("Sim") : setLabel("Não")}
            onClick={(e) => setFieldValue(name, e.target.checked)}
        />
    )
}



export default class ActionForm extends Component {
    constructor(props) {
        super(props)
        //if the form has initialValues, it means a suggestion to change an Action
        this.isChangeForm = this.props.initialValues ? true : false
        this.data = actionFormData
        this.state = {
            error: null,
            isLoaded: false,
            submissionError: { value: false, text: "" },
            submitted: false,
            tags: null
        }

        if (this.isChangeForm) {
            //if the form has initialValues, it means a suggestion to change an Action
            this.data.push({
                id: "justification",
                type: "text",
                validationType: "string",
                validations: [
                    {
                        type: "required",
                        params: ["*A justificativa é obrigatória."]
                    },
                ]
            })
        }
        this.validationSchema = yup.object().shape(this.data.reduce(createYupSchema, {}))

        this._initialValues = this.isChangeForm ?
            { ...this.props.initialValues, user_email: "", recaptcha: "", justification: "" }
            : {
                user_email: "",
                description: "",
                source: "",
                tags: "",
                date: "",
                date_is_estimated: false,
                additional_infos: "",
                recaptcha: ""
            }
        this._reCaptchaRef = createRef()
        this._fetchTagsWhitelist()
    }

    _fetchTagsWhitelist() {
        fetch(`${BASE_API_URL}/actions/tags`)
            .then(response => {
                if (!response.ok) {
                    response.json().then(
                        data => {
                            this.setState({
                                isLoaded: true,
                                error: { message: data.errorMessage }
                            })
                        }
                    )
                }
                else {
                    response.json().then(
                        data => this.setState({ isLoaded: true, tags: data.map(tag => tag.name) }),
                        error => this.setState({ isLoaded: true, error })
                    )
                }
            })
            .catch(error => {
                this.setState({ isLoaded: true, error })
            })
    }

    onClick = () => this.setState({ submissionError: { value: false, text: "" }, submitted: false })

    render() {
        if (this.state.error) return <Error message={this.state.error.message} />
        if(!this.state.isLoaded) return <Loader />
        return (
            <Formik
                validationSchema={this.validationSchema}
                initialValues={this._initialValues}
                onSubmit={(values, { setSubmitting, resetForm }) => {
                    setSubmitting(true)
                    if (formHasChanges(values, this._initialValues)) {
                        fetch(this.isChangeForm ?
                            `${BASE_API_URL}/actions/${values.id}/change` :
                            `${BASE_API_URL}/actions/suggest`,
                            {
                                method: "POST",
                                headers: {
                                    "Accept": "application/json",
                                    "Content-Type": "application/json",
                                    "X-CSRFToken": getCookie("csrftoken")
                                },
                                body: JSON.stringify({...values, date: convertDateStringToLocaleFormat(values.date)}),
                            }
                        )
                            .then(response => {
                                if (!response.ok) {
                                    response.json().then(
                                        response => {
                                            setSubmitting(false)
                                            this.setState({
                                                submissionError: {
                                                    value: true,
                                                    text: "Requisição inválida!\n" + JSON.stringify(response)
                                                }
                                            })
                                            this.setState({ submitted: true })
                                        }
                                    )
                                }
                                else {
                                    response.json().then(_ => {
                                        setSubmitting(false)
                                        this.setState({ submitted: true })
                                        resetForm()
                                    })
                                        .catch(_ => {
                                            setSubmitting(false)
                                            this.setState({
                                                submissionError: {
                                                    value: true,
                                                    text: (
                                                        `Tivemos um erro na hora de processar sua solicitação! 
                                                    Por favor, feche esta caixa e tente enviar a sugestão novamente.`
                                                    )
                                                }
                                            })
                                            this.setState({ submitted: true })
                                        })
                                }
                            })
                    }
                    else {
                        setSubmitting(false)
                        this.setState({
                            submissionError: {
                                value: true,
                                text: "Sua sugestão precisa alterar pelo menos um campo!"
                            }
                        })
                    }
                }
                }
            >
                {({
                    handleBlur,
                    handleChange,
                    handleSubmit,
                    setFieldValue,
                    values,
                    touched,
                    errors,
                    isSubmitting
                }) => {
                    const customHandleBlur = (e) => {
                        if(!!values.email && !!values.description && !values.recaptcha) {
                            this._reCaptchaRef.current.execute()
                        }
                       handleBlur(e)
                    }
                    if (this.state.submitted && !this.state.submissionError.value) {
                        return (
                            <div className="d-flex justify-content-center mt-4">
                                <div className="text-center">
                                    <h3>Obrigado por contribuir com o site!</h3>
                                    <h5>Enviaremos detalhes do processo no seu e-mail.</h5>
                                    {!this.isChangeForm && (
                                        <Button variant={getVariant()} onClick={this.onClick}>
                                            Enviar nova sugestão
                                        </Button>
                                    )}
                                </div>
                            </div>
                        )
                    }
                    return (
                        <Form noValidate onSubmit={handleSubmit}>
                            <Form.Group controlId="action-email">
                                <Form.Label>E-mail*</Form.Label>
                                <Form.Control
                                    name="user_email"
                                    type="email"
                                    placeholder="email@exemplo.com"
                                    value={values.user_email}
                                    onChange={handleChange}
                                    onBlur={customHandleBlur}
                                    isValid={touched.user_email && !errors.user_email}
                                    isInvalid={touched.user_email && errors.user_email}
                                />
                                <Form.Text className={
                                    errors.user_email && touched.user_email ?
                                        "error__message" : "text-muted"
                                }>
                                    {errors.user_email && touched.user_email ?
                                        errors.user_email :
                                        "Você receberá atualizações sobre o andamento do processo de revisão e inclusão."
                                    }
                                </Form.Text>
                            </Form.Group>
                            <Form.Group controlId="action-description">
                                <Form.Label>Descrição*</Form.Label>
                                <Form.Control
                                    name="description"
                                    as="textarea"
                                    rows={3}
                                    placeholder="Sabia que não tinha encontrado todas..."
                                    value={values.description}
                                    onChange={handleChange}
                                    onBlur={customHandleBlur}
                                    isValid={touched.description && !errors.description}
                                    isInvalid={touched.description && errors.description}
                                />
                                <Form.Text className={
                                    errors.description && touched.description ?
                                        "error__message" : "text-muted"
                                }>
                                    {errors.description && touched.description ?
                                        errors.description :
                                        "Tente ser o mais breve possível :)"
                                    }
                                </Form.Text>
                            </Form.Group>
                            <Form.Group controlId="action-source">
                                <Form.Label>Fonte*</Form.Label>
                                <Form.Control
                                    name="source"
                                    type="input"
                                    placeholder="www.fonteconfiavel.com.br"
                                    value={values.source}
                                    onChange={handleChange}
                                    onBlur={customHandleBlur}
                                    isValid={touched.source && !errors.source}
                                    isInvalid={touched.source && errors.source}
                                />
                                <Form.Text className={
                                    errors.source && touched.source ?
                                        "error__message" : "text-muted"
                                }>
                                    {errors.source && touched.source ?
                                        errors.source :
                                        "Links de vídeos são preferidos."
                                    }
                                </Form.Text>
                            </Form.Group>
                            <Form.Group controlId="action-tags">
                                <Form.Label>Tags*</Form.Label>
                                <Field
                                    name="tags"
                                    component={TagsInput}
                                    whitelist={this.state.tags}
                                    initialValues={this._initialValues.tags}
                                    placeholder="Corrupção, Ministério da Cidadania..."
                                />
                                <Form.Text className={
                                    errors.tags && touched.tags ?
                                        "error__message" : "text-muted"
                                }>
                                    {errors.tags && touched.tags ?
                                        errors.tags :
                                        "Que tags representam esta ação?"}
                                </Form.Text>
                            </Form.Group>
                            <Form.Group as={Row} controlId="action-date">
                                <Col>
                                    <Form.Label>Data*</Form.Label>
                                    <Form.Control
                                        name="date"
                                        type="date"
                                        placeholder="dd/mm/aaaa"
                                        value={values.date}
                                        onChange={handleChange}
                                        onBlur={customHandleBlur}
                                        isValid={touched.date && !errors.date}
                                        isInvalid={touched.date && errors.date}
                                    />
                                    <Form.Text className={
                                        errors.date && touched.date ?
                                            "error__message" : "text-muted"
                                    }>
                                        {errors.date && touched.date ?
                                            errors.date :
                                            "Quando Bolsonaro fez isso?"
                                        }
                                    </Form.Text>
                                </Col>
                                <Col>
                                    <Form.Label>A data é estimada?</Form.Label>
                                    <CustomSwitch
                                        name="date_is_estimated"
                                        setFieldValue={setFieldValue}
                                        value={values.date_is_estimated}
                                    />
                                    <Form.Text className="text-muted">
                                        Se você não tem certeza da data, estime-a no campo ao lado e marque esta opção.
                                    </Form.Text>
                                </Col>
                            </Form.Group>
                            <Form.Group controlId="action-additional-infos">
                                <Form.Label>Informações adicionais</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    rows={3}
                                    name="additional_infos"
                                    value={values.additional_infos}
                                    onChange={handleChange}
                                />
                                <Form.Text className="text-muted">
                                    Alguma informação adicional que ajude a entender o contexto?
                                </Form.Text>
                            </Form.Group>
                            {this.isChangeForm && (
                                <Form.Group controlId="action-justification">
                                    <Form.Label>Por que você está sugerindo esta mudança?*</Form.Label>
                                    <Form.Control
                                        as="textarea"
                                        rows={3}
                                        name="justification"
                                        value={values.justification}
                                        onChange={handleChange}
                                        onBlur={customHandleBlur}
                                        isValid={touched.justification && !errors.justification}
                                        isInvalid={touched.justification && errors.justification}
                                    />
                                    <Form.Text className={
                                        errors.justification && touched.justification ?
                                            "error__message" : "text-muted"
                                    }>
                                        {errors.justification && touched.justification ?
                                            errors.justification :
                                            "Por favor, conte um pouco do motivo desta sugestão."
                                        }
                                    </Form.Text>
                                </Form.Group>
                            )}
                            <Form.Group as={Row} controlId="action-submit">
                                <Col md={this.isChangeForm ? 8 : 7}>
                                    <ReCAPTCHA
                                        ref={this._reCaptchaRef}
                                        sitekey={RECAPTCHA_SITE_KEY}
                                        onChange={(value) => setFieldValue("recaptcha", value)}
                                        size="invisible"
                                    />
                                </Col>
                                <Col md={this.isChangeForm ? 4 : 5} className="align-self-center">
                                    <div className="d-flex justify-content-end">
                                        {isSubmitting ? <Loader bootstrapClassName="mt-1" />  : (
                                            <Button
                                                variant={this.isChangeForm ? 'dark' : getVariant()}
                                                type="submit"
                                                size={this.isChangeForm ? "lg" : "md"}
                                                onClick={() => this._reCaptchaRef.current.execute()}
                                            >
                                                Enviar para revisão
                                            </Button>
                                        )}
                                    </div>
                                </Col>
                            </Form.Group>
                            {this.state.submissionError.value &&
                                (
                                    <Modal
                                        show={this.state.submissionError.value}
                                        onHide={this.onClick}
                                        className="submission-error"
                                        centered
                                    >
                                        <Modal.Header closeButton>
                                            <Modal.Title>
                                                Infelizmente, um erro aconteceu :(
                                </Modal.Title>
                                        </Modal.Header>
                                        <Modal.Body>
                                            {this.state.submissionError.text}
                                        </Modal.Body>
                                    </Modal>
                                )
                            }
                        </Form>
                    )
                }}
            </Formik>
        )
    }
}