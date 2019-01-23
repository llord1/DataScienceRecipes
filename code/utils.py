import tarfile

def list_tar_files(tar_ball):
    """
    `getmembers()` requires scaning the entire file before returning the first value.
    Avoid that by making a looping iterator.
    """

    tar_info = tar_ball.next()
    while tar_info is not None:
        tar_file = tar_ball.extractfile(tar_info)
        if tar_file is not None:
            pass
            yield tar_info, tar_file
        tar_info = tar_ball.next()
    pass