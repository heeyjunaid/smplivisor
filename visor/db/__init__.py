import psycopg2

import visor.config as config
from visor.utils import init_logger

logger = init_logger(__name__)

# Establish a database connection
def get_db_connection():
    try:
        return psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
    except Exception as err:
        logger.exception(err)
        raise Exception("Some issue with connecting DB")

        
DB_CONN = get_db_connection()


def run_query(query, data = ()):
    logger.info(f"runnnig db query| {query}")
    cursor = DB_CONN.cursor()

    if len(data) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    
    DB_CONN.commit()
    cursor.close()

def fetch_one(query, params=()):
    logger.info(f"runnnig db query| {query}")
    cursor = DB_CONN.cursor()
    if len(params) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    res = cursor.fetchone()

    cursor.close()
    return res



def fetch_all(query, params=()):
    logger.info(f"runnnig db query| {query}")
    cursor = DB_CONN.cursor()
    if len(params) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, params)    
    res = cursor.fetchall()

    cursor.close()
    return res