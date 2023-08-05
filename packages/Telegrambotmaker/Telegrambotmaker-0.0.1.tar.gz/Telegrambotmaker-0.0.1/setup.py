from setuptools import setup
__project__ = "Telegrambotmaker"
__version__ = "0.0.1"
__description__ = "Telegram API"
__packages__ = ["telegramapi"]
__requires__ = ["requests"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    requires = __requires__
)
