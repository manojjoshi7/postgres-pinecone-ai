import psycopg

from app.database.postgres import get_connection


TABLE_NAME = "ecommerce_customers"


def get_documents_batch(offset=0, batch_size=100):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = f"""
                SELECT *
                FROM {TABLE_NAME}
                ORDER BY id
                LIMIT %s OFFSET %s
            """

            cursor.execute(
                sql,
                (batch_size, offset)
            )

            rows = cursor.fetchall()

            if not rows:
                return []

            columns = [
                description.name
                for description in cursor.description
            ]
            #print(columns)
            documents = []

            for row in rows:

                data = dict(
                    zip(columns, row)
                )

                text_parts = []

                for key, value in data.items():

                    if key == "id":
                        continue

                    if value is not None and str(value).strip():

                        text_parts.append(
                            f"{key.replace('_', ' ').title()}: {value}"
                        )

                documents.append({
                    "id": str(data["id"]),
                    "text": "\n".join(text_parts),
                    "metadata": data
                })

            return documents

    finally:
        connection.close()