from database import get_connection


class ContactService:


    def get_contacts(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                phone
            FROM contacts
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return rows


    def add_contact(self, name, phone):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO contacts
            (
                name,
                phone
            )
            VALUES
            (
                ?,
                ?
            )
        """, (name, phone))

        conn.commit()

        conn.close()


    def delete_contact(self, contact_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM contacts
            WHERE id = ?
        """, (contact_id,))

        conn.commit()

        conn.close()