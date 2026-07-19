from app.core.env_loader import EnvLoader


class Database:
    """
    Database configuration manager.

    Database credentials are loaded
    from the .env file.
    """


    def __init__(self):

        self.__host = EnvLoader.get(
            "DATABASE_HOST"
        )

        self.__port = EnvLoader.get_int(
            "DATABASE_PORT"
        )

        self.__user = EnvLoader.get(
            "DATABASE_USER"
        )

        self.__password = EnvLoader.get(
            "DATABASE_PASSWORD"
        )

        self.__name = EnvLoader.get(
            "DATABASE_NAME"
        )


        self.__validate()


    def __validate(self):
        """
        Validate required database settings.
        """

        required = {
            "DATABASE_HOST": self.__host,
            "DATABASE_PORT": self.__port,
            "DATABASE_USER": self.__user,
            "DATABASE_PASSWORD": self.__password,
            "DATABASE_NAME": self.__name
        }


        for key, value in required.items():

            if not value:
                raise ValueError(
                    f"{key} is required"
                )


    @property
    def host(self):
        return self.__host


    @property
    def port(self):
        return self.__port


    @property
    def user(self):
        return self.__user


    @property
    def password(self):
        return self.__password


    @property
    def name(self):
        return self.__name


    @property
    def uri(self):
        """
        Generate SQLAlchemy database URI.
        """

        return (
            f"mysql+pymysql://"
            f"{self.user}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.name}"
        )
    