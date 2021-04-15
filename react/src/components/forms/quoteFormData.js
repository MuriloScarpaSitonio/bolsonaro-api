import * as yup from "yup"


const quoteFormData = [
    {
        id: "user_email",
        type: "text",
        validationType: "string",
        validations: [
            {
                type: "required",
                params: ["*O e-mail é obrigatório."]
            },
            {
                type: "email",
                params: ["*E-mail inválido."]
            }
        ]
    },
    {
        id: "description",
        type: "text",
        validationType: "string",
        validations: [
            {
                type: "required",
                params: ["*A declaração é obrigatória."]
            },
        ]
    },
    {
        id: "source",
        type: "text",
        validationType: "string",
        validations: [
            {
                type: "required",
                params: ["*Informe um link que comprove a declaração."]
            },
            {
                type: "url",
                params: ["*Informe uma URL válida. (tente copiar e colar um link do navegador)"]
            }
        ]
    },
    {
        id: "tags",
        type: "text",
        validationType: "string",
        validations: [
            {
                type: "required",
                params: ["*Informe pelo menos uma tag."]
            },
        ]
    },
    {
        id: "date",
        type: "text",
        validationType: "date",
        validations: [
            {
                type: "min",
                params: [new Date("1955-03-21"), "*A data precisa ser superior à 21/03/1955"]
            },
            {
                type: "max",
                params: [new Date(), "*A data precisa ser anterior ou igual ao dia de hoje"]
            },
            {
                type: "required",
                params: ["*Informe a data da declaração."]
            },
            {
                type: "typeError",
                params: ["*Informe uma data válida."]
            }
        ]
    },
    {
        id: "date_is_estimated",
        type: "boolean",
        validationType: "boolean",
        required: false,
    },
    {
        id: "additional_infos",
        type: "text",
        validationType: "string",
        required: false,
    },
    {
        id: "is_fake_news",
        type: "boolean",
        validationType: "boolean",
        required: false,
    },
    {
        id: "fake_news_source",
        type: "text",
        validationType: "string",
        validations: [
            {
                type: "url",
                params: ["*Informe uma URL válida (tente copiar e colar um link do navegador)."]
            },
            {
                type: "when",
                params: ["is_fake_news", {
                    is: true,
                    then: yup.string()
                        .url()
                        .required("*Informe uma fonte que comprove que a declaração é falsa.")
                }]
            }
        ]
    },
    {
        id: "recaptcha",
        type: "text",
        validationType: "string",
        validations: [
            {
                type: "required",
                params: ["*Marque a caixa para provar que você não é um robô."]
            },
        ]
    }
];


export default quoteFormData