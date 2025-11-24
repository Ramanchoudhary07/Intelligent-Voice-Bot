"""
Database module for backend integration
"""
from typing import Optional, Dict, List
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()


class QueryLog(Base):
    """Model for storing query logs"""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(Text, nullable=False)
    intent = Column(String(100))
    response = Column(Text)
    response_time = Column(Integer)  # in milliseconds
    timestamp = Column(DateTime, default=datetime.utcnow)
    error = Column(Text, nullable=True)


class User(Base):
    """Model for storing user credentials"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        """Initialize database connection"""
        self.engine = None
        self.Session = None
        self.db_type = settings.database_type.lower()
        
        if self.db_type == "postgresql" and settings.database_url:
            try:
                self.engine = create_engine(settings.database_url)
                Base.metadata.create_all(self.engine)
                self.Session = sessionmaker(bind=self.engine)
                logger.info("PostgreSQL database connection established")
            except Exception as e:
                logger.error(f"Error connecting to PostgreSQL: {str(e)}")
        elif self.db_type == "sqlite":
            try:
                # Default to local sqlite file if no URL provided
                db_url = settings.database_url or f"sqlite:///{settings.base_dir}/voice_bot.db"
                self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
                Base.metadata.create_all(self.engine)
                self.Session = sessionmaker(bind=self.engine)
                logger.info(f"SQLite database connection established at {db_url}")
            except Exception as e:
                logger.error(f"Error connecting to SQLite: {str(e)}")
        elif self.db_type == "mongodb":
            # MongoDB connection can be added here
            logger.warning("MongoDB support not yet implemented")
        else:
            logger.warning("No database configuration found")
    
    def log_query(
        self,
        query_text: str,
        intent: str,
        response: str,
        response_time: int,
        error: Optional[str] = None
    ):
        """
        Log a query and response
        
        Args:
            query_text: User query text
            intent: Detected intent
            response: Generated response
            response_time: Response time in milliseconds
            error: Error message if any
        """
        if not self.Session:
            return
        
        try:
            session = self.Session()
            log_entry = QueryLog(
                query_text=query_text,
                intent=intent,
                response=response,
                response_time=response_time,
                error=error
            )
            session.add(log_entry)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Error logging query: {str(e)}")
    
    def get_account_info(self, account_id: str) -> Optional[Dict]:
        """
        Retrieve account information (placeholder - implement based on your backend)
        
        Args:
            account_id: Account identifier
            
        Returns:
            Account information dictionary
        """
        # This is a placeholder - implement based on your actual backend API
        if settings.backend_api_url:
            # Make API call to backend
            import requests
            try:
                response = requests.get(
                    f"{settings.backend_api_url}/accounts/{account_id}"
                )
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logger.error(f"Error fetching account info: {str(e)}")
        
        return None
    
    def get_faqs(self, query: str) -> List[Dict]:
        """
        Retrieve relevant FAQs (placeholder - implement based on your backend)
        
        Args:
            query: Search query for FAQs
            
        Returns:
            List of relevant FAQs
        """
        # This is a placeholder - implement based on your actual backend API
        if settings.backend_api_url:
            import requests
            try:
                response = requests.get(
                    f"{settings.backend_api_url}/faqs",
                    params={"q": query}
                )
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logger.error(f"Error fetching FAQs: {str(e)}")
        
        return []

    def get_recent_queries(self, limit: int = 20) -> List[Dict]:
        """
        Retrieve recent queries from the query log table.

        Args:
            limit: Maximum number of recent queries to return

        Returns:
            List of dicts with keys: id, query_text, intent, response, response_time, timestamp, error
        """
        if not self.Session:
            return []

        try:
            session = self.Session()
            results = session.query(QueryLog).order_by(QueryLog.id.desc()).limit(limit).all()
            session.close()

            out = []
            for r in results:
                out.append({
                    "id": r.id,
                    "query_text": r.query_text,
                    "intent": r.intent,
                    "response": r.response,
                    "response_time": r.response_time,
                    "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                    "error": r.error,
                })
            return out
            return []
        except Exception as e:
            logger.error(f"Error retrieving recent queries: {str(e)}")
            return []

    def create_user(self, username, password_hash):
        """Create a new user"""
        if not self.Session:
            return False
        
        try:
            session = self.Session()
            user = User(username=username, password_hash=password_hash)
            session.add(user)
            session.commit()
            session.close()
            return True
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return False

    def get_user_by_username(self, username):
        """Get user by username"""
        if not self.Session:
            return None
        
        try:
            session = self.Session()
            user = session.query(User).filter_by(username=username).first()
            session.close()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user: {str(e)}")
            return None

