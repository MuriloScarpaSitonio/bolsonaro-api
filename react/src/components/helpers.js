import * as yup from 'yup'

function getDateString(date) {
    let dateParts = date.split("/");
    let quote_date = new Date(+dateParts[2], dateParts[1] - 1, +dateParts[0])
    //setando a data para o GMT
    quote_date = new Date(quote_date.valueOf() + quote_date.getTimezoneOffset() * 60000)
        //setando a data para o GMT
        .toLocaleDateString('pt-br', { year: 'numeric', month: 'long', day: 'numeric' })

    return quote_date
}

function toSlug(tag) {
    return tag
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')   // retira os acentos
        .toLowerCase()
        .replace(/ /g, '-')
        .replace(',', '')
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createYupSchema(schema, config) {
    const { id, validationType, validations = [] } = config;
    if (!yup[validationType]) {
        return schema;
    }
    let validator = yup[validationType]();
    validations.forEach(validation => {
        const { params, type } = validation;
        if (!validator[type]) {
            return;
        }
        validator = validator[type](...params);
    });
    schema[id] = validator;
    return schema;
}


function formHasChanges(values, initialValues) {
    let changes = []
    let changeableValues = ["user_email", "justification"]
    for (const prop in values) {
        if (!changeableValues.includes(prop)) {
            if (values[prop] !== initialValues[prop]) {
                changes.push(prop)
            }
        }
    }
    return changes.length > 0
}


function convertDateStringToLocaleFormat(dateStr) {
    return dateStr.split('-').reverse().join('/')
}


function convertDateStringLocaleToRegularFormat(dateStr) {
    return dateStr.split('/').reverse().join('-')
}

function getVariant() {
    return window.localStorage.getItem('theme') === 'theme--dark' ? 'light' : 'dark'
}

export {
    convertDateStringToLocaleFormat,
    convertDateStringLocaleToRegularFormat,
    createYupSchema,
    formHasChanges,
    getVariant,
    getCookie,
    getDateString,
    toSlug
}


/*
TODO: implement django URLValidation in the frontend

function URLValidator() {
    const ul = '\u00a1-\uffff'
    const ipv4_re = '(?:25[0-5]|2[0-4]d|[0-1]?d?d)(?:.(?:25[0-5]|2[0-4]d|[0-1]?d?d)){3}'
    const ipv6_re = '[[0-9a-f:.]+]'
    const hostname_re = '[a-z' + ul + '0-9](?:[a-z' + ul + '0-9-]{0,61}[a-z' + ul + '0-9])?'
    const domain_re = '(?:.(?!-)[a-z' + ul + '0-9-]{1,63}(?<!-))*'
    const tld_re = (
        '.' +                                                   //dot
        '(?!-)' +                                               //can't start with a dash
        '(?:[a-z' + ul + '-]{2,63}' +                           //domain label
        '|xn--[a-z0-9]{1,59})' +                                //or punycode label
        '(?<!-)' +                                              //can't end with a dash
        '.?'                                                    //may have a trailing dot
    )
    const host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

    const re = (
        '^(?:[a-z0-9.+-]*):\/\/' +                                  //scheme is validated separately
        '(?:[^s:@/]+(?::[^s:@\/]*)?@)?' +                           //user:pass authentication
        '(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')' +
        '(?::d{2,5})?' +                                            //port
        '(?:[\/?#][^s]*)?' +                                        //resource path
        'Z'
    )
    const regex = new RegExp(re, 'i') //igonare case
}*/



/*
TODO: Focus first error field on formik error;
A funcao abaixo nao funciona com multiplos erros. Imagine que voce tenha dois erros
no form. Essa funcao focará na primeiro erro, como deveria. No entanto, após a
validação do campo com erro (enquanto o usuario digita), a funcao focará no próximo erro
(repito: enquanto o usuário digita!). Em resumo: se a form ja tiver os erros mapeados,
essa funcao focará neles após a validação dos erros anteriores

const FormikOnError = ({ children, isChangeForm }) => {
    const formik = useFormikContext()
    useEffect(() => {
        //let index = isChangeForm ? 0 : 1 -> only for ActionForm
        if (!formik.isValid && formik.submitCount > 0) {
            const firstErrorKey = Object.keys(formik.errors)[0]
            if (global.window.document.getElementsByName(firstErrorKey).length) {
                //global.window.document.getElementsByName(firstErrorKey)[index].focus()
                global.window.document.getElementsByName(firstErrorKey)[0].focus()
            }
        }
    }, [formik.submitCount, formik.isValid, formik.errors, isChangeForm])
    return children
}
*/