#!/usr/bin/env python3
"""
copy_db.py — copia i DATI (non lo schema) da un database all'altro.

I due DB devono stare sulla stessa istanza e avere lo schema gia' creato.

Uso:
    poetry run python copy_db.py <source_db> <target_db>
    # es.
    poetry run python copy_db.py myinves_prod myinves_test

Usa le librerie del progetto (asyncpg + pydantic-settings): nessun binario
esterno tipo psql/pg_dump. Le tabelle vengono svuotate sul target e
ricaricate in ordine che rispetta le foreign key.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

import asyncpg
from pydantic_settings import BaseSettings, SettingsConfigDict

# Tabelle di contabilita' delle migrazioni: non vanno copiate/sovrascritte
YOYO_PREFIXES = ("_yoyo", "yoyo")


def find_env_file() -> Path:
    """Cerca il .env accanto allo script, in backend/ o nella cartella superiore."""
    here = Path(__file__).resolve().parent
    for candidate in (here / ".env", here / "backend" / ".env", here.parent / ".env"):
        if candidate.is_file():
            return candidate
    raise SystemExit(f".env non trovato vicino a {here}")


class DbSettings(BaseSettings):
    postgresql_user: str
    postgresql_password: str
    postgresql_host: str
    postgresql_port: str = "5432"

    model_config = SettingsConfigDict(extra="ignore")

    def connect_kwargs(self) -> dict:
        return {
            "host": self.postgresql_host,
            "port": int(self.postgresql_port),
            "user": self.postgresql_user,
            "password": self.postgresql_password,
        }


def q(identifier: str) -> str:
    """Quoting sicuro di un identificatore SQL."""
    return '"' + identifier.replace('"', '""') + '"'


async def list_tables(conn: asyncpg.Connection) -> list[str]:
    rows = await conn.fetch(
        """
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND NOT starts_with(tablename, $1)
          AND NOT starts_with(tablename, $2)
        ORDER BY tablename
        """,
        *YOYO_PREFIXES,
    )
    return [r["tablename"] for r in rows]


async def fk_order(conn: asyncpg.Connection, tables: list[str]) -> list[str]:
    """Ordina le tabelle in modo che quelle referenziate vengano prima."""
    rows = await conn.fetch(
        """
        SELECT rel.relname AS tbl, frel.relname AS ref
        FROM pg_constraint c
        JOIN pg_class rel  ON rel.oid  = c.conrelid
        JOIN pg_class frel ON frel.oid = c.confrelid
        JOIN pg_namespace n ON n.oid = c.connamespace
        WHERE c.contype = 'f' AND n.nspname = 'public'
        """
    )
    deps: dict[str, set[str]] = {t: set() for t in tables}
    for r in rows:
        tbl, ref = r["tbl"], r["ref"]
        if tbl in deps and ref in deps and tbl != ref:
            deps[tbl].add(ref)

    ordered: list[str] = []
    seen: set[str] = set()

    def visit(node: str) -> None:
        if node in seen:
            return
        seen.add(node)
        for dep in sorted(deps[node]):
            visit(dep)
        ordered.append(node)

    for table in sorted(tables):
        visit(table)
    return ordered


async def columns_of(conn: asyncpg.Connection, table: str) -> list[str]:
    rows = await conn.fetch(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = $1
        ORDER BY ordinal_position
        """,
        table,
    )
    return [r["column_name"] for r in rows]


async def truncate(conn: asyncpg.Connection, tables: list[str]) -> None:
    stmt = "TRUNCATE TABLE " + ", ".join(q(t) for t in tables) + " RESTART IDENTITY CASCADE"
    await conn.execute(stmt)


async def copy_table(
    src: asyncpg.Connection, dst: asyncpg.Connection, table: str
) -> int:
    cols = await columns_of(src, table)
    if not cols:
        return 0

    col_list = ", ".join(q(c) for c in cols)
    placeholders = ", ".join(f"${i + 1}" for i in range(len(cols)))
    select_sql = f"SELECT {col_list} FROM {q(table)}"
    insert_sql = f"INSERT INTO {q(table)} ({col_list}) VALUES ({placeholders})"

    rows = await src.fetch(select_sql)
    if rows:
        async with dst.transaction():
            await dst.executemany(insert_sql, [tuple(r) for r in rows])
    return len(rows)


async def run(source_db: str, target_db: str) -> int:
    if source_db == target_db:
        raise SystemExit("Source e target non possono coincidere.")

    settings = DbSettings(_env_file=find_env_file())  # type: ignore[call-arg]
    kwargs = settings.connect_kwargs()

    src = await asyncpg.connect(**kwargs, database=source_db)
    try:
        dst = await asyncpg.connect(**kwargs, database=target_db)
        try:
            tables = await list_tables(dst)
            if not tables:
                raise SystemExit(f"Nessuna tabella trovata in '{target_db}'.")

            ordered = await fk_order(dst, tables)

            print(f"==> Svuoto le tabelle su '{target_db}'")
            await truncate(dst, tables)

            print(f"==> Copia dati: {source_db} -> {target_db}")
            for table in ordered:
                n = await copy_table(src, dst, table)
                print(f"    {table:<20} {n:>8} righe")

            print("==> Verifica contaggi")
            ok = True
            for table in ordered:
                s = await src.fetchval(f"SELECT count(*) FROM {q(table)}")
                d = await dst.fetchval(f"SELECT count(*) FROM {q(table)}")
                mark = "OK" if s == d else "MISMATCH"
                if s != d:
                    ok = False
                print(f"    {table:<20} source={s:<8} target={d:<8} {mark}")
        finally:
            await dst.close()
    finally:
        await src.close()

    if not ok:
        print("==> ATTENZIONE: alcuni conteggi non coincidono.", flush=True)
        return 1
    print("==> Fatto.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copia i dati (non lo schema) da un database all'altro.",
    )
    parser.add_argument("source_db", help="nome del database sorgente")
    parser.add_argument("target_db", help="nome del database di destinazione")
    args = parser.parse_args()
    return asyncio.run(run(args.source_db, args.target_db))


if __name__ == "__main__":
    raise SystemExit(main())
