from psycopg_pool import AsyncConnectionPool


async def setup_postgres():
    pool = AsyncConnectionPool()
    # TODO: Set up tenacity
    await pool.open(wait=True)

