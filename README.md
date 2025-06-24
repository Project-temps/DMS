# DMS

DMS (Data Management System) combines Django with Dash to provide interactive dashboards and APIs for handling data ingestion, processing and visualization.

## Setup

1. Clone the repository and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (for development add them to `.env` or your shell profile):
   ```bash
   export DJANGO_SECRET_KEY=your_secret_key
   export DJANGO_DEBUG=True
   ```
   The application uses SQLite by default, but you can adjust database settings in `myproject/settings.py`.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

After starting the server, visit `http://127.0.0.1:8000` to access the web interface and dashboards. Log in with the superuser credentials to manage data and users.

## License

This project is distributed under the [MIT License](LICENSE). Usage, distribution or modification of the software requires explicit permission from the authors. See the license file for the complete terms.

Third-party assets are included under their respective licenses:

- Icons in `ui/static/admin/img` originate from the Font Awesome project and are covered by both the MIT License and the SIL Open Font License. Refer to [`ui/static/admin/img/README.txt`](ui/static/admin/img/README.txt) and [`ui/static/admin/img/LICENSE`](ui/static/admin/img/LICENSE) for details.
- HTML templates in `ui/templates/sneat_html` are based on ThemeSelection's Sneat Bootstrap template and require a valid license from ThemeSelection, as noted in the comments within those files (e.g. `ui/templates/sneat_html/ui-footer.html`).
