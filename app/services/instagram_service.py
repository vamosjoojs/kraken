from app.integrations.instagram_integration import InstagramIntegration


class InstagramServices:
    @staticmethod
    def post_clip(caption, video_path) -> bool:
        instagram_integration = InstagramIntegration(video_path=video_path, caption=caption)
        posted = instagram_integration.post_video()
        return posted
