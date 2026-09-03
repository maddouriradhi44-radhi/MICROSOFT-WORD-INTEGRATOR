"""
Section repository.

This module handles database operations
related to document sections.
"""


from sqlalchemy.orm import Session

from app.models.section import Section



class SectionRepository:
    """
    Database operations related to sections.
    """


    def create_section(
        self,
        db: Session,
        section: Section,
    ) -> Section:
        """
        Save a new section into the database.
        """

        db.add(section)
        db.commit()
        db.refresh(section)

        return section



    def create_many(
        self,
        db: Session,
        sections: list[Section],
    ) -> list[Section]:
        """
        Save multiple sections into the database at once.
        """

        db.add_all(sections)
        db.commit()

        for section in sections:
            db.refresh(section)

        return sections

    

    def get_section_by_id(
        self,
        db: Session,
        section_id: int,
    ) -> Section | None:
        """
        Retrieve a section by its ID.
        """

        return (
            db.query(Section)
            .filter(
                Section.id == section_id
            )
            .first()
        )



    def get_document_sections(
        self,
        db: Session,
        document_id: int,
    ) -> list[Section]:
        """
        Retrieve all sections belonging
        to a document.
        """

        return (
            db.query(Section)
            .filter(
                Section.document_id == document_id
            )
            .order_by(
                Section.order
            )
            .all()
        )



    def get_user_sections(
        self,
        db: Session,
        user_id: int,
    ) -> list[Section]:
        """
        Retrieve all sections assigned
        to a specific user.
        """

        return (
            db.query(Section)
            .filter(
                Section.assigned_user_id == user_id
            )
            .all()
        )



    def update_section(
        self,
        db: Session,
        section: Section,
        updates: dict,
    ) -> Section:
        """
        Update an existing section.
        """

        for field, value in updates.items():
            setattr(
                section,
                field,
                value,
            )


        db.commit()
        db.refresh(section)

        return section



    def delete_section(
        self,
        db: Session,
        section: Section,
    ) -> bool:
        """
        Delete a section from the database.
        """

        db.delete(section)
        db.commit()

        return True


    def assign_user(
        self,
        db: Session,
        section: Section,
        user_id: int,
    ) -> Section:
        """
        Assign a user to a section.
        """

        section.assigned_user_id = user_id

        db.commit()
        db.refresh(section)

        return section


    def get_project_sections(
        self,
        db: Session,
        project_id: int,
    ) -> list[Section]:
        """
        Retrieve all sections belonging to a project.
        """

        return (
            db.query(Section)
            .filter(
                Section.project_id == project_id
            )
            .order_by(
                Section.order
            )
            .all()
        )

    
        