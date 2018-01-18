import os
import uuid
import oncoserve.logger
from oncodata.dicom_to_png.dicom_to_png import dicom_to_png_dcmtk, dicom_to_png_imagemagick
from PIL import Image
import pdb


NO_CONVERTOR_MSG = 'OncoData- Converter choice {} not recognized!'
FAIL_CONVERT_MESSAGE = 'OncoData- Fail to convert dicom {}. Caused Exception {} with args: {}'
SUCCESS_CONV_MESSAGE = 'OncoData- Succesffuly converted dicom {} into png with args: {}'

def get_converter(args, logger):
    convertor = args.convertor

    if convertor == 'dcmtk':
        return dicom_to_png_dcmtk
    elif convertor == 'imagemagick':
        return dicom_to_png_imagemagick
    else:
        err_msg = NO_CONVERTOR_MSG.format(convertor)
        logger.error(err_msg)
        raise Exception(err_msg)


def remove_if_exist(path):
    if os.path.exists(path):
            os.remove(path)

def get_pngs(dicoms, args, logger):
    '''
        Converts dicoms into PIL images through use of OncoData.
        This function makes and deletes temporary files to interface with OncoData depdencies.

        params:
        - dicoms: List of dicom files, each in bytes
        - args: Instance of OncoData args. Specify what kind of convertor to use. i.e dcmtk, imagemagic or matlab.

        returns:
        - images: list of PIL image objects

    '''
    convertor = get_converter(args, logger)
    images = []
    for key, dicom in enumerate(dicoms):
        try:
            os.makedirs(args.temp_img_dir)
        except Exception as e:
            pass
        dicom_path = "{}.dcm".format(os.path.join(args.temp_img_dir, str(uuid.uuid4())))
        png_path = "{}.png".format(os.path.join(args.temp_img_dir, str(uuid.uuid4())))

        remove_if_exist(dicom_path)
        remove_if_exist(png_path)

        dicom.save(dicom_path)
        convertor(dicom_path, png_path, skip_existing=False)

        try:
            os.remove(dicom_path)
            images.append(Image.open(png_path))
            os.remove(png_path)
            logger.info(SUCCESS_CONV_MESSAGE.format(key, args.convertor))
        except Exception, e:
            if os.path.exists(dicom_path):
                os.remove(dicom_path)
            err_msg = FAIL_CONVERT_MESSAGE.format(key, e, args.convertor)
            logger.error(err_msg)
            raise Exception(err_msg)

    return images


