const actionFormData = [
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
                params: ["*A descrição é obrigatória."]
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
                params: ["*Informe um link que comprove a descrição."]
            },
            {
                type: "url",
                params: ["*Informe uma URL válida (tente copiar e colar um link do navegador)."]
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
                params: ["*Informe a data da descrição."]
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


export default actionFormData