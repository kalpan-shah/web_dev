# Database Migrations Ledger

This folder contains the database schema migration scripts managed by Alembic. 
Always log applied schema modifications in the ledger below.


## Migration History

### Actions
*   **Up**: Migration script applied forward to the database.
*   **Down**: Migration script rolled back / reverted.
*   **Pending**: Script generated but not yet executed against the live database.


| Date | Revision ID | Description / Tables Affected | Action | Notes / Breaking Changes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-05-14 | `b97800b75bf8` | Initial schema setup (`Posts`) | Pending | Base migration file. |
| 2026-05-15 | `b97800b75bf8` | Initial schema setup (`Posts`) | Up | Base migration Applied |
| 2026-05-22 | `9cf743877585` | Added Users Table (`Users`) | Up | User table added |
| 2026-05-22 | `0cf0fe4b7122` | Added User id Column to Table (`Posts`) | Up | User table added |
| 2026-07-27 | `6b70e3a53fee` | Deleted Posts added Todo (`Posts`, `Users`, `Todo`, `TodoItems`) | Up | Todo table added |





## Quick Reference Commands

### Routine Migrations
*   **Generate an automated migration script:**
    ```bash
    alembic revision --autogenerate -m "your description here"
    ```
*   **Apply all pending migrations to the database:**
    ```bash
    alembic upgrade head
    ```
*   **Rollback the single most recent migration:**
    ```bash
    alembic downgrade -1
    ```

### Inspection & Troubleshooting
*   **Check current database migration state:**
    ```bash
    alembic current
    ```
*   **View history of all generated migration files:**
    ```bash
    alembic history --indicate-current
    ```

---

## Pre-Migration Safety Checklist

Before running `alembic upgrade head`, open the newly generated file in `migrations/versions/` and verify the following rules:

1.  **⚠️ Column Renames (Critical)**
    *   Alembic **cannot** auto-detect a renamed column. It will generate a destructive `drop_column()` followed by an `add_column()`, resulting in total data loss.
    *   **Fix:** Manually delete those lines and replace them with:
        ```python
        op.alter_column('table_name', 'old_column', new_column_name='new_column')
        ```
2.  **🔄 Table Renames**
    *   Alembic will drop the old table and create a new one.
    *   **Fix:** Manually edit the file to use `op.rename_table('old_name', 'new_name')`.
3.  **🧩 Model Discovery**
    *   If a new model table is completely missing from the generated file, ensure the model file is explicitly imported inside `migrations/env.py` so the MetaData class registers it.

---
