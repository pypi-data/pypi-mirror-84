# encoding: utf-8


from datetime import datetime, timezone
import os
import shutil

import click

from img2epub import functions as func


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "__init__.py")) as f:
    exec(f.read(), about)
VERSION = about["__version__"]


def main():
    cmd(obj={})


@click.group()
@click.pass_context
@click.version_option(version=VERSION, message="v%(version)s")
def cmd(ctx):
    pass


@cmd.command(help="Build EPUB book.")
@click.pass_context
@click.option("--title", type=str, help="Specify book title.")
@click.option("--output", type=str, metavar="FILENAME", help="Specify filename output to.")
@click.option("--keep", is_flag=True, help="Keep temporary directory.")
@click.argument("src_dir")
def build(ctx, title, output, keep, src_dir):
    now = datetime.now(timezone.utc)
    tmp_dir_name = "tmp.epub.{time}".format(time=now.strftime("%Y%m%d%H%M%S"))

    func.make_dirs(tmp_dir_name)
    images = func.copy_images(src_dir, tmp_dir_name)
    images = [s.replace("\\","/") for s in sorted(images)]
    func.gen_mimetype(tmp_dir_name)
    func.copy_container(tmp_dir_name)
    if not title:
        title = src_dir
    book_opf_context = {
        "title": title,
        "time": now.isoformat(),
        "images": images
    }
    func.gen_book_opf(tmp_dir_name, book_opf_context)
    func.copy_nav(tmp_dir_name)
    func.gen_chap1_xhtml(tmp_dir_name, book_opf_context)
    func.zip_epub(tmp_dir_name, func.build_epub_filename(output, title))

    if not keep:
        shutil.rmtree(tmp_dir_name)


@cmd.command(help="Remove any temporary directories.")
@click.pass_context
def clean(ctx):
    dirs = [f for f in os.listdir(".") if os.path.isdir(f)]
    tmp_dirs = [d for d in dirs if d.startswith("tmp.epub.")]
    for tmp_dir in tmp_dirs:
        shutil.rmtree(tmp_dir)



if __name__ == "__main__":
    main()
