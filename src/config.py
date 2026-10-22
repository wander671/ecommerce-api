from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configurações do projeto, lidas do arquivo .env."""
    # Sem valor padrão: se SECRET_KEY não existir no .env, o servidor
    # se recusa a iniciar e mostra um erro claro. Isso é proposital:
    # é melhor falhar na partida do que rodar com uma chave ausente.
    SECRET_KEY: str

    # Aqui há valor padrão. Se a linha sumir do .env, usa HS256 e 30.
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # env_file diz qual arquivo ler. O caminho ".env" é relativo à pasta
    # de onde o servidor é iniciado, que é a pasta ecommerce.
    # extra="ignore" evita erro se o .env tiver outras linhas no futuro.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Criamos UMA instância aqui. O resto do projeto importa "settings"
# e lê os valores dela, sem ler o arquivo de novo a cada uso.
settings = Settings()
   