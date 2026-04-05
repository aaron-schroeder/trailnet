from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Delete all objects for a given model (by name)'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model name (e.g. Line)')
        parser.add_argument(
            '--app',
            type=str,
            help='App label (optional, but recommended if model names collide)',
        )

    def handle(self, *args, **options):
        model_name = options['model']
        app_label = options.get('app')
        try:
            if app_label:
                model = apps.get_model(app_label, model_name)
            else:
                matches = [
                    m for m in apps.get_models()
                    if m.__name__.lower() == model_name.lower()
                ]
                if not matches:
                    raise LookupError(f'No model found with name "{model_name}"')
                if len(matches) > 1:
                    raise CommandError(
                        f'Multiple models found named "{model_name}". '
                        f'Specify --app. Options: {[m._meta.label for m in matches]}'
                    )
                model = matches[0]
        except LookupError as e:
            raise CommandError(str(e))
        count, _ = model.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                f'Deleted {count} objects from {model._meta.label}'
            )
        )
