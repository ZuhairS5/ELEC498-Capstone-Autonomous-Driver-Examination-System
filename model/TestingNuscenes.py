from nuscenes.nuscenes import NuScenes

# Initialize a 'NuScenes' object
nusc = NuScenes(version='v1.0-mini', dataroot='./data/nuscenes/', verbose=True)

# Print the first record to check if it's loaded correctly
print(nusc.sample[0])

my_sample = nusc.sample[0]
nusc.render_sample_data(my_sample['data']['CAM_FRONT'])

# Get the annotated data
my_annotation_token = my_sample['anns'][0]
my_annotation_data = nusc.get('sample_annotation', my_annotation_token)
print(my_annotation_data)