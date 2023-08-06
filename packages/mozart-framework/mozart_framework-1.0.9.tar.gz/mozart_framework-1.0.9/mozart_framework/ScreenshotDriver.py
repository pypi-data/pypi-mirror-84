# =============================================================
# =================     Library Import    =====================
# =============================================================

from PIL import ImageGrab



# =============================================================
# =================        class          =====================
# =============================================================

# Classe Screenshot Responsável pela automatização do de screenshot
class ScreenshotAutomator:


    def take_Snapshot(savePath):

        snapshot = ImageGrab.grab()
        snapshot.save(savePath)

