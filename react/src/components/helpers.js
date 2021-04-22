import * as yup from 'yup'

function getDateString(date) {
    let dateParts = date.split("/");
    let quote_date = new Date(+dateParts[2], dateParts[1] - 1, +dateParts[0])
    //setando a data para o GMT
    quote_date = new Date(quote_date.valueOf() + quote_date.getTimezoneOffset() * 60000)
        //setando a data para o GMT
        .toLocaleDateString('pt-br', {year: 'numeric', month: 'long', day: 'numeric'})

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
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createYupSchema(schema, config) {
    const {id, validationType, validations = []} = config
    if (!yup[validationType]) return schema
    let validator = yup[validationType]()
    validations.forEach(validation => {
        const {params, type} = validation
        if(!validator[type]) return
        validator = validator[type](...params)
    })
    schema[id] = validator
    return schema
}


function _arraysAreEqual(arrayA, arrayB) {
    if (arrayA === arrayB) return true
    if (arrayA.length !== arrayB.length) return false

    for(var i = 0; i < arrayA.length; ++i) {
        if (!arrayB.includes(arrayA[i])) return false
    }
    return true
}


function formHasChanges(values, initialValues) {
    let changes = []
    let changeableValues = ["user_email", "justification", "recaptcha"]
    for(const prop in values) {
        if(prop === 'tags') {
            if (!_arraysAreEqual(values[prop], initialValues[prop])) {
                changes.push(prop)
            }
            continue
        }
        if(!changeableValues.includes(prop)) {
            if(values[prop] !== initialValues[prop]) {
                changes.push(prop)
            }
        }
    }
    return changes.length > 0
}


function convertDateStringToLocaleFormat(dateStr) { return dateStr.split('-').reverse().join('/') }

function convertDateStringLocaleToRegularFormat(dateStr) { return dateStr.split('/').reverse().join('-') }

function getVariant() { return window.localStorage.getItem('theme') === 'theme--dark' ? 'light' : 'dark' }

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
