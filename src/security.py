import bcrypt

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