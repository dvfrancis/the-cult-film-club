from django.db import migrations


def create_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'thecultfilmclub.up.railway.app',
            'name': 'The Cult Film Club',
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_site, migrations.RunPython.noop),
    ]