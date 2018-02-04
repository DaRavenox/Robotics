import xml.etree.ElementTree as ET
import os
import sys
from PIL import Image

import argparse



def crop_image(data, image_folder, target_folder):
    xmlfile = ET.parse(data)
    root = xmlfile.getroot()
    file_name = root[1].text
    xmin = int(root[6][4][0].text)
    ymin = int(root[6][4][1].text)
    xmax = int(root[6][4][2].text)
    ymax = int(root[6][4][3].text)
    image_obj = Image.open(image_folder+'/'+file_name)
    print(image_folder+'/'+file_name)
    cropped_image = image_obj.crop((xmin,ymin,xmax,ymax))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    cropped_image.save(target_folder+'/'+file_name[:-4]+'CROPPED.jpg')


def crop_all(xmlfolder, image_folder, target_folder):
    for file_name in os.listdir(xmlfolder):
        crop_image(xmlfolder+'/'+file_name,image_folder,target_folder)


def crop_dataset(dataset_path, dataset_xmls):
    for folder_name in os.listdir(dataset_path):
        folder_path = dataset_path+'/'+folder_name
        for subfolder_name in os.listdir(folder_path):
            subfolder_path = folder_path+'/'+subfolder_name
            for subsubfolder_name in os.listdir(subfolder_path):
                subsubfolder_path = subfolder_path + '/' + subsubfolder_name
                crop_all(dataset_xmls+'/'+subsubfolder_name+'_'+folder_name+'_'+subfolder_name,
                         subsubfolder_path+'/Kinect',subsubfolder_path+'/cropped_kinect')
                crop_all(dataset_xmls + '/' + subsubfolder_name + '_' + folder_name + '_' + subfolder_name+'_web',
                         subsubfolder_path + '/webcam', subsubfolder_path + '/cropped_web')


def main():
    crop_dataset(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
	parser=argparse.ArgumentParser(
    description='''Cropps all images according to the xmls generated in Imagelabler ''',
    epilog="""Author: Jonas Hongisto""")
	parser.add_argument('String', metavar='Pd', type=int, nargs=1,
                    help='path to directory with the dataset')
	parser.add_argument('String', metavar='Px', type=int, nargs=1,
                    help='path to the directory with the XMLs')
	args=parser.parse_args()
	main()




