import logging
import pymysql
from datetime import datetime

class DBLogHandler(logging.Handler):
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config

    def emit(self, record):
        try:
            connection = pymysql.connect(**self.db_config)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO logs (timestamp, level, message, module, `function`)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    datetime.fromtimestamp(record.created),
                    record.levelname,
                    self.format(record),
                    record.module,
                    record.funcName
                ))
                connection.commit()
        except Exception as e:
            print("DB logging failed:", e)
        finally:
            try:
                connection.close()
            except:
                pass
