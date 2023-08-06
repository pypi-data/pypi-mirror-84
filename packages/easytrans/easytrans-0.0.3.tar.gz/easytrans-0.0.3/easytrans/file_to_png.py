import os
import fitz

from easytrans.file_to_pdf import DocToPdf

SUCCESS_STATUS = 0
FAILURE_STATUS = 1


class DocToPng(object):

    @staticmethod
    def single_doc_to_png(doc_path, libreoffice_version=7.0, img_dir=None, img_name=None, zoom_x=8, zoom_y=8,
                          rotation_angle=0):
        status, result = DocToPdf.single_doc_to_pdf(doc_path, pdf_dir="/tmp/", pdf_name=None,
                                                      libreoffice_version=libreoffice_version)
        if status != SUCCESS_STATUS:
            return FAILURE_STATUS, result

        return PdfToPng.pdf_to_img(result, img_dir, img_name, zoom_x, zoom_y, rotation_angle)

    @staticmethod
    def multiple_doc_to_png_by_file_dir(doc_dir="", libreoffice_version=7.0, img_dir=None, img_name=None, zoom_x=8,
                                        zoom_y=8, rotation_angle=0):
        try:
            status, result = DocToPdf.multiple_doc_to_pdf_by_file_dir(doc_dir, pdf_dir="/tmp/", pdf_name=None,
                                                                        libreoffice_version=libreoffice_version)

            if status != SUCCESS_STATUS:
                return status, result

            img_list = []
            for pdf_path in result:
                status, result = PdfToPng.pdf_to_img(pdf_path, img_dir, img_name, zoom_x, zoom_y, rotation_angle)
                if status != SUCCESS_STATUS:
                    return status, result
                else:
                    img_list.append(result)

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, img_list

    @staticmethod
    def multiple_doc_to_png_by_file_list(doc_path_list=[], libreoffice_version=7.0, img_dir=None, img_name=None,
                                         zoom_x=8, zoom_y=8, rotation_angle=0):
        try:
            status, result = DocToPdf.multiple_doc_to_pdf_by_file_list(doc_path_list, pdf_dir="/tmp/", pdf_name=None,
                                                                         libreoffice_version=libreoffice_version)

            if status != SUCCESS_STATUS:
                return status, result

            img_list = []
            for pdf_path in result:
                status, result = PdfToPng.pdf_to_img(pdf_path, img_dir, img_name, zoom_x, zoom_y, rotation_angle)
                if status != SUCCESS_STATUS:
                    return status, result
                else:
                    img_list.append(result)

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, img_list


class PdfToPng(object):

    @staticmethod
    def pdf_to_img(pdf_path, img_dir=None, img_name=None, zoom_x=8, zoom_y=8, rotation_angle=0):
        try:

            if not isinstance(pdf_path, str) or os.path.isfile(pdf_path):
                return FAILURE_STATUS, "'{0}' is not a directory!".format(pdf_path)

            pdf = fitz.open(pdf_path)

            if not img_name:
                img_name = os.path.splitext(pdf_path)[0]

            if not img_dir:
                img_dir = os.path.dirname(pdf_path)

            img_list = []
            pg_count = pdf.pageCount

            for pg in range(0, pg_count):
                page = pdf[pg]
                trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
                pm = page.getPixmap(matrix=trans, alpha=False)
                if pg_count == 1:
                    img_path = os.path.join(img_dir, "{0}.png".format(img_name))
                else:
                    img_path = os.path.join(img_dir, "{0}{1}.png".format(img_name, str(pg)))
                pm.writePNG(img_path)
                img_list.append(img_path)

            pdf.close()

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, img_list
