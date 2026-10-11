import csv
import re

from app.database.postgres import get_connection


CSV_FILE = "datasets/ecommerce_customer_behavior_dataset.csv"
TABLE_NAME = "ecommerce_customers"


def clean_column_name(column_name):
    """
    Convert CSV column names into PostgreSQL-friendly names.

    Examples:
        Customer ID -> customer_id
        Purchase Amount (USD) -> purchase_amount_usd
    """

    column_name = column_name.strip().lower()

    column_name = re.sub(r"[^a-zA-Z0-9]+", "_", column_name)

    column_name = column_name.strip("_")

    if column_name and column_name[0].isdigit():
        column_name = f"column_{column_name}"

    return column_name


def get_columns():
    """
    Read only the CSV header and return cleaned column names.
    """

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.reader(file)

        headers = next(reader)

    columns = [
        clean_column_name(column)
        for column in headers
    ]

    return columns


def create_table(connection, columns):
    """
    Create PostgreSQL table.

    No commit here.
    Transaction is controlled by main().
    """

    column_sql = ",\n".join(
        f'"{column}" TEXT'
        for column in columns
    )

    sql = f"""
        DROP TABLE IF EXISTS {TABLE_NAME};

        CREATE TABLE {TABLE_NAME} (
            id BIGSERIAL PRIMARY KEY,
            {column_sql}
        );
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)

    print(f"Table '{TABLE_NAME}' created.")


def import_csv(connection, columns):
    """
    Use PostgreSQL COPY for fast bulk CSV import.

    No commit here.
    Transaction is controlled by main().
    """

    column_list = ", ".join(
        f'"{column}"'
        for column in columns
    )

    copy_sql = f"""
        COPY {TABLE_NAME} ({column_list})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            NULL ''
        )
    """

    with connection.cursor() as cursor:

        with open(
            CSV_FILE,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            with cursor.copy(copy_sql) as copy:

                while data := file.read(1024 * 1024):
                    copy.write(data)

    print("CSV imported successfully.")


def show_count(connection):
    """
    Verify imported rows.
    """

    with connection.cursor() as cursor:

        cursor.execute(
            f"SELECT COUNT(*) FROM {TABLE_NAME}"
        )

        count = cursor.fetchone()[0]

    print(f"Rows imported: {count}")


def main():

    print("=" * 60)
    print("CSV → PostgreSQL Import")
    print("=" * 60)

    print(f"CSV file: {CSV_FILE}")

    try:

        # Read CSV columns
        columns = get_columns()

        print("\nCSV columns:")

        for column in columns:
            print(f"  - {column}")

        print(f"\nTotal columns: {len(columns)}")

        # Connect to PostgreSQL
        connection = get_connection()

        try:

            # Start transaction automatically when SQL executes
            create_table(connection, columns)

            print("\nImporting CSV...")

            import_csv(connection, columns)

            print("\nVerifying import...")

            show_count(connection)

            # Save everything
            connection.commit()

            print("\nTransaction committed successfully.")
            print("Import completed successfully.")

        except Exception as e:

            # Undo all database changes
            connection.rollback()

            print("\nImport failed.")
            print(f"Error: {e}")
            print("Transaction rolled back.")

        finally:

            connection.close()

    except Exception as e:

        # Handles errors such as:
        # - CSV file not found
        # - CSV header error
        # - Database connection failure

        print("\nApplication failed.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

