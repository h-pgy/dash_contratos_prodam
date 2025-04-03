# config.py
import os
from dotenv import load_dotenv
import copy


def get_env_var(varname:str)->str:

    load_dotenv()
    try:
        return os.environ[varname]
    except KeyError:
        raise RuntimeError(f'Variavel de ambiente {varname} não definida')
    

# Acesso às variáveis
DATA_PATH: str = get_env_var('DATA_PATH')
SOF_TOKEN: str = get_env_var('SOF_TOKEN')

if __name__ == '__main__':

    namespace_copy = {k: v for k, v in globals().items() if not k.startswith("__") and k[0].isupper()}

    print(namespace_copy)