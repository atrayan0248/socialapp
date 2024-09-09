
if IN_DOCKER: #type: ignore
    print("Running in docker mode ...")
    assert MIDDLEWARE[:1] == [
        'django.middleware.security.SecurityMiddleware'
    ]

