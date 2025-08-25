from aiogram import Router
from app.routers import (
    start,
    quote,
    portfolio,
    reviews,
    heal,
    contact,
    about,
    admin,
    sketches,
)

# Create a main router that includes all sub-routers
main_router = Router()
main_router.include_router(start.router)
main_router.include_router(quote.router)
main_router.include_router(portfolio.router)
main_router.include_router(reviews.router)
main_router.include_router(heal.router)
main_router.include_router(contact.router)
main_router.include_router(about.router)
main_router.include_router(admin.router)
main_router.include_router(sketches.router)
