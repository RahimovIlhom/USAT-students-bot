import asyncpg

from data import config


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if self.pool is None:  # Avoid redundant initialization
            try:
                self.pool = await asyncpg.create_pool(
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    host=config.DB_HOST,
                    database=config.DB_NAME,
                    min_size=1,
                    max_size=10,
                    timeout=10
                )
            except Exception as e:
                raise RuntimeError(f"Error connecting to the database: {e}")

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()  # Correctly await the pool closing

    async def execute(self, command, *args) -> None:
        await self._query("execute", command, *args)

    async def fetch(self, command, *args) -> list[dict]:
        result = await self._query("fetch", command, *args)
        return [dict(row) for row in result] if result else []

    async def fetchrow(self, command, *args) -> dict | None:
        result = await self._query("fetchrow", command, *args)
        return dict(result) if result else None

    async def fetchval(self, command, *args) -> str | None:
        return await self._query("fetchval", command, *args)

    async def _query(self, query_type, command, *args):
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized. Call `connect()` first.")

        try:
            async with self.pool.acquire() as connection:
                return await getattr(connection, query_type)(command, *args)
        except asyncpg.PostgresError as e:
            raise RuntimeError(f"Database query failed: {e}")

    async def get_user(self, tg_id) -> dict | None:
        sql = """
        SELECT 
            tg_id, 
            phone,
            chat_lang,
            status
        FROM
            users
        WHERE
            tg_id = $1;
        """
        return await self.fetchrow(sql, tg_id)

    async def add_draft_user(self, tg_id, status, *args, **kwargs):
        sql = """
        INSERT INTO
            users (tg_id, status, created_at, updated_at)
        VALUES
            ($1, $2, now(), now());
        """
        return await self.execute(sql, str(tg_id), status)

    async def update_user_language(self, tg_id, chat_lang, status='COMPLETED', *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            chat_lang = $1, status = $2
        WHERE
            tg_id = $3;
        """
        return await self.execute(sql, chat_lang, status, str(tg_id))

    async def update_user_phone(self, tg_id, phone, status='COMPLETED', *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            phone = $1, status = $2
        WHERE
            tg_id = $3;
        """
        return await self.execute(sql, phone, status, str(tg_id))

    async def update_user_passport(self, tg_id, student_id, status='COMPLETED', *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            student_id = $1, status = $2
        WHERE
            tg_id = $3;
        """
        return await self.execute(sql, student_id, status, str(tg_id))

    async def update_user_status(self, tg_id, status, *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            status = $1
        WHERE
            tg_id = $2;
        """
        return await self.execute(sql, status, str(tg_id))

    async def get_student(self, passport: str) -> dict | None:
        sql = """
        SELECT 
            s.id,
            s.fullname, 
            s.passport, 
            s.pinfl, 
            s.course, 
            ed.name_uz AS edu_direction_name_uz, 
            ed.name_ru AS edu_direction_name_ru, 
            et.name_uz AS edu_type_name_uz, 
            et.name_ru AS edu_type_name_ru, 
            s.edu_lang, 
            s.contract_amount, 
            s.voucher_amount, 
            s.currency
        FROM 
            students s
        LEFT JOIN 
            edu_directions ed ON s.edu_direction_id = ed.id
        LEFT JOIN 
            edu_types et ON s.edu_type_id = et.id
        WHERE 
            s.passport = $1;
        """
        return await self.fetchrow(sql, passport)
