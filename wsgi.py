from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
else:
    application = app    # für WSGI-Server wie Gunicorn oder uWSGI 