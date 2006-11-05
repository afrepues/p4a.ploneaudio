def has_fatsyndication_support():
    try:
        import Products.fatsyndication
    except ImportError, e:
        return False
    return True

def has_ataudio_support():
    try:
        import Products.ATAudio
        return True
    except:
        return False

def has_blobfile_support():
    try:
        import Products.BlobFile
    except ImportError, e:
        return False
    return True
