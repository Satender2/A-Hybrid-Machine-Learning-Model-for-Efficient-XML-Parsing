# 1. Ensure virtual environment is activated
xml_venv\Scripts\activate

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Create superuser (Admin)
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123 (or your choice)
# When prompted for user_type, open Django shell and update manually

# 4. Generate training dataset
python datasets/generate_dataset.py

# 5. Populate parsers
python scripts/populate_parsers.py

# 6. Train ML models
python scripts/train_models.py

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Update admin user type in Django shell
python manage.py shell
from accounts.models import User
admin = User.objects.get(username='admin')
admin.user_type = 'admin'
admin.save()
exit()

# 9. Run development server
python manage.py runserver

