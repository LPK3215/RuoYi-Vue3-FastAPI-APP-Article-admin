import argparse
import os
import sys

import pymysql
from pymysql.constants import CLIENT


def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main() -> int:
    parser = argparse.ArgumentParser(description='Run MySQL .sql file against configured DB.')
    parser.add_argument('sql_file', help='Path to .sql file (relative to backend root or absolute)')
    args = parser.parse_args()

    backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_path = args.sql_file
    if not os.path.isabs(sql_path):
        sql_path = os.path.join(backend_root, sql_path)
    if not os.path.exists(sql_path):
        print(f'[run_sql] file not found: {sql_path}', file=sys.stderr)
        return 2

    host = os.getenv('DB_HOST', '127.0.0.1')
    port = int(os.getenv('DB_PORT', '3306'))
    user = os.getenv('DB_USERNAME', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_DATABASE', 'ruoyi-fastapi')

    sql = read_text(sql_path)
    if not sql.strip():
        print(f'[run_sql] empty sql: {sql_path}', file=sys.stderr)
        return 3

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4',
        autocommit=False,
        client_flag=CLIENT.MULTI_STATEMENTS,
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        print(f'[run_sql] OK: {os.path.relpath(sql_path, backend_root)}')
        return 0
    except Exception as exc:
        conn.rollback()
        print(f'[run_sql] FAILED: {exc}', file=sys.stderr)
        return 1
    finally:
        conn.close()


if __name__ == '__main__':
    raise SystemExit(main())

