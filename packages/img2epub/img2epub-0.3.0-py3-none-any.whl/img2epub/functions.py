# encoding: utf-8


from datetime import datetime, timezone
import glob
import os
import re
import shutil
import subprocess
import uuid

from jinja2 import Template, Environment, FileSystemLoader


data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


def make_dirs(tmp_dir_name):
    os.makedirs(os.path.join(tmp_dir_name, "META-INF"))
    os.makedirs(os.path.join(tmp_dir_name, "EPUB"))


def copy_images(src_dir, tmp_dir_name):
    images_dir = os.path.join(tmp_dir_name, "EPUB/images")
    shutil.copytree(src_dir, images_dir)
    return glob.glob("{dir}/*".format(dir=images_dir))


def gen_mimetype(tmp_dir_name):
    with open(os.path.join(tmp_dir_name, "mimetype"), "w") as f:
        f.write("application/epub+zip")


def copy_container(tmp_dir_name):
    src = os.path.join(data_dir, "container.xml")
    dest = os.path.join(tmp_dir_name, "META-INF/container.xml")
    shutil.copyfile(src, dest)


def gen_book_opf(tmp_dir_name, context):
    env = Environment(loader=FileSystemLoader(data_dir))
    template = env.get_template("book.opf.template")
    context["images"] = [s.replace("{tmp}/EPUB".format(tmp=tmp_dir_name), ".") for s in context["images"]]
    context["cover"] = context["images"][0]
    context["uuid"] = str(uuid.uuid4())
    with open(os.path.join(tmp_dir_name, "EPUB/book.opf"), "w", encoding="utf-8") as f:
        f.write(template.render(context))


def copy_nav(tmp_dir_name):
    src = os.path.join(data_dir, "nav.xhtml")
    dest = os.path.join(tmp_dir_name, "EPUB/nav.xhtml")
    shutil.copyfile(src, dest)


def gen_chap1_xhtml(tmp_dir_name, context):
    env = Environment(loader=FileSystemLoader(data_dir))
    template = env.get_template("chap1.xhtml.template")
    images = [s.replace("{tmp}/EPUB".format(tmp=tmp_dir_name), ".") for s in context["images"]]
    with open(os.path.join(tmp_dir_name, "EPUB/chap1.xhtml"), "w", encoding="utf-8") as f:
        f.write(template.render(images=images, title=context["title"]))


def zip_epub(tmp_dir_name, filename):
    epub_file_name = "../{filename}".format(filename=filename)
    os.chdir(tmp_dir_name)
    subprocess.run(["zip", "-X0", epub_file_name, "mimetype"], stdout=subprocess.DEVNULL)
    subprocess.run(["zip", "-r9", epub_file_name, "*", "-x", "mimetype"], stdout=subprocess.DEVNULL)
    os.chdir("..")


def build_epub_filename(output, title):
    if not output:
        output = title
    return re.sub("\.epub\Z", "", output, flags=re.IGNORECASE) + ".epub"
