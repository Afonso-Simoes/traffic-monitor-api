from django.db import migrations

def create_initial_users(apps, schema_editor):
    from django.contrib.auth.models import User

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
        print("Superutilizador 'admin' criado.")
    else:
        print("Superutilizador 'admin' já existe.")

    if not User.objects.filter(username='traffic_user').exists():
        User.objects.create_user(
            username='traffic_user',
            email='user@example.com',
            password='password123'
        )
        print("Utilizador 'traffic_user' criado.")
    else:
        print("Utilizador 'traffic_user' já existe.")

class Migration(migrations.Migration):

    dependencies = [
        ('traffic_data_app', '0002_alter_roadsegment_id_alter_trafficreading_id'),
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]