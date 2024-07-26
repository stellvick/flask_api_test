
def normalize_hotel_path_params(
    cidade: str = None,
    estrelas_min: float = 0,
    estrelas_max: float = 5,
    diaria_min: float = 0,
    diaria_max: float = 10000,
    limit: int = 50,
    offset: int = 0,
    **kwargs
) -> dict:
    if cidade:
        return {
            'cidade': cidade,
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset,
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset,
    }


def search_hotel_query(params: dict) -> str:
    if not params.get('cidade'):
        consulta = ("SELECT * FROM hoteis "
                    "WHERE (estrelas >= ? and estrelas <= ?) and "
                    "(diaria >= ? and diaria <= ?) "
                    "LIMIT ? "
                    "OFFSET ?")
    else:
        consulta = ("SELECT * FROM hoteis "
                    "WHERE cidade = ? and "
                    "(estrelas >= ? and estrelas <= ?) and "
                    "(diaria >= ? and diaria <= ?) "
                    "LIMIT ? "
                    "OFFSET ?")
    return consulta
