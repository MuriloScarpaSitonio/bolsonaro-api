import { Component } from 'react'

import {Field,Formik} from 'formik'
import { Button, Col, Form } from 'react-bootstrap'
import Cookies from 'universal-cookie'

import TagsInput from './TagsInput'
import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { BASE_API_URL } from "../consts"
import { convertDateStringToLocaleFormat, getVariant, toSlug } from "../helpers"


export default class QueryForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false,
            submissionError: {value: false, text: ""},
            tagsWhitelist: []
        }
        this._fetchTagsWhitelist()
    }
    
    _fetchTagsWhitelist = () => {
        fetch(`${BASE_API_URL}/${this.props.baseEndpoint}/tags`)
            .then(response => {
                if(!response.ok) {
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
                        data => this.setState({ isLoaded: true, tagsWhitelist: data.map(tag => tag.name) }),
                        error => this.setState({ isLoaded: true, error })

                    )
                }
            })
            .catch(error => {
                this.setState({ isLoaded: true, error })
            })
    }

    _getTagsInitialValues = () => {
        const cookies = new Cookies()
        let tags = cookies.get('tags') || []
        for (var i = 0; i < tags.length; i++) {
            if(tags[i].slug === this.props.tagsInitialValues) {
                return [tags[i].name]
            }
        }

        return []
    }

    render() {
        if(this.state.error) return <Error message={this.state.error.message} />
        if(!this.state.isLoaded) return <Loader />
        let tagsInitialValues = this._getTagsInitialValues()
        return (
            <Formik
                key={this.props.textInitialValue}
                initialValues={{
                    start_date: '',
                    end_date: '',
                    description: this.props.textInitialValue,
                    tags: tagsInitialValues
                }}
                onSubmit={(values,{setSubmitting}) => {
                    setSubmitting(true)
                    this.props.setSearchParams({
                        ...values,
                        tags: values.tags.map(tag => toSlug(tag)).toString(),
                        start_date: convertDateStringToLocaleFormat(values.start_date),
                        end_date: convertDateStringToLocaleFormat(values.end_date),
                        page: 1
                    })
                    setSubmitting(false)
                }
            }
            >
            {({ handleChange, handleSubmit }) => (
                <Form noValidate onSubmit={handleSubmit}>
                    <Form.Row className='mt-4'>
                        <Col xs={12} sm={12} md={6} lg={6} xl={6} className='mt-3'>
                            <Form.Label>Data inicial</Form.Label>
                            <Form.Control
                                name='start_date'
                                type='date'
                                onChange={handleChange}
                            />
                        </Col>
                        <Col xs={12} sm={12} md={6} lg={6} xl={6} className='mt-3'>
                            <Form.Label>Data final</Form.Label>
                            <Form.Control
                                name='end_date'
                                type='date'
                                onChange={handleChange}
                            />
                        </Col>
                    </Form.Row>
                    <Form.Row>
                        <Col className='mt-3'>
                            <Form.Label>Texto</Form.Label>
                            <Form.Control
                                name='description'
                                defaultValue={this.props.textInitialValue}
                                type='text'
                                placeholder='Filtre por texto'
                                onChange={handleChange}
                            />
                        </Col>
                    </Form.Row>
                    <Form.Row>
                        <Col className='mt-3'>
                            <Form.Label>Tags</Form.Label>
                            <Field
                                name='tags'
                                component={TagsInput}
                                noValidate
                                whitelist={this.state.tagsWhitelist}
                                initialValues={tagsInitialValues}
                                placeholder='Filtre por tags'
                            />
                        </Col>
                    </Form.Row>
                    <div className='d-flex justify-content-end'>
                        <Button variant={getVariant()} type='submit' className='mt-4'>
                            Pesquisar
                        </Button>
                    </div>
                </Form>
            )}
            </Formik>
        )
    }
}
