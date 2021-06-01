FROM python:3.8-alpine

RUN apk add --update git bash curl unzip zip openssl make

ENV TERRAFORM_VERSION="0.13.7"

RUN curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > terraform.zip && \
    unzip terraform -d /bin && \
    rm -f terraform_${TERRAFORM_VERSION}_linux_amd64.zip

ENTRYPOINT ["terraform"]