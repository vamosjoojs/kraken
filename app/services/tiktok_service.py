from app.config.logger import Logger
from app.integrations.tiktok_integration import TiktokIntegration

logging = Logger.get_logger("Tiktok")


class TiktokServices:
    @staticmethod
    def post_clip(caption, video_path) -> bool:
        logging.info(f'video path {video_path}')
        tiktok_integration = TiktokIntegration(video_path=video_path, caption=caption)
        logging.info('Começando integração com o tiktik')
        status_code = tiktok_integration.post_media()
        logging.info(status_code)
        if status_code != 200:
            return True
        return False
