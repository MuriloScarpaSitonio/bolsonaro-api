import os

import pytest


@pytest.fixture
def bolsonaro_api_url():
    return "http://www.test.com"


@pytest.fixture(scope="function", autouse=True)
def set_env_vars(request):
    if "noenvvars" in request.keywords:
        os.environ = {}
        return
    os.environ["BOLSONARO_API_BASE_URL"] = "http://www.test.com"


@pytest.fixture
def action_data():
    return {
        "id": 1000,
        "tags": ["Anticiência", "Coronavírus", "Ministério da Saúde"],
        "date": "03/07/2020",
        "description": (
            "Veto ao uso obrigatório de máscaras, em meio a pandemia de coronavírus."
        ),
        "source": (
            "https://g1.globo.com/politica/noticia/2020/07/03/bolsonaro-sanciona-com-vetos-lei-"
            "que-obriga-uso-de-mascaras-em-locais-publicos-pelo-pais.ghtml"
        ),
        "date_is_estimated": False,
        "additional_infos": (
            "O presidente vetou a obrigatoriedade de máscaras em órgãos e entidades públicas, "
            "estabelecimentos comerciais, industriais, templos religiosos e demais locais "
            "fechados em que haja reunião de pessoas."
        ),
    }


@pytest.fixture
def quote_data():
    return {
        "id": 1000,
        "tags": ["Coronavírus", "Fake news"],
        "date": "10/11/2020",
        "description": "Morte, invalidez, anomalia. Esta é a vacina que o Doria queria [...]",
        "source": (
            "https://g1.globo.com/politica/noticia/2020/11/10/mais-uma-que-jair-bolsonaro-"
            "ganha-diz-o-presidente-ao-comentar-suspensao-de-testes-da-vacina-coronavac.ghtml"
        ),
        "is_fake_news": True,
        "fake_news_source": (
            "https://politica.estadao.com.br/blogs/estadao-verifica/coronavac-teve-apenas"
            "-efeitos-colaterais-leves-e-falso-que-voluntarios-tenham-morrido/"
        ),
        "date_is_estimated": False,
        "additional_infos": (
            "Sem apresentar provas, Bolsonaro conclui efeitos "
            "adversos da vacina coronaVac."
        ),
    }
