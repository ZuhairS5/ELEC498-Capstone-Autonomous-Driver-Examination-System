import csv
from nuimages import NuImages
import argparse

cam_back_left_token = '972a846916414f828b9d2434e465e150'
cam_back_right_token = '9a1de644815e46d1bb8faa1837f8a88b'
car_token = 'fd69059b62a3469fbaef25340c0eab7f'


# returns list of all camera tokens matching desired type specified in camera_tokens



def get_cameras(camera_tokens, cam_table):
    cameras = []
    for token in camera_tokens:
        camera = [entry['token'] for entry in cam_table if entry['sensor_token'] == token]
        cameras += camera
    return cameras


#given a camera token retrieve all samples from that camera
def get_camera_samples(camera, sample_table):
    samples = [entry['token']
               for entry in sample_table
               if (entry['calibrated_sensor_token'] == camera and entry['is_key_frame'])]
    return samples


def get_sample_annotations(sample, annotation_table):
    annotations = []
    for annotation in annotation_table:
        #if checked annotation is not from the desired camera
        if annotation['sample_data_token'] != sample:
            continue
        annotations.append(annotation['token'])
    return annotations


def select_category_annotations(annotations, category_token, nuim):
    filtered_annotations = [annotation for annotation in annotations
                            if nuim.get('object_ann', annotation)['category_token'] == category_token]
    return filtered_annotations

def generate_sample_label(annotations):
    return len(annotations) > 0


def write_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV DictWriter object with the fieldnames taken from the keys of the first dictionary
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row
        writer.writeheader()

        # Write all dictionaries as rows in the CSV file
        writer.writerows(data)

def get_nuim_tables(version, root):
    print(f"creating nuim version:{version} from root:{root}")
    nuim = NuImages(dataroot=root, version=version, verbose=True, lazy=True)
    cam_table = nuim.calibrated_sensor
    sample_table = nuim.sample_data
    annotations_table = nuim.object_ann
    return nuim, cam_table, sample_table, annotations_table

def generate_dataset_file(version, root):
    #Load needed tables for nuim
    nuim, cam_table, sample_table, annotations_table = get_nuim_tables(version, root)
    # Gather all back left and back right cameras from dataset
    cameras = get_cameras([cam_back_left_token, cam_back_right_token], cam_table)

    # from each camera, collect their image frames
    samples = []
    for camera in cameras:
        samples += get_camera_samples(camera, sample_table)

    #generate annotations_list
    annotations = [get_sample_annotations(sample, annotations_table) for sample in samples]
    filtered_annotations = [select_category_annotations(sample_annotations, car_token, nuim)
                            for sample_annotations in annotations]

    #create data objects to be read by loader
    data_objects = []
    for sample, sample_annotations in zip(samples, filtered_annotations):
        annotation_bboxes = [nuim.get('object_ann', annotation)['bbox'] for annotation in sample_annotations]
        sample_object = {'filename': nuim.get('sample_data', sample)['filename'],
                         'annotations': annotation_bboxes,
                         'label': generate_sample_label(annotation_bboxes)
                         }
        data_objects.append(sample_object)

    #write file
    write_csv(data_objects, version + 'dataset.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Dataset Creator',
        description='Selects desired nuimage images and saves to csv')
    parser.add_argument('-v', type=str, default='v1.0-mini', help='Nuimages version to search, default is v1.0-mini')
    parser.add_argument('-p', type=str, default='../data/sets/nuimages', help='path to nuimages, default is ../data/sets/nuimages')
    arguments = parser.parse_args()
    generate_dataset_file(arguments.v,arguments.p)