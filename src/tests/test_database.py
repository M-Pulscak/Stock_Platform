from db.database import Database


def main() -> None:

    with Database() as db:

        print("=" * 60)
        print("Database connection test")
        print("=" * 60)

        print(f"Connected: {db.is_connected}")

        version = db.scalar("SELECT version();")
        print(f"Version: {version}")

        current_time = db.scalar("SELECT NOW();")
        print(f"Server time: {current_time}")

        schemas = db.fetch_all("""
            SELECT schema_name
            FROM information_schema.schemata
            ORDER BY schema_name;
        """)

        print(f"Schemas found: {len(schemas)}")

        for schema in schemas:
            print(f" - {schema['schema_name']}")

        print("=" * 60)
        print("Database OK")
        print("=" * 60)


if __name__ == "__main__":
    main()
