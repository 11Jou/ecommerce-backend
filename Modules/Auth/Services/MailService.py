from abc import ABC, abstractmethod

from fastapi import Depends

from Core.settings import (
    get_domain,
    get_gmail_password,
    get_gmail_port,
    get_gmail_server,
    get_gmail_user,
)
from Modules.Auth.Models import User
from Modules.Auth.Services.AuthService import AuthService, get_auth_service
from Tasks.SendMail import send_mail as send_mail_task


class IMailService(ABC):

    @abstractmethod
    async def build_mail_body(self, user: User) -> str:
        pass

    @abstractmethod
    async def send_mail(self, user: User) -> None:
        pass


class BaseMailService(IMailService):
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.gmail_user = get_gmail_user()
        self.gmail_password = get_gmail_password()
        self.gmail_port = get_gmail_port()
        self.gmail_server = get_gmail_server()
        self.domain = get_domain()


class ActivationMailService(BaseMailService):


    async def build_mail_body(self, user: User) -> str:
        activation_token = await self.auth_service.create_activation_token(user)
        token = activation_token.token
        return f"Click the link below to activate your account: {self.domain}/auth/activate?token={token}"

    async def send_mail(self, user: User) -> None:
        mail = await self.build_mail_body(user)
        mail_config = {
            "smtp_user": self.gmail_user,
            "smtp_password": self.gmail_password,
            "smtp_server": self.gmail_server,
            "smtp_port": self.gmail_port,
        }
        send_mail_task.delay(
            recipient=user.email,
            body=mail,
            mail_config=mail_config,
            subject="Activate your account",
        )


class ResetPasswordMailService(BaseMailService):

    async def build_mail_body(self, user: User) -> str:
        pass

    async def send_mail(self, user: User) -> None:
        pass




def get_activation_mail_service(auth_service: AuthService = Depends(get_auth_service)) -> IMailService:
    return ActivationMailService(auth_service)


def get_reset_password_mail_service(auth_service: AuthService = Depends(get_auth_service)) -> IMailService:
    return ResetPasswordMailService(auth_service)
