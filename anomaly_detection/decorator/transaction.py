from functools import wraps
from anomaly_detection.utils.logger import logger

from anomaly_detection.db.database import Database


def transaction(func):
    """
      Decorator to handle database session
      :param session:
      :return:
      """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_instance = Database()
        session = db_instance.get_session()
        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
        finally:
            session.close()
            logger.info("Session closed")
    return wrapper