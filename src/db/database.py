"""Database class with all-in-one features."""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from src.configuration import conf

from .repositories import (
    UserRepo, SellerRepo, 
    ClientRepo, ProductRepo, 
    CashbackRepo, AllowedRepo,
    PurchaseRepo, FeedbackRepo,
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    user: UserRepo
    seller: SellerRepo
    client: ClientRepo
    product: ProductRepo
    cashback: CashbackRepo
    allowed: AllowedRepo
    purchase: PurchaseRepo
    feedback: FeedbackRepo

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        seller: SellerRepo = None,
        client: ClientRepo = None,
        product: ProductRepo = None,
        cashback: CashbackRepo = None,
        allowed: AllowedRepo = None,
        purchase: PurchaseRepo = None,
        feedback: FeedbackRepo = None,
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.seller = seller or SellerRepo(session=session)
        self.client = client or ClientRepo(session=session)
        self.product = product or ProductRepo(session=session)
        self.cashback = cashback or CashbackRepo(session=session)
        self.allowed = allowed or AllowedRepo(session=session)
        self.purchase = purchase or PurchaseRepo(session=session)
        self.feedback = feedback or FeedbackRepo(session=session)
