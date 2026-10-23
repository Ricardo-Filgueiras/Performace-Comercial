import psycopg2
import requests

senha = "abc123SEGREDO"
URL_BANCO = "postgres://usuario:p4ssWORD@servidor/db"


def conectar():
    return psycopg2.connect(host="servidor", password="XYZ_SEGREDO")


def baixar():
    return requests.get("https://exemplo.invalid/dados")
