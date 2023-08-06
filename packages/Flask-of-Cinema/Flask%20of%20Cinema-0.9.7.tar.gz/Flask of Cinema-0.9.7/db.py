import os
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine

# HACK quick way to toggle echo mode for the engines
# is_dev = True
is_dev = False

load_dotenv()




# Scelta automatica dell'uri in base all'ambiente
if getenv("IS_DOCKER"):
    # utilizza uri docker
    uri = getenv("DB_URI_DOCKER")
    print('Sei connesso al server di Docker')
else:
    # Usa uri di Heroku
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    uri = os.environ['DATABASE_URL']
    print('Sei connesso al server di Heroku')

engine = create_engine(uri, echo=is_dev)


# Crea la connessione con l'isolamento desiderato
def create_conn(transaction_isolation="AUTOCOMMIT"):
    """Create connection with the transaction isolation level specified."""
    conn = engine.connect()
    return update_conn(conn, transaction_isolation)


# Modifica l'isolamento di una connessione esistente
def update_conn(old_connection, transaction_isolation="AUTOCOMMIT"):
    """Update connection to use the transaction isolation level specified."""
    return old_connection.execution_options(isolation_level=transaction_isolation)
