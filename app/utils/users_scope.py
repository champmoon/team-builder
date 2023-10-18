from app.consts import UsersTypes


class UsersScope:
    users_list = [user_type for user_type in UsersTypes]

    @classmethod
    def all(cls) -> list[UsersTypes]:
        return cls.users_list.copy()

    @classmethod
    def exclude(cls, exclude: UsersTypes | list[UsersTypes]) -> list[UsersTypes]:
        if isinstance(exclude, list):
            return list(set(cls.users_list) - set(exclude))
        return [user_type for user_type in cls.users_list if user_type != exclude]
