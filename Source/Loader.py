import numpy as np
import pickle as cPickle
import os
import random
from scipy import misc
from PIL import Image
import Resizer
import PIL
#def images()

scale = 0.3

for filename in next(os.walk('Data'))[1]:

    for fname in os.listdir('Data' + '/' + filename):

        img = Image.open('Data' + '/' + filename + '/' + fname)
        height, width = img.size
        img.thumbnail((height*scale, width*scale))
        img.save('Resized'+'Data' + '/' + filename + '/' + fname)


def pickle(path='ResizedData', max_size=100, file = 'pickle', split = 0.6):

    loaded_images = []
    label_vectors = []
    file = file
    i = 0

    for filename in next(os.walk(path))[1]:

        for fname in os.listdir(path + '/' + filename):



            label_vectors.append(label_vector(fname))
            image = Image.open(path + '/' + filename + '/' + fname)
            y_leeway1, x_leeway1 = np.floor_divide(np.subtract(max_size, image.size), 2)
            y_leeway = max_size-image.size[0] - y_leeway1
            x_leeway = max_size-image.size[1] - x_leeway1
            image_array = np.asarray(image)

            height, width = image.size
            zeros = np.zeros([max_size, max_size, 3])
            #zeros = np.zeros([height, width, 3])


            if np.max(image.size) > max_size:
                print('Picture: ' + fname + ' is too large')
                continue
            zeros = np.pad(image_array, ((x_leeway, x_leeway1), (y_leeway, y_leeway1), (0,0)), 'constant')

            """
            img = Image.fromarray(zeros, 'RGB')
            img.save('tis.png')
            img.show()
            """
            #zeros[0:width, 0:height, 0:3] = image_array
            print(zeros.shape)
            """
            img = Image.fromarray(zeros, 'RGB')
            img.save('anus.png')
            img.show()
            """

            loaded_images.append(zeros)
            

            image.close()


    #loaded_imagesxd = np.array(loaded_images)
    mean = np.mean(loaded_images)
    print('mean', mean)
    #img = Image.fromarray(loaded_images[0], 'RGB')
    #img.save('pis.png')
   # img.show()
    normalized_images = np.array(loaded_images)


    img = Image.fromarray(normalized_images[0], 'RGB')
    img.save('pis.png')
    img.show()
    print('normalized')
    Y_norm = np.array(label_vectors)

    ndata = len(normalized_images)
    permutation = list(np.random.permutation(ndata))

    X_shuffled = normalized_images[permutation]

    #random.shuffle(normalized_images)
    #X_shuffled = normalized_images.reshape(ndata,max_size,max_size,3)
    print(X_shuffled.shape)
    Y_shuffled = Y_norm[permutation]
    ntrain = int(split * 100 * ndata // 100)
    X_train = X_shuffled[0:ntrain, :]
    Y_train = Y_shuffled[0:ntrain, :]
    X_test = X_shuffled[ntrain:ndata, :]
    Y_test = Y_shuffled[ntrain:ndata, :]


    with open('Pickles/' + file + '.pkl' , 'wb') as fp:
        for XY in [X_train, Y_train, X_test, Y_test]:
            cPickle.dump(XY, fp)
    return


def label_vector(fname):
    label_vector = np.zeros(len(classes))
    for i in range(len(classes)):
        if fname.lower().startswith(classes[i].lower()):
            label_vector[i] = 1
            break



    return label_vector



def unpickle(filename):

    with open(filename, 'rb') as fp:
        X_train = cPickle.load(fp)
        Y_train = cPickle.load(fp)
        X_test = cPickle.load(fp)
        Y_test = cPickle.load(fp)

    return X_train, Y_train, X_test, Y_test




def categories(path):
    types = os.listdir(path)
    print(len(types))
    categories = []
    j = 1
    for i in range(len(types)):
        if i == 0:
            categories.append(types[0])
        else:
            if not types[i].lower().startswith(categories[i - j].lower()):
                categories.append(types[i].split(';', 1)[0])
            else:
                j += 1

    return categories


classes = categories('Data')
pickle()
