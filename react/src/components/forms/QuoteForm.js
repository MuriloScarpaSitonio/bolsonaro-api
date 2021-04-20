import { useRef, useState } from "react"

import ReCAPTCHA from "react-google-recaptcha"
import { Field, Formik } from "formik"
import * as yup from "yup"
import { Button, Col, Form, Modal, Row } from "react-bootstrap"

import Error from "../static/Error"
import { Loader } from "../static/Loader"
import quoteFormData from "./quoteFormData"
import TagsInput from "./TagsInput"
import { useQuery } from "../hooks/useQuery"
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
            id={"custom-switch" + name}
            checked={value}
            value={value}
            onChange={() => label === "Não" ? setLabel("Sim") : setLabel("Não")}
            onClick={(e) => setFieldValue(name, e.target.checked)}
        />
    )
}

const MyFormikForm = (props) => {
    const [submissionError, setSubmissionError] = useState({value: false,text: ""})
    const [submitted, setSubmitted] = useState(false)
    let reCaptchaRef = useRef()
    
    const onClick = () => {
        setSubmissionError({value: false,text: ""})
        setSubmitted(false)
    }

    return (
        <Formik
                validationSchema={props.validationSchema}
                initialValues={props.initialValues}
                onSubmit={(values, { setSubmitting, resetForm }) => {
                    setSubmitting(true)
                    if (formHasChanges(values, props.initialValues)) {
                        fetch(props.isChangeForm ?
                            `${BASE_API_URL}/quotes/${values.id}/change` :
                            `${BASE_API_URL}/quotes/suggest`,
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
                                            setSubmissionError({
                                                value: true,
                                                text: "Requisição inválida!\n" + JSON.stringify(response)
                                            })
                                            setSubmitted(true)
                                        }
                                    )
                                }
                                else {
                                    response.json().then(_ => {
                                        setSubmitting(false)
                                        setSubmitted(true)
                                        resetForm()
                                    })
                                        .catch(_ => {
                                            setSubmitting(false)
                                            setSubmissionError({
                                                value: true,
                                                text: (
                                                    `Tivemos um erro na hora de processar sua solicitação! 
                                                Por favor, feche esta caixa e tente enviar a sugestão novamente.`
                                                )
                                            })
                                            setSubmitted(true)
                                        })
                                }
                            })
                    }
                    else {
                        setSubmitting(false)
                        setSubmissionError({value: true, text: "Sua sugestão precisa alterar pelo menos um campo!"})
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
                            reCaptchaRef.current.execute()
                        }
                       handleBlur(e)
                    }
                    if (submitted && !submissionError.value) {
                        return (
                            <div className="d-flex justify-content-center mt-4">
                                <div className="text-center">
                                    <h3>Obrigado por contribuir com o site!</h3>
                                    <h5>Enviaremos detalhes do processo no seu e-mail.</h5>
                                    {!props.isChangeForm && (
                                        <Button variant={getVariant()} onClick={onClick}>
                                            Enviar nova sugestão
                                        </Button>
                                    )}
                                </div>
                            </div>
                        )
                    }
                    return (
                        <Form noValidate onSubmit={handleSubmit}>
                            <Form.Group controlId="quote-email">
                                <Form.Label>E-mail*</Form.Label>
                                <Form.Control
                                    name="user_email"
                                    type="email"
                                    placeholder="email@exemplo.com"
                                    value={values.user_email}
                                    onBlur={customHandleBlur}
                                    onChange={handleChange}
                                    isValid={touched.user_email && !errors.user_email}
                                    isInvalid={touched.user_email && errors.user_email}
                                />
                                <Form.Text className={
                                    touched.user_email && errors.user_email ?
                                        "error__message" : "text-muted"
                                }>
                                    {touched.user_email && errors.user_email ?
                                        errors.user_email :
                                        "Você receberá atualizações sobre o andamento do processo de revisão e inclusão."
                                    }
                                </Form.Text>
                            </Form.Group>
                            <Form.Group controlId="quote-description">
                                <Form.Label>Declaração*</Form.Label>
                                <Form.Control
                                    name="description"
                                    as="textarea"
                                    rows={3}
                                    placeholder="Blablabla muuuuu..."
                                    value={values.description}
                                    onBlur={customHandleBlur}
                                    onChange={handleChange}
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
                            <Form.Group controlId="quote-source">
                                <Form.Label>Fonte*</Form.Label>
                                <Form.Control
                                    name="source"
                                    type="input"
                                    placeholder="www.fonteconfiavel.com.br"
                                    value={values.source}
                                    onBlur={customHandleBlur}
                                    onChange={handleChange}
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
                            <Form.Group>
                                <Form.Label>Tags*</Form.Label>
                                <Field
                                    name="tags"
                                    component={TagsInput}
                                    whitelist={props.tagsWhitelist}
                                    initialValues={props.initialValues.tags}
                                    placeholder="Esquerda, Ditadura..."
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
                            <Form.Group as={Row} controlId="quote-date">
                                <Col>
                                    <Form.Label>Data*</Form.Label>
                                    <Form.Control
                                        name="date"
                                        type="date"
                                        placeholder="dd/mm/aaaa"
                                        value={values.date}
                                        onBlur={customHandleBlur}
                                        onChange={handleChange}
                                        isValid={touched.date && !errors.date}
                                        isInvalid={touched.date && errors.date}
                                    />
                                    <Form.Text className={
                                        errors.date && touched.date ?
                                            "error__message" : "text-muted"
                                    }>
                                        {errors.date && touched.date ?
                                            errors.date :
                                            "Quando Bolsonaro falou isso?"
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
                            <Form.Group controlId="quote-addition-infos">
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
                            <Form.Group as={Row} controlId="quote-fake-news">
                                <Col xs={3}>
                                    <Form.Label>Fake news?</Form.Label>
                                    <CustomSwitch
                                        name="is_fake_news"
                                        setFieldValue={setFieldValue}
                                        value={values.is_fake_news}
                                    />
                                </Col>
                                <Col xs={9}>
                                    {values.is_fake_news && (
                                        <Form.Group>
                                            <Form.Label>Fonte da fake news*</Form.Label>
                                            <Form.Control
                                                type="input"
                                                name="fake_news_source"
                                                placeholder="www.fakenews.com.br"
                                                value={values.fake_news_source}
                                                onBlur={customHandleBlur}
                                                onChange={handleChange}
                                                isValid={touched.fake_news_source && !errors.fake_news_source}
                                                isInvalid={touched.fake_news_source && errors.fake_news_source}
                                            />
                                            <Form.Text className={
                                                errors.fake_news_source && touched.fake_news_source ?
                                                    "error__message" : "text-muted"
                                            }>
                                                {errors.fake_news_source && touched.fake_news_source ?
                                                    errors.fake_news_source :
                                                    "Algum link que mostre que a declaração é uma fake news."
                                                }
                                            </Form.Text>
                                        </Form.Group>
                                    )}
                                </Col>
                            </Form.Group>
                            {props.isChangeForm && (
                                <Form.Group controlId="quote-justification">
                                    <Form.Label>Por que você está sugerindo esta mudança?*</Form.Label>
                                    <Form.Control
                                        as="textarea"
                                        rows={3}
                                        name="justification"
                                        value={values.justification}
                                        onBlur={customHandleBlur}
                                        onChange={handleChange}
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
                            <Form.Group as={Row} controlId="quote-submit">
                                <Col md={props.isChangeForm ? 8 : 7}>
                                    <ReCAPTCHA
                                        ref={reCaptchaRef}
                                        sitekey={RECAPTCHA_SITE_KEY}
                                        onChange={(value) => setFieldValue("recaptcha", value)}
                                        size="invisible"
                                    />
                                </Col>
                                <Col md={props.isChangeForm ? 4 : 5} className="align-self-center">
                                    <div className="d-flex justify-content-end">
                                        {isSubmitting ? <Loader bootstrapClassName="mt-1" /> : (
                                            <Button
                                                variant={props.isChangeForm ? 'dark' : getVariant()}
                                                type="submit"
                                                size={props.isChangeForm ? "lg" : "md"}
                                                onClick={(e) => {
                                                    reCaptchaRef.current.execute()
                                                    handleSubmit(e)
                                                }}
                                            >
                                                Enviar para revisão
                                            </Button>
                                        )}
                                    </div>
                                </Col>
                            </Form.Group>
                            {submissionError.value &&
                                (
                                    <Modal
                                        show={submissionError.value}
                                        onHide={onClick}
                                        className="submission-error"
                                        centered
                                    >
                                        <Modal.Header closeButton>
                                            <Modal.Title>
                                                Infelizmente, um erro aconteceu :(
                                            </Modal.Title>
                                        </Modal.Header>
                                        <Modal.Body>
                                            {submissionError.text}
                                        </Modal.Body>
                                    </Modal>
                                )
                            }
                        </Form>
                    )
                }}
            </Formik>)
}

export const QuoteForm = (props) => {
    const [data, isLoaded,error] = useQuery('quotes/tags')
    
    let isChangeForm = props.initialValues ? true : false
    if(isChangeForm) { //if the form has initialValues, it means a suggestion to change an Action
        quoteFormData.push({
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

    let initialValues = isChangeForm ?
        {...props.initialValues,user_email: "",recaptcha: "",justification: ""}
        : {
            user_email: "",
            description: "",
            source: "",
            tags: "",
            date: "",
            date_is_estimated: false,
            additional_infos: "",
            is_fake_news: false,
            fake_news_source: "",
            recaptcha: ""
        }

    if (error) return <Error message={error.message} />
    if (!isLoaded) return <Loader />
    return <MyFormikForm
        validationSchema={yup.object().shape(quoteFormData.reduce(createYupSchema,{}))}
        initialValues={initialValues}
        isChangeForm={isChangeForm}
        tagsWhitelist={data.map(tag => tag.name)}
    />
}
