from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("chewapp", "0001_initial")]

    operations = [
        migrations.RunSQL(
            """
            INSERT INTO chewapp_userprofile
                (id, name, is_manager, is_administrator, is_owner, is_staff)
            VALUES
                (1,  'Manager',       true,  false, false, false),
                (2,  'Administrator', false, true,  false, false),
                (3,  'Owner',         false, false, true,  false),
                (4,  'Staff',         false, false, false, true),
                (5,  'Superuser',     true,  true,  true,  true);
            """,
            reverse_sql="""
            DELETE FROM chewapp_userprofile
            WHERE id IN (1, 2, 3, 4, 5);
            """,
        )
    ]
