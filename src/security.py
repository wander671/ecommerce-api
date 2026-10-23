from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from src.config import settings

def hash_password(password: str) -> str:
    """""Transforma a senha digitada em um hash para guardar no banco de dados."""
    # O bcrypt trabalha com bytes, não com texto. O encode converte
    # a senha (str) em bytes usando a codificação UTF-8.
    password_bytes = password.encode("utf-8")

    # O "salt" é um texto aleatório misturado à senha antes do hash.
    # Ele garante que duas pessoas com a MESMA senha tenham hashes
    # DIFERENTES no banco, o que impede que alguém descubra senhas
    # repetidas olhando a tabela.
    salt = bcrypt.gensalt()

    # hashed faz o embaralhamento em si. O resultado é irreversível:
    # não existe função que devolva a senha original a partir do hash
    hashed = bcrypt.hashpw(password_bytes, salt)   

    # Retorna o hash como uma string (não bytes).
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """""Verifica se a senha digitada bate com o hash guardado no banco de dados."""
    # O bcrypt trabalha com bytes, não com texto. O encode converte
    # a senha (str) em bytes usando a codificação UTF-8.
    password_bytes = password.encode("utf-8")

    # O hash também precisa ser convertido para bytes.
    hashed_bytes = hashed.encode("utf-8")

    # A função checkpw devolve True se a senha bate com o hash,
    # e False caso contrário.
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(subject: str) -> str:
    """Gera um token JWT assinado para o usuário identificado por 'subject'."""
    # Momento em que o token deixa de valer: agora + 30 minutos
    # (o número vem do .env, via settings).
    # timezone.utc deixa a hora sem ambiguidade. Sem fuso, o Python
    # não sabe se a hora é local ou universal, e isso gera bugs.
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # O conteúdo do crachá. "sub" (subject, o assunto) diz de quem é o
    # token, e aqui vamos usar o e-mail. "exp" é a validade.
    # Esses nomes são padrão do JWT, e quem lê o token sabe o que significam
    payload = {"sub": subject, "exp": expire}

    # Aqui o token é montado e ASSINADO com a chave secreta.
    # O resultado é o texto de três partes separadas por ponto
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)