from src.schemas import UpdateUserProfileModel
from typing import Optional
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user_by_username(username: str, db: AsyncSession) -> User:
    """
    Retrieves a user by their email from the database.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the specified email, or None if not found.
    :rtype: User | None
    """
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalars().first()

async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Retrieves a user by their email from the database.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the specified email, or None if not found.
    :rtype: User | None
    """
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalars().first()

async def create_user(body: UserModel, db: AsyncSession) -> User:
    """
    Creates a new user in the database.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
    Updates the refresh token for a user in the database.

    :param user: The user whose token should be updated.
    :type user: User
    :param token: The new refresh token or None to remove the token.
    :type token: str | None
    :param db: The database session.
    :type db: AsyncSession
    :return: None
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Marks a user's email as confirmed in the database.

    :param email: The email address of the user to mark as confirmed.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
    Updates the avatar URL for a user in the database.

    :param email: The email address of the user to update.
    :type email: str
    :param url: The new avatar URL for the user.
    :type url: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the updated avatar URL.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_user_profile(email: str, profile_data: UpdateUserProfileModel, db: AsyncSession) -> User:
    """
    Updates the profile information for a user in the database.

    :param email: The email address of the user to update.
    :type email: str
    :param profile_data: The updated profile information.
    :type profile_data: UpdateUserProfileModel
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the updated profile information.
    :rtype: User
    """
    user = await get_user_by_email(email, db)

    if profile_data.avatar:
        user.avatar = profile_data.avatar

    if profile_data.username:
        user.username = profile_data.username

    if profile_data.email:
        user.email = profile_data.email

    db.commit()
    db.refresh(user)

    return user
