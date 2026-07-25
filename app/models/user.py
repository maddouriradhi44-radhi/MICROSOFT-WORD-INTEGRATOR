"""User model

This module defines the User model,witch represents 
an application user in the database.
"""

from datetime import datetime
from sqlalchemy import DATETIME,Enum,Integer,String
from sqlalchemy import Mapped , mapped_column

from app.database.base import Base
from app.enums.user_role import UserRole

class User(Base):
     """
    Represents an application user.

    A user can:
    - Sign in to the application.
    - Import documents.
    - Edit assigned sections.
    - Collaborate with other users.
    """
     __tablename__="users"

     id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Personal Information 
     first_name: Mapped[str] = mapped_column(
         String(100),
         nullable=False
        
    )

     last_name: Mapped[str] = mapped_column(
          String(100),
          nullable=False
     )

    # Authentification 
     email:Mapped[str]=mapped_column(
          String(150),
          unique=True,
          nullable=False
     )    

    #User's hashed passworf(bcrypt)
     password_hush:Mapped[str]= mapped_column(
          String(255),
          nullable=False  
    ) 

     role:Mapped[UserRole]=mapped_column(
          Enum(UserRole,name="user_roles"),
          nullable=False
     )

     # Audit Information 
     #Date and time when the account was created 

     created_at: Mapped[datetime]=mapped_column(
          DATETIME,
          default=datetime.utcnow,
          nullable=False
     )

     