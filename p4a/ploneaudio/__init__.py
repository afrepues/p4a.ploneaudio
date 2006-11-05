
def has_ataudio_support():
    try:
        import Products.ATAudio
        return True
    except:
        return False
