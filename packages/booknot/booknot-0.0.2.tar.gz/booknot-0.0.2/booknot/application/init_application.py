import click
import inquirer

from booknot.booknot_storage.booknot_storage import BooknotStorage

class InitApplication:

    def __init__(self, booknot_storage: BooknotStorage):
        self.booknot_storage = booknot_storage

    def run(self):

        if self.booknot_storage.exists():
            raise click.ClickException('.booknot already exists')

        if not self.booknot_storage.is_sphinx_present():
            questions = [
                inquirer.Confirm('init sphinx',
                                 message='This will create a workspace for sphinx, do you want to continue ?',
                                 default=False),
            ]

            answers = inquirer.prompt(questions)
            if answers['init sphinx']:
                questions = [
                    inquirer.Text('project',
                                     message='What the name of the project of this booknot',
                                     default='Booknot'),
                    inquirer.Text('author',
                                     message='What the name of the author',
                                     default='me'),
                ]

                answers = inquirer.prompt(questions)
                self.booknot_storage.create_sphinx(answers['project'], answers['author'])

                click.echo("to render the documentation, use make html")
                click.echo("to open the render, use open _build/html/index.html")
                self.booknot_storage.init_store()
        else:
            self.booknot_storage.init_store()
            click.echo("you can use : booknot capture https://...")
