import json
import os


def load_secrets_into_env() -> None:
    secret_name = os.environ.get("PORTER_SECRETS_NAME")
    if not secret_name:
        return

    import boto3

    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    secrets: dict = json.loads(response["SecretString"])

    db_url = (
        f"postgresql://{secrets['DATABASE_USER']}:{secrets['DATABASE_PASSWORD']}"
        f"@{secrets['DATABASE_HOST']}:{secrets['DATABASE_PORT']}/{secrets['DATABASE_NAME']}"
    )

    os.environ["DATABASE_URL"] = db_url
    os.environ["SECRET_KEY"] = secrets["SECRET_KEY"]
    os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]
