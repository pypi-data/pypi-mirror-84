import os
import gzip
import shutil
import glob
import datetime


# other options are zlib and bz2.
def unzip_file(in_file: str, out_file: str):
    with gzip.open(in_file, 'rb') as f_in, open(out_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def zip_file(in_file: str, out_file: str):
    with open(in_file, 'rb') as f_in, gzip.open(out_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


# file scanners
def latest_file_in(folder: str, pattern='*'):
    files = glob.glob(folder + '/' + pattern)
    latest = max(files, key=os.path.getmtime)  # we use modify time as marker
    return latest


def latest_folder_in(folder: str, pattern='*/'):
    files = glob.glob(folder + '/' + pattern)
    latest = max(files, key=os.path.getctime)  # we use creation time as marker
    return latest


def find_latest_file(target_dir, file_pattern, before_time=datetime.datetime.now()):
    """
    scan the target directory for files with the given pattern, return the
    latest file with timestamp before the given upper bound. file_pattern
    follows unix pattern, before_time is of type datetime
    """
    ret = None

    t_dir = target_dir if target_dir.endswith('/') else target_dir + '/'
    for f in glob.glob(t_dir + file_pattern):
        stats = os.stat(f)  # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
        mtime = datetime.datetime.fromtimestamp(stats[8])
        if mtime > before_time:
            continue
        else:
            if not ret:
                ret = (mtime, f)
            else:
                if ret[0] < mtime:
                    ret = (mtime, f)

    if not ret:
        return None
    else:
        return ret[1]


def find_earliest_file(target_dir, file_pattern,
                       after_time=datetime.datetime.combine(datetime.date.today(), datetime.time())):
    """
    scan the target directory for files with the given pattern, return the
    earliest file with timestamp after the given lower bound. The default of
    the after_time is the beginning of the day. file_pattern follows unix
    pattern, before_time is of type datetime
    """
    ret = None

    t_dir = target_dir if target_dir.endswith('/') else target_dir + '/'
    for f in glob.glob(t_dir + file_pattern):
        stats = os.stat(f)  # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
        mtime = datetime.datetime.fromtimestamp(stats[8])
        if mtime < after_time:
            continue
        else:
            if not ret:
                ret = (mtime, f)
            else:
                if ret[0] > mtime:
                    ret = (mtime, f)

    if not ret:
        return None
    else:
        return ret[1]
