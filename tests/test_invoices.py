from http import HTTPStatus

INVOICES_PATH = "/api/invoices"

def test_get_invoices_success(client, sample_invoices, auth_headers):
    """
    Escenario:
        Existen facturas registradas dentro del rango de fechas solicitado.

    Acción:
        Se consulta el endpoint con todos los parámetros válidos.

    Resultado esperado:
        Se obtiene una respuesta HTTP 200 con la lista paginada de facturas.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "page": 1,
            "page_size": 3,
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 3
    assert data["total_pages"] == 1
    assert len(data["items"]) == 3


def test_get_invoices_without_start_date(client, auth_headers):
    """
    Escenario:
        El cliente no envía el parámetro obligatorio 'start_date'.

    Acción:
        Se consulta el endpoint únicamente con la fecha de fin.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que el parámetro
        'start_date' es obligatorio.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "end_date": "2022-01-31",
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["start_date"] == [
        "The start_date parameter is required."
    ]


def test_get_invoices_without_end_date(client, auth_headers):
    """
    Escenario:
        El cliente no envía el parámetro obligatorio 'end_date'.

    Acción:
        Se consulta el endpoint únicamente con la fecha de inicio.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que el parámetro
        'end_date' es obligatorio.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["end_date"] == [
        "The end_date parameter is required."
    ]


def test_get_invoices_with_default_page(client, sample_invoices, auth_headers):
    """
    Escenario:
        El cliente no envía el parámetro 'page'.

    Acción:
        Se consulta el endpoint únicamente indicando el rango de fechas
        y el tamaño de página.

    Resultado esperado:
        Se utiliza la página 1 por defecto.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "page_size": 3,
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert data["page"] == 1
    assert data["page_size"] == 3


def test_get_invoices_with_default_page_size(client, sample_invoices, auth_headers):
    """
    Escenario:
        El cliente no envía el parámetro 'page_size'.

    Acción:
        Se consulta el endpoint indicando únicamente el rango de fechas
        y el número de página.

    Resultado esperado:
        Se utiliza el tamaño de página por defecto de 20 registros.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "page": 1,
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert data["page"] == 1
    assert data["page_size"] == 20


def test_get_invoices_with_maximum_page_size(client, sample_invoices, auth_headers):
    """
    Escenario:
        El cliente solicita el número máximo permitido de registros
        por página.

    Acción:
        Se consulta el endpoint con page_size=100.

    Resultado esperado:
        La solicitud es procesada correctamente.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "page": 1,
            "page_size": 100,
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert data["page_size"] == 100


def test_get_invoices_with_page_size_greater_than_maximum(client, auth_headers):
    """
    Escenario:
        El cliente envía un valor de 'page_size' mayor al permitido.

    Acción:
        Se consulta el endpoint con page_size=101.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que el valor no
        cumple con las restricciones establecidas.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "page_size": 101,
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "page_size" in data


def test_get_invoices_with_page_less_than_one(client, auth_headers):
    """
    Escenario:
        El cliente envía un número de página menor que uno.

    Acción:
        Se consulta el endpoint con page=0.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que el valor
        proporcionado es inválido.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "page": 0,
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "page" in data


def test_get_invoices_with_invalid_date_range(client, auth_headers):
    """
    Escenario:
        La fecha de inicio es posterior a la fecha de fin.

    Acción:
        Se consulta el endpoint con un rango de fechas inválido.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que la fecha
        inicial no puede ser mayor que la fecha final.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-02-01",
            "end_date": "2022-01-01",
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["start_date"] == [
        "The start_date cannot be later than end_date."
    ]


def test_get_invoices_with_invalid_start_date_format(client, auth_headers):
    """
    Escenario:
        El cliente envía una fecha de inicio con un formato inválido.

    Acción:
        Se consulta el endpoint utilizando un formato diferente a
        YYYY-MM-DD.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que el formato
        de la fecha es incorrecto.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "01/01/2022",
            "end_date": "2022-01-31",
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["start_date"] == [
        "The start_date must have the format YYYY-MM-DD."
    ]


def test_get_invoices_with_invalid_end_date_format(client, auth_headers):
    """
    Escenario:
        El cliente envía una fecha de fin con un formato inválido.

    Acción:
        Se consulta el endpoint utilizando un formato diferente a
        YYYY-MM-DD.

    Resultado esperado:
        Se obtiene una respuesta HTTP 400 indicando que el formato
        de la fecha es incorrecto.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2022-01-01",
            "end_date": "31/01/2022",
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data["end_date"] == [
        "The end_date must have the format YYYY-MM-DD."
    ]


def test_get_invoices_without_results(client, auth_headers):
    """
    Escenario:
        No existen facturas dentro del rango de fechas solicitado.

    Acción:
        Se consulta el endpoint con un rango de fechas sin registros.

    Resultado esperado:
        Se obtiene una respuesta HTTP 200 con una lista vacía y un
        total de cero registros.
    """
    response = client.get(
        INVOICES_PATH,
        query_string={
            "start_date": "2030-01-01",
            "end_date": "2030-01-31",
        },
        headers=auth_headers,
    )

    data = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert data["total"] == 0
    assert data["items"] == []
    assert data["total_pages"] == 0