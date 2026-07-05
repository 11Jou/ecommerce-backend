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
from Tasks.SendActivation import send_activation_mail as send_activation_mail_task


class IActivationMailService(ABC):

    @abstractmethod
    async def generate_activation_token(self, user: User) -> str:
        pass

    @abstractmethod
    async def build_activation_mail(self, user: User) -> str:
        pass

    @abstractmethod
    async def send_activation_mail(self, user: User) -> None:
        pass


class GmailActivationMailService(IActivationMailService):

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.gmail_user = get_gmail_user()
        self.gmail_password = get_gmail_password()
        self.gmail_port = get_gmail_port()
        self.gmail_server = get_gmail_server()
        self.domain = get_domain()

    async def generate_activation_token(self, user: User) -> str:
        activation_token = await self.auth_service.create_activation_token(user)
        return activation_token.token

    async def build_activation_mail(self, user: User) -> str:
        token = await self.generate_activation_token(user)
        return f"Click the link below to activate your account: {self.domain}/auth/activate?token={token}"

    async def send_activation_mail(self, user: User) -> None:
        mail = await self.build_activation_mail(user)
        send_activation_mail_task.delay(
            recipient=user.email,
            body=mail,
            smtp_user=self.gmail_user,
            smtp_password=self.gmail_password,
            smtp_server=self.gmail_server,
            smtp_port=self.gmail_port,
        )


def get_activation_mail_service(auth_service: AuthService = Depends(get_auth_service)) -> IActivationMailService:
    return GmailActivationMailService(auth_service)
