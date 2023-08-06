from os import listdir,path
from mrcfile import mmap as mrcfile_mmap        #it is not in the setup.py because it is already installed by cryolo
import numpy as np
from cryoloBM import MyRectangle
from cryolo import imagereader

def get_all_loaded_filesnames(root):
    """
    get the list of the loaded file
    :param root: QtG.QTreeWidget obj
    :return: list of filenames
    """
    child_count = root.childCount()
    filenames = []
    for i in range(child_count):
        item = root.child(i)
        filename = path.splitext(item.text(0))[0]
        filenames.append(filename)
    return filenames

def resize_box(rect, new_size):
    """
    resize a 'matplotlib.patches.Rectangle' obj
    :param rect: a 'matplotlib.patches.Rectangle' obj
    :param new_size: new width and height
    :return: None
    """
    if rect.get_width() != new_size or rect.get_height() != new_size:
        height_diff = new_size - rect.get_height()
        width_diff = new_size - rect.get_width()
        newy = rect.get_y() - height_diff / 2
        newx = rect.get_x() - width_diff / 2
        rect.set_height(new_size)
        rect.set_width(new_size)
        rect.set_xy((newx, newy))


def get_only_files(dir_path,wildcard,is_list_tomo):
    """
    generate list of files in 'dir_path' path
    :param dir_path: path to the folder
    :param wildcard: using wildcard
    :param is_list_tomo: True if folder of 3D tomo
    :return: list of valid files in 'dir_path'
    """
    onlyfiles = [
        f
        for f in sorted(listdir(dir_path))
        if path.isfile(path.join(dir_path, f))
    ]

    if wildcard:
        import fnmatch
        onlyfiles = [
            f
            for f in sorted(listdir(dir_path))
            if fnmatch.fnmatch(f, wildcard)
        ]

    if is_list_tomo is False:
        onlyfiles = [
            i
            for i in onlyfiles
            if not i.startswith(".")
               and i.endswith((".jpg", ".jpeg", ".png", ".mrc", ".mrcs", ".tif", ".tiff"))]
    else:
        onlyfiles_all = [i for i in onlyfiles if not i.startswith(".") and i.endswith((".mrc", ".mrcs"))]
        onlyfiles.clear()
        for f in onlyfiles_all:
            with mrcfile_mmap(path.join(dir_path, f), permissive=True, mode="r") as mrc:
                if len(mrc.data.shape) == 3:
                    onlyfiles.append(f)
                mrc.close()

    return onlyfiles


def filter_tuple_is_equal(a,b):
    return a[0]==b[0] and a[1]==b[1] and a[2] == b[2]


def is_helicon_with_particle_coords(path_f):
    with open(path_f) as f:
        first_line = f.readline()
        f.close()
    return "#micrograph" in first_line


def is_eman1_helicion(path_f):
    try:
        box_lines = np.atleast_2d(np.genfromtxt(path_f))
        if len(box_lines) < 2:
            return False
        return (
                len(box_lines[0]) == 5
                and box_lines[0][4] == -1
                and box_lines[1][4] == -2
        )
    except ValueError:
        return False


def getEquidistantRectangles(x_start, y_start, x_end, y_end, width, parts, edgecolor):
    points = zip(
        np.linspace(x_start, x_end, parts + 1, endpoint=False),
        np.linspace(y_start, y_end, parts + 1, endpoint=False),
    )
    new_rectangles = []
    w = width
    h = width

    for point in points:
        rect = MyRectangle.MyRectangle(
            (point[0], point[1]),
            w,
            h,
            linewidth=1,
            edgecolor=edgecolor,
            facecolor="none",
        )
        rect.set_confidence(1)
        new_rectangles.append(rect)
    return new_rectangles


def get_file_type(file_path):
    im_type = None
    if file_path.endswith(("jpg", "jpeg", "png")):
        im_type = 0
    if file_path.endswith(("tif", "tiff")):
        im_type = 1
    if file_path.endswith(("mrc", "mrcs","rec")):
        im_type = 2
    return im_type


def read_image(file_path, use_mmap=False):
    im_type = get_file_type(file_path)

    img = imagereader.image_read(file_path, use_mmap=use_mmap)
    img = normalize_and_flip(img, im_type)
    return img

def normalize_and_flip(img, file_type):
    if file_type == 0:
        # JPG
        img = np.flip(img, 0)
    if file_type == 1 or file_type == 2:
        # tif /mrc
        if not np.issubdtype(img.dtype, np.float32):
            img = img.astype(np.float32)
        if len(img.shape) == 3:
            img = np.flip(img, 1)
        else:
            img = np.flip(img, 0)
        mean = np.mean(img)
        sd = np.std(img)
        img = (img - mean) / sd
        img[img > 3] = 3
        img[img < -3] = -3
    return img


def get_number_visible_boxes( rectangles):
    i = 0
    for box in rectangles:
        if box.is_figure_set():
            i = i + 1
    return i

def get_corresponding_box(x, y, rectangles, current_conf_thresh, box_size, get_low=False):
    a = np.array([x, y])

    for box in rectangles:
        b = np.array(box.getRect().xy)
        dist = np.linalg.norm(a - b)
        if get_low:
            if dist < box_size / 2 and box.confidence < current_conf_thresh:
                return box
        else:
            if dist < box_size / 2 and box.confidence > current_conf_thresh:
                return box
    return None

def check_if_should_be_visible( box, current_conf_thresh, upper_size_thresh, lower_size_thresh):
    return box.confidence > current_conf_thresh and upper_size_thresh >= box.est_size >= lower_size_thresh
