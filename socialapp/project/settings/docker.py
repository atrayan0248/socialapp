from __future__ import annotations

if IN_DOCKER:  # type: ignore # noqa: F821
    print('Running in docker mode ...')
    assert MIDDLEWARE[:1] == [  # noqa: F821
        'django.middleware.security.SecurityMiddleware',
    ]
