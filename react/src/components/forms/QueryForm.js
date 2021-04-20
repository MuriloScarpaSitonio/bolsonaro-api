import { Field, Formik } from 'formik'
import { Button, Col, Form } from 'react-bootstrap'
import Cookies from 'universal-cookie'

import TagsInput from './TagsInput'
import Error from "../static/Error"
import { Loader } from "../static/Loader"
import { useQuery } from "../hooks/useQuery"
import { convertDateStringToLocaleFormat, getVariant, toSlug } from "../helpers"

function _getTagsInitialNames(tagsInitialValues) {
    const cookies = new Cookies()
    let tags = cookies.get('tags') || []
    for (var i = 0; i < tags.length; i++) {
        if(tags[i].slug === tagsInitialValues) {
            return [tags[i].name]
        }
    }
    return []
}


export const QueryForm = (props) => {
    const [data, isLoaded, error] = useQuery(`${props.baseEndpoint}/tags`)
    let tagsInitialNames = _getTagsInitialNames(props.tagsInitialValues)

    if(error) return <Error message={error.message} />
    if(!isLoaded) return <Loader />
    return (
        <Formik
            key={props.textInitialValue}
            initialValues={{
                start_date: '',
                end_date: '',
                description: props.textInitialValue,
                tags: tagsInitialNames
            }}
            onSubmit={(values,{setSubmitting}) => {
                setSubmitting(true)
                props.setSearchParams({
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
                            defaultValue={props.textInitialValue}
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
                            whitelist={data.map(tag => tag.name)}
                            initialValues={tagsInitialNames}
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

