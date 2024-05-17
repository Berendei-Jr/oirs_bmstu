import os
from shutil import copyfile
from translate import translate

VALIDATION_IMAGES_PERCENTAGE = 20
IMAGE_COUNTER = 100/VALIDATION_IMAGES_PERCENTAGE

train_dir = 'train'
validation_dir = 'validation'
os.mkdir(train_dir)
os.mkdir(validation_dir)

for dir in os.listdir('raw-img'):
    animal = translate[dir]
    print('Processing ' + animal)
    animal_train_dir = train_dir + '/' + animal
    animal_val_dir = validation_dir + '/' + animal
    os.mkdir(animal_train_dir)
    os.mkdir(animal_val_dir)
    
    image_count = 0
    for image in os.listdir('raw-img/' + dir):
        if image_count < IMAGE_COUNTER:
            copyfile('raw-img/' + dir + '/' + image, animal_train_dir + '/' + image)
            image_count += 1
        else:
            copyfile('raw-img/' + dir + '/' + image, animal_val_dir + '/' + image)
            image_count = 0
