from app.database.postgres import get_connection


def main():
    print("AI container started.")

    try:
        connection = get_connection()

        print("PostgreSQL connection successful!")

        connection.close()

    except Exception as error:
        print("PostgreSQL connection failed:")
        print(error)


if __name__ == "__main__":
    main()