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

    async def fetchval(self, command, *args):
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
        await self.execute(sql, str(tg_id), status)

    async def update_user_language(self, tg_id, chat_lang, status='COMPLETED', *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            chat_lang = $1, status = $2
        WHERE
            tg_id = $3;
        """
        await self.execute(sql, chat_lang, status, str(tg_id))

    async def update_user_phone(self, tg_id, phone, status='COMPLETED', *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            phone = $1, status = $2
        WHERE
            tg_id = $3;
        """
        await self.execute(sql, phone, status, str(tg_id))

    async def is_student_linked(self, student_id: int) -> bool:
        """
        Tekshiradi: student_id allaqachon boshqa user bilan bog'langanmi.

        :param student_id: Tekshirilayotgan student ID
        :return: True - agar bog'langan bo'lsa, aks holda False
        """
        sql = "SELECT COUNT(*) FROM users WHERE student_id = $1;"
        count = await self.fetchval(sql, student_id)
        return count > 0

    async def linked_student_to_user(self, tg_id, student_id, status='COMPLETED', *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            student_id = $1, status = $2
        WHERE
            tg_id = $3;
        """
        await self.execute(sql, student_id, status, str(tg_id))

    async def update_user_status(self, tg_id, status, *args, **kwargs):
        sql = """
        UPDATE
            users
        SET
            status = $1
        WHERE
            tg_id = $2;
        """
        await self.execute(sql, status, str(tg_id))

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

    async def set_student_fullname(self, passport: str, fullname: str) -> None:
        sql = """
        UPDATE
            students
        SET
            fullname = $1
        WHERE
            passport = $2;
        """
        await self.execute(sql, fullname, passport)

    async def set_student_course(self, passport: str, course: str) -> None:
        sql = """
        UPDATE
            students
        SET
            course = $1
        WHERE
            passport = $2;
        """
        await self.execute(sql, course, passport)

    async def set_student_edu_direction(self, passport: str, edu_direction_id: int) -> None:
        sql = """
        UPDATE
            students
        SET
            edu_direction_id = $1
        WHERE
            passport = $2;
        """
        await self.execute(sql, edu_direction_id, passport)

    async def set_student_edu_type(self, passport: str, edu_type_id: int) -> None:
        sql = """
        UPDATE
            students
        SET
            edu_type_id = $1
        WHERE
            passport = $2;
        """
        await self.execute(sql, edu_type_id, passport)

    async def set_student_edu_lang(self, passport: str, edu_lang: str) -> None:
        sql = """
        UPDATE
            students
        SET
            edu_lang = $1
        WHERE
            passport = $2;
        """
        await self.execute(sql, edu_lang, passport)

    async def get_edu_directions(self) -> list[dict]:
        sql = """
        SELECT id, name_uz, name_ru FROM edu_directions;
        """
        return await self.fetch(sql)

    async def get_edu_types(self) -> list[dict]:
        sql = """
        SELECT id, name_uz, name_ru FROM edu_types;
        """
        return await self.fetch(sql)

    async def get_next_upcoming_event(self):
        sql = """
            SELECT 
                id,
                name_uz,
                name_ru,
                description_uz,
                description_ru,
                date,
                default_price
            FROM events
            WHERE status = 'no_started' AND is_active = TRUE
              AND date > NOW()
            ORDER BY date ASC
            LIMIT 1;
        """
        return await self.fetchrow(sql)

    async def get_available_tickets_count(self, event_id):
        sql = """
            SELECT COUNT(*)
            FROM tickets
            WHERE event_id = $1 AND is_booking = FALSE
        """
        return await self.fetchval(sql, event_id)

    async def has_user_booked_ticket(self, event_id, user_id):
        sql = """
            SELECT
                tickets.price AS ticket_price,
                tickets.is_paid AS ticket_is_paid,
                tickets.is_booking AS ticket_is_booking,
                tickets.booking_at AS ticket_booking_at,
                seats.number AS seat_number,
                lines.number AS line_number,
                sectors.name AS sector_name
            FROM tickets
            JOIN seats ON tickets.seat_id = seats.id
            JOIN lines ON seats.line_id = lines.id
            JOIN sectors ON lines.sector_id = sectors.id
            WHERE tickets.event_id = $1 AND tickets.user_id = $2 AND tickets.is_booking = TRUE
        """
        return await self.fetchrow(sql, event_id, str(user_id))

    async def get_first_unbooked_ticket(self, event_id):
        sql = """
            SELECT
                tickets.id AS ticket_id,
                tickets.price AS ticket_price,
                seats.number AS seat_number,
                lines.number AS line_number,
                sectors.name AS sector_name
            FROM tickets
            JOIN seats ON tickets.seat_id = seats.id
            JOIN lines ON seats.line_id = lines.id
            JOIN sectors ON lines.sector_id = sectors.id
            WHERE tickets.event_id = $1 AND tickets.is_booking = FALSE
            ORDER BY tickets.created_at ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        """
        return await self.fetchrow(sql, event_id)

    async def booking_ticket(self, ticket_id, user_id):
        sql = """
            UPDATE tickets
            SET is_booking = TRUE, booking_at = NOW(), user_id = $1, updated_at = NOW()
            WHERE id = $2;
        """
        await self.execute(sql, str(user_id), ticket_id)
