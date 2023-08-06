

import pkg_resources

from unidecode import unidecode

import json
import pandas as pd

from ..utils import constant as cst


def bonds_as_df(country=None):
    """
    Esta função recupera todos os dados de títulos armazenados no arquivo `bonds.csv`, que anteriormente era
    recuperado de Investing.com. Uma vez que o objeto resultante é uma matriz de dados, os dados dos títulos são devidamente
    estruturado em linhas e colunas, em que colunas são os nomes dos atributos dos dados de títulos. Além disso, país
    a filtragem pode ser especificada, o que fará com que esta função não retorne todos os dados de títulos armazenados, mas apenas
    os dados dos títulos do país introduzido.
    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.

    Returns:
        :obj:`pandas.DataFrame` - bonds_df:
        O: obj: `pandas.DataFrame` resultante contém todos os dados de títulos do país introduzido, se especificado,
            ou de todos os países se Nenhum foi especificado, conforme indexado em Investing.com a partir das informações anteriores
            recuperado pelo ejtrader e armazenado em um arquivo csv.

            Então, o: obj: `pandas.DataFrame` resultante será semelhante a ::

               país | nome | nome completo
                --------|------|-----------
                xxxxxxx | xxxx | xxxxxxxxx

    Raises:
        ValueError: gerado sempre que algum dos argumentos introduzidos não é válido.
        FileNotFoundError: gerado quando o arquivo `bonds.csv` não foi encontrado.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'ejtrader'
    resource_path = '/'.join(('resources', 'bonds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    bonds.drop(columns=['tag', 'id'], inplace=True)
    bonds = bonds.where(pd.notnull(bonds), None)

    if country is None:
        bonds.reset_index(drop=True, inplace=True)
        return bonds
    else:
        country = unidecode(country.strip().lower())

        if country not in bond_countries_as_list():
            raise ValueError("ERR#0034: country " + country + " not found, check if it is correct.")

        bonds = bonds[bonds['country'] == country]
        bonds.reset_index(drop=True, inplace=True)
        
        return bonds


def bonds_as_list(country=None):
    """
    Esta função recupera todos os nomes de títulos armazenados no arquivo `bonds.csv`, que contém todos os
    dados dos títulos, obtidos anteriormente de Investing.com. Então, esta função irá apenas retornar
    os nomes dos títulos do governo, que serão um dos parâmetros de entrada quando se trata de funções de recuperação de dados de títulos
    do ejtrader. Além disso, observe que a filtragem de país pode ser aplicada, o que é muito útil, pois
    esta função apenas retorna os nomes e nas funções de recuperação de dados de títulos tanto o nome quanto o país
    devem ser especificados e devem corresponder.
    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.

    Returns:
        :obj:`list` - bonds_list:
            The resulting :obj:`list` contains the all the bond names from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by ejtrader and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of bond names will look like::

                bonds_list = ['Argentina 1Y', 'Argentina 3Y', 'Argentina 5Y', 'Argentina 9Y', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `bonds.csv` file was not found.
        IOError: raised when `bonds.csv` file is missing or empty.
    
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'ejtrader'
    resource_path = '/'.join(('resources', 'bonds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    bonds.drop(columns=['tag', 'id'], inplace=True)
    bonds = bonds.where(pd.notnull(bonds), None)

    if country is None:
        return bonds['name'].tolist()
    else:
        country = unidecode(country.strip().lower())

        if country not in bond_countries_as_list():
            raise ValueError("ERR#0034: country " + country + " not found, check if it is correct.")

        return bonds[bonds['country'] == country]['name'].tolist()


def bonds_as_dict(country=None, columns=None, as_json=False):
    """
    Esta função recupera todas as informações de títulos armazenadas no arquivo `bonds.csv` e o formata como um
    Dicionário Python que contém as mesmas informações do arquivo, mas cada linha é um: obj: `dict` e
    todos eles estão contidos em uma: obj: `list`. Observe que a estrutura do dicionário é a mesma que a
    Estrutura JSON. Alguns parâmetros opcionais podem ser especificados como o país, colunas ou as_json, que
    são uma filtragem por país para não retornar todos os títulos, mas apenas os do país introduzido,
    os nomes das colunas que deseja recuperar no caso de precisar de apenas algumas colunas para evitar informações desnecessárias
    carregar e se as informações devem ser retornadas como um objeto JSON ou como um dicionário; respectivamente.
    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.
        columns (:obj:`list`, optional): column names of the bonds data to retrieve, can be: <country, name, full_name>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - bonds_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every bond as indexed in Investing.com from
            the information previously retrieved by ejtrader and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                bonds_dict = {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `bonds.csv` file was not found.
        IOError: raised when `bonds.csv` file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = 'ejtrader'
    resource_path = '/'.join(('resources', 'bonds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    bonds.drop(columns=['tag', 'id'], inplace=True)
    bonds = bonds.where(pd.notnull(bonds), None)

    if columns is None:
        columns = bonds.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in bonds.columns.tolist() for column in columns):
        raise ValueError("ERR#0063: specified columns does not exist, available columns are "
                         "<country, name, full_name>")

    if country is None:
        if as_json:
            return json.dumps(bonds[columns].to_dict(orient='records'))
        else:
            return bonds[columns].to_dict(orient='records')
    else:
        country = unidecode(country.strip().lower())

        if country not in bond_countries_as_list():
            raise ValueError("ERR#0034: country " + country + " not found, check if it is correct.")

        if as_json:
            return json.dumps(bonds[bonds['country'] == country][columns].to_dict(orient='records'))
        else:
            return bonds[bonds['country'] == country][columns].to_dict(orient='records')


def bond_countries_as_list():
    """
   Esta função retorna uma lista com todos os países disponíveis de onde os títulos podem ser recuperados, para
    informe ao usuário quais deles estão disponíveis, já que o parâmetro país é obrigatório em toda recuperação de títulos
    função.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with government bonds as indexed in Investing.com

    """

    return [value['country'] for value in cst.BOND_COUNTRIES]
