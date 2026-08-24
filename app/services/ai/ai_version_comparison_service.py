"""
AI version comparison service.

This module compares two versions of a document section
and detects additions, deletions and modifications,
including the exact line locations of the changes.
"""

from __future__ import annotations

import difflib

from app.models.version import Version


class AIVersionComparisonService:
    """
    Service responsible for comparing two section versions.
    """

    # ==========================================================
    # COMPARE VERSIONS
    # ==========================================================

    def compare_versions(
        self,
        old_version: Version,
        new_version: Version,
    ) -> dict:
        """
        Compare an old version with a new version.

        Returns:
            A structured comparison containing:
            - additions
            - deletions
            - modifications
            - unchanged
            - exact change locations
        """

        old_content = (
            old_version.content_snapshot or ""
        )

        new_content = (
            new_version.content_snapshot or ""
        )

        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()

        matcher = difflib.SequenceMatcher(
            None,
            old_lines,
            new_lines,
        )

        additions = []
        deletions = []
        modifications = []

        for (
            tag,
            old_start,
            old_end,
            new_start,
            new_end,
        ) in matcher.get_opcodes():

            # ==================================================
            # ADDITION
            # ==================================================

            if tag == "insert":

                additions.append(
                    {
                        "type": "addition",
                        "new_start": new_start + 1,
                        "new_end": new_end,
                        "content": new_lines[
                            new_start:new_end
                        ],
                    }
                )

            # ==================================================
            # DELETION
            # ==================================================

            elif tag == "delete":

                deletions.append(
                    {
                        "type": "deletion",
                        "old_start": old_start + 1,
                        "old_end": old_end,
                        "content": old_lines[
                            old_start:old_end
                        ],
                    }
                )

            # ==================================================
            # MODIFICATION
            # ==================================================

            elif tag == "replace":

                modifications.append(
                    {
                        "type": "modification",

                        "old_start": old_start + 1,
                        "old_end": old_end,

                        "new_start": new_start + 1,
                        "new_end": new_end,

                        "old": old_lines[
                            old_start:old_end
                        ],

                        "new": new_lines[
                            new_start:new_end
                        ],
                    }
                )

        # ======================================================
        # RETURN RESULT
        # ======================================================

        return {
            "old_version_id": old_version.id,
            "new_version_id": new_version.id,

            "old_version_number": (
                old_version.version_number
            ),

            "new_version_number": (
                new_version.version_number
            ),

            "additions": additions,
            "deletions": deletions,
            "modifications": modifications,

            "has_changes": bool(
                additions
                or deletions
                or modifications
            ),
        }