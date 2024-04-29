from src.engine.services.font_services import FontsService
from src.engine.services.images_services import ImagesServices
from src.engine.services.sounds_services import SoundsServices


class ServiceLocator:
    images_service = ImagesServices()
    sounds_service = SoundsServices()
    fonts_service = FontsService()
