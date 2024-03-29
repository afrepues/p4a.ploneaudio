from p4a.ploneaudio import sitesetup
from p4a.z2utils import utils as z2utils

def install(portal):
    sitesetup.setup_portal(portal)

def uninstall(portal, reinstall):
    z2utils.persist_five_components(portal, 'p4a.ploneaudio')
    if not reinstall:
        sitesetup.unsetup_portal(portal)
