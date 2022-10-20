from time import sleep

from app.integrations.graph_api import InstagramGraphIntegration
from app.config.logger import Logger

logging = Logger.get_logger("graph api")


class InstagramServices:
    @staticmethod
    def post_clip(caption, video_path) -> bool:
        logging.info(f'video path {video_path}')
        instagram_integration = InstagramGraphIntegration(video_path=video_path, caption=caption)
        logging.info('Começando integração')
        container_id = instagram_integration.create_container_instagram_graph_api()
        logging.info(f'Container ID: {container_id}')
        while True:
            status_code = instagram_integration.verify_container_id(container_id)
            logging.info(status_code)
            if status_code == "FINISHED":
                instagram_integration.post_media(container_id)
                return True
            if status_code == "ERROR":
                return False
            if status_code == "EXPIRED":
                return False
            if status_code == "IN_PROGRESS":
                sleep(5)
                continue
