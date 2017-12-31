import os
import uuid
import oncoserve.logger
from OncoData.oncodata.dicom_to_png.dicom_to_png import dicom_to_png_dcmtk, dicom_to_png_imagemagick, dicom_to_png_matlab
from PIL import Image

logger = oncoserve.logger.get_logger('oncologger.oncodata', 'errors.log')



NO_CONVERTOR_MSG = 'Converter choice {} not recognized!'
FAIL_CONVERT_MESSAGE = 'Fail to convert dicom {}. Caused Exception {} with args: {}'
SUCCESS_CONV_MESSAGE = 'Succesffuly converted dicom {} into png with args: {}'

def get_converter(args):
    convertor = args.convertor

    if convertor == 'dcmtk':
        return dicom_to_png_dcmtk
    elif convertor == 'imagemagick':
        return dicom_to_png_imagemagick
    elif convertor == 'matlab':
        dicom_to_png_matlab
    else:
        err_msg = NO_CONVERTOR_MSG.format(convertor)
        logger.error(err_msg)
        raise Exception(err_msg)


def remove_if_exist(path):
    if os.path.exists(path):
            os.remove(path)

def get_pngs(dicoms, args):
    '''
        Converts dicoms into PIL images through use of OncoData.
        This function makes and deletes temporary files to interface with OncoData depdencies.

        params:
        - dicoms: List of dicom files, each in bytes
        - args: Instance of OncoData args. Specify what kind of convertor to use. i.e dcmtk, imagemagic or matlab.

        returns:
        - images: list of PIL image objects

    '''
    convertor = get_converter(args)
    images = []
    for indx, dicom in enumerate(dicoms):
        dicom_path = os.path.join(args.temp_img_dir, uuid.uuid4())
        png_path = os.path.join(args.temp_img_dir, uuid.uuid4())

        remove_if_exist(dicom_path)
        remove_if_exist(png_path)

        f = open(dicom_path, 'wb')
        f.write(dicom)

        convertor(dicom_path, png_path, skip_existing=False)

        try:
            images.append(Image.open(png_path))
            os.remove(png_path)
            logger.info(SUCCESS_CONV_MESSAGE.format(indx, args))
        except Exception, e:
            err_msg = FAIL_CONVERT_MESSAGE.format(indx, e, args)
            logger.error(err_msg)
            raise Exception(e)

    return images


