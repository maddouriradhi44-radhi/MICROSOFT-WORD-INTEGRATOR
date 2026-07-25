"""
Project model.

This module defines the Project model,
which represents a collaborative project.
"""

from datetime import datetime
from sqlalchemy import DateTime,Enum,ForeignKey,Integer,String,Text
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base
from app.enums.project_status import ProjectStatus

class project(Base):
     """
    Represents a collaborative project.

    A project contains members, documents,
    sections, and collaboration workflows.
    """

    #Primery Key
     id: Mapped[int] = mapped_column(
         Integer,
         primary_key=True,
         autoincrement= True
    )

     # Project Information
       # Project name
     name: Mapped[str] = mapped_column(
          String(255),
          nullable=False
     )

       # Project description
     description: Mapped[str] = mapped_column(
          Text,
          nullable=False
     )

      # Current project status
     status: Mapped[ProjectStatus]=mapped_column(
         DateTime,
         default=datetime.utcnow,
         nullable=False
      )

      # Audit Information
        # Date and time when the project was created
     created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
