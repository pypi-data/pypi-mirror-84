import tempfile
from anews.dao import msn
from anews.dao import sound
from anews.dao import create_msn_news
from anews.common import utils
from gbackup import *
class anews():
    def __init__(self):
        self.root_dir = tempfile.TemporaryDirectory()

    def create_msn_news(self,url, title, font_url, logo_url, drive_email, background_url, langCode, langName):
        font_path = utils.cache_file(font_url)
        logo_path = utils.cache_file(logo_url)
        background_path = utils.cache_file(background_url)
        final_vid, final_thumnail = create_msn_news(url, title, self.root_dir.name, font_path, logo_path,
                                                   background_path, langCode, langName)
        video_drive_id = utils.upload_file(drive_email, final_vid)
        thumb_drive_id = utils.upload_file(drive_email, final_thumnail)
        return video_drive_id, thumb_drive_id
    def close(self):
        self.root_dir.cleanup()