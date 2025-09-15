# manage_item.py
import pymysql

from db import get_db_connection

def get_devices_with_details():
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # for mysql.connector
            cursor.execute("""
                SELECT 
                    d.device_id,
                    d.device_name,
                    d.department_id,
                    dept.department_name,
                    (
                        SELECT COUNT(*) 
                        FROM concern_devices 
                        WHERE device_id = d.device_id
                    ) AS concern_count
                FROM devices d
                LEFT JOIN departments dept 
                    ON d.department_id = dept.department_id
                ORDER BY dept.department_name, d.device_name
            """)
            return cursor.fetchall()
    finally:
        conn.close()


def add_device(device_name, quantity, department_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO devices (device_name, quantity, department_id) VALUES (%s, %s, %s)",
                (device_name, quantity, department_id)
            )
            conn.commit()
    finally:
        conn.close()
