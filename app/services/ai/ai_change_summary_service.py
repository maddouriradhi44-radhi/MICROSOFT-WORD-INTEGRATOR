"""
AI change summary service.

This module generates a structured summary
from a version comparison result.
"""

from __future__ import annotations


class AIChangeSummaryService:
    """
    Service responsible for summarizing changes
    detected between two document versions.
    """

    # ==========================================================
    # GENERATE SUMMARY
    # ==========================================================

    def generate_summary(
        self,
        comparison: dict,
    ) -> dict:
        """
        Generate an automatic summary from
        a version comparison.
        """

        additions = comparison.get(
            "additions",
            [],
        )

        deletions = comparison.get(
            "deletions",
            [],
        )

        modifications = comparison.get(
            "modifications",
            [],
        )

        # ------------------------------------------------------
        # Count changes
        # ------------------------------------------------------

        addition_count = len(additions)
        deletion_count = len(deletions)
        modification_count = len(modifications)

        total_changes = (
            addition_count
            + deletion_count
            + modification_count
        )

        # ------------------------------------------------------
        # Summary
        # ------------------------------------------------------

        if total_changes == 0:

            summary = (
                "No changes were detected "
                "between the two versions."
            )

        else:

            parts = []

            if addition_count > 0:
                parts.append(
                    f"{addition_count} addition"
                    f"{'s' if addition_count != 1 else ''}"
                )

            if deletion_count > 0:
                parts.append(
                    f"{deletion_count} deletion"
                    f"{'s' if deletion_count != 1 else ''}"
                )

            if modification_count > 0:
                parts.append(
                    f"{modification_count} modification"
                    f"{'s' if modification_count != 1 else ''}"
                )

            summary = (
                "The new version contains "
                + ", ".join(parts)
                + "."
            )

        # ------------------------------------------------------
        # Important changes
        # ------------------------------------------------------

        important_changes = []

        # ======================================================
        # ADDITIONS
        # ======================================================

        for addition in additions:

            if not isinstance(
                addition,
                dict,
            ):
                continue

            content = addition.get(
                "content",
                [],
            )

            if not content:
                continue

            important_changes.append(
                {
                    "type": "addition",
                    "new_start": addition.get(
                        "new_start"
                    ),
                    "new_end": addition.get(
                        "new_end"
                    ),
                    "content": content,
                }
            )

        # ======================================================
        # DELETIONS
        # ======================================================

        for deletion in deletions:

            if not isinstance(
                deletion,
                dict,
            ):
                continue

            content = deletion.get(
                "content",
                [],
            )

            if not content:
                continue

            important_changes.append(
                {
                    "type": "deletion",
                    "old_start": deletion.get(
                        "old_start"
                    ),
                    "old_end": deletion.get(
                        "old_end"
                    ),
                    "content": content,
                }
            )

        # ======================================================
        # MODIFICATIONS
        # ======================================================

        for modification in modifications:

            if not isinstance(
                modification,
                dict,
            ):
                continue

            important_changes.append(
                {
                    "type": "modification",

                    "old_start": modification.get(
                        "old_start"
                    ),

                    "old_end": modification.get(
                        "old_end"
                    ),

                    "new_start": modification.get(
                        "new_start"
                    ),

                    "new_end": modification.get(
                        "new_end"
                    ),

                    "old": modification.get(
                        "old",
                        [],
                    ),

                    "new": modification.get(
                        "new",
                        [],
                    ),
                }
            )

        return {
            "summary": summary,

            "important_changes": (
                important_changes
            ),

            "total_changes": total_changes,

            "addition_count": addition_count,

            "deletion_count": deletion_count,

            "modification_count": (
                modification_count
            ),
        }