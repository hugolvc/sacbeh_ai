"""
Data connectors using Abstract Factory pattern.
Provides seamless switching between different database implementations.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Type
import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

from .auth_models import (
    UserAuth, Role, UserRole, Session, LoginAttempt, 
    AuthStatus, Permission, AuthUtils
)
from .data_models import User, UserRole as UserRoleEnum


class DatabaseConnector(ABC):
    """Abstract base class for database connectors."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results."""
        pass
    
    @abstractmethod
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        pass
    
    @abstractmethod
    def begin_transaction(self) -> None:
        """Begin a database transaction."""
        pass
    
    @abstractmethod
    def commit_transaction(self) -> None:
        """Commit the current transaction."""
        pass
    
    @abstractmethod
    def rollback_transaction(self) -> None:
        """Rollback the current transaction."""
        pass


class SQLiteConnector(DatabaseConnector):
    """SQLite database connector implementation."""
    
    def __init__(self, database_path: str = "sacbeh_auth.db"):
        self.database_path = database_path
        self.connection: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize the database with required tables."""
        self.connect()
        
        # Create tables if they don't exist
        self._create_tables()
        
        # Insert default roles if they don't exist
        self._insert_default_roles()
        
        self.disconnect()
    
    def _create_tables(self) -> None:
        """Create all required database tables."""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS user_auth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                failed_login_attempts INTEGER DEFAULT 0,
                locked_until TEXT,
                password_changed_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                email_verified BOOLEAN DEFAULT 0,
                verification_token TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                permissions TEXT NOT NULL,
                is_default BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                assigned_at TEXT NOT NULL,
                assigned_by INTEGER,
                expires_at TEXT,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES user_auth (id),
                FOREIGN KEY (role_id) REFERENCES roles (id),
                FOREIGN KEY (assigned_by) REFERENCES user_auth (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_token TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                is_active BOOLEAN DEFAULT 1,
                last_activity TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user_auth (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                success BOOLEAN NOT NULL,
                attempted_at TEXT NOT NULL,
                failure_reason TEXT
            )
            """
        ]
        
        for table_sql in tables:
            self.execute_update(table_sql)
    
    def _insert_default_roles(self) -> None:
        """Insert default roles into the database."""
        default_roles = [
            {
                "name": "admin",
                "description": "System administrator with full access",
                "permissions": ",".join([p.value for p in Permission]),
                "is_default": False
            },
            {
                "name": "user",
                "description": "Standard user with basic permissions",
                "permissions": ",".join([Permission.READ.value, Permission.WRITE.value]),
                "is_default": True
            },
            {
                "name": "guest",
                "description": "Guest user with read-only access",
                "permissions": Permission.READ.value,
                "is_default": False
            }
        ]
        
        for role_data in default_roles:
            # Check if role already exists
            existing = self.execute_query(
                "SELECT id FROM roles WHERE name = ?", 
                (role_data["name"],)
            )
            
            if not existing:
                self.execute_update(
                    """
                    INSERT INTO roles (name, description, permissions, is_default, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        role_data["name"],
                        role_data["description"],
                        role_data["permissions"],
                        role_data["is_default"],
                        datetime.now().isoformat(),
                        datetime.now().isoformat()
                    )
                )
    
    def connect(self) -> None:
        """Establish SQLite database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.database_path,
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
    
    def disconnect(self) -> None:
        """Close SQLite database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows
    
    def begin_transaction(self) -> None:
        """Begin a database transaction."""
        self.connect()
        self.connection.execute("BEGIN TRANSACTION")
    
    def commit_transaction(self) -> None:
        """Commit the current transaction."""
        if self.connection:
            self.connection.commit()
    
    def rollback_transaction(self) -> None:
        """Rollback the current transaction."""
        if self.connection:
            self.connection.rollback()
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        try:
            self.begin_transaction()
            yield self
            self.commit_transaction()
        except Exception:
            self.rollback_transaction()
            raise


class DatabaseConnectorFactory:
    """Abstract Factory for creating database connectors."""
    
    _connectors: Dict[str, Type[DatabaseConnector]] = {
        "sqlite": SQLiteConnector
    }
    
    @classmethod
    def register_connector(cls, name: str, connector_class: Type[DatabaseConnector]) -> None:
        """Register a new database connector type."""
        cls._connectors[name] = connector_class
    
    @classmethod
    def create_connector(cls, connector_type: str, **kwargs) -> DatabaseConnector:
        """
        Create a database connector instance.
        
        Args:
            connector_type: Type of connector to create
            **kwargs: Additional arguments for the connector
            
        Returns:
            DatabaseConnector instance
            
        Raises:
            ValueError: If connector type is not supported
        """
        if connector_type not in cls._connectors:
            raise ValueError(f"Unsupported connector type: {connector_type}")
        
        connector_class = cls._connectors[connector_type]
        return connector_class(**kwargs)
    
    @classmethod
    def get_supported_connectors(cls) -> List[str]:
        """Get list of supported connector types."""
        return list(cls._connectors.keys())


# Convenience function for creating default SQLite connector
def create_default_connector() -> DatabaseConnector:
    """Create a default SQLite database connector."""
    return DatabaseConnectorFactory.create_connector("sqlite") 