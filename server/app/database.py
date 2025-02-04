import time
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")
TABEL_NAME = 'query_resp_data'
TIME_EXPIRATION = 3600 * 24 * 10 # delete records after 10 days since it's creation.
LAST_EXECUTION = time.time()
# PostgreSQL connection parameters
conn = psycopg2.connect(DATABASE_URL)

# Create a cursor object to interact with the database
cur = conn.cursor()


async def create_table(app):
    global conn, cur, TABEL_NAME
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # SQL command to create a table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABEL_NAME} (
            p_key VARCHAR(100) PRIMARY KEY,
            question JSON,
            answer TEXT,
            provider VARCHAR(100),
            model VARCHAR(100),
            timestamp FLOAT,
            miner_hot_key VARCHAR(100),
            miner_uid INTEGER,
            score FLOAT,
            similarity FLOAT,
            vali_uid INTEGER,
            timeout INTEGER,
            time_taken INTEGER,
            epoch_num INTEGER,
            cycle_num INTEGER,
            block_num INTEGER,
            name VARCHAR(100)
        );
        """

        # Execute the SQL command
        cur.execute(create_table_query)
        conn.commit()  # Save changes
        create_index_query = f"""
        CREATE INDEX IF NOT EXISTS question_answer_index ON {TABEL_NAME} (provider, model);
        CREATE INDEX IF NOT EXISTS miner_id_index ON {TABEL_NAME} (miner_uid);
        CREATE INDEX IF NOT EXISTS miner_hot_key_index ON {TABEL_NAME} (miner_hot_key);
        CREATE INDEX IF NOT EXISTS idx_score_sim_timestamp ON {TABEL_NAME} (score, similarity, timestamp);
        CREATE INDEX IF NOT EXISTS idx_block__cycle_epoch_num_ ON {TABEL_NAME} (block_num, cycle_num, epoch_num);
        """
        cur.execute(create_index_query)
        conn.commit()
        print("Table created successfully!")

    except Exception as e:
        print(f"Error creating table: {e}")


def delete_records():
    global TIME_EXPIRATION, LAST_EXECUTION
    if (time.time() - LAST_EXECUTION) < TIME_EXPIRATION:
        return
    LAST_EXECUTION = time.time()
    timestamp = time.time() - TIME_EXPIRATION
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    query_str = f"""
    delete from query_resp_data where timestamp <= {timestamp}
    """
    cur.execute(query_str)
    conn.commit()


create_table(None)
