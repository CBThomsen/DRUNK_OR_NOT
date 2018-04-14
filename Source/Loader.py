import numpy as np
import pickle as cPickle
import os
from scipy import misc
from PIL import Image
import Resizer

#def images()

    #img = Image.open("lena.png")
    #pix = np.array(img)
    #changed_img = Resizer.shrink(pix, 512, 40)  # Change - Issue #1
    #resized = Image.fromarray(changed_img, 'RGB')
    #resized.save("lena_resize.png")


def pickle(path='Data', max_size=800, file = 'pickle', split = 0.6):

    loaded_images = []
    label_vectors = []
    file = file
    i = 0

    for filename in next(os.walk(path))[1]:

        for fname in os.listdir(path + '/' + filename):

            i += 1
            if i > 10:
                break

            label_vectors.append(label_vector(fname))
            image = Image.open(path + '/' + filename + '/' + fname)
            y_leeway, x_leeway = np.floor_divide(np.subtract(max_size, image.size), 2)
            image_array = np.asarray(image)
            zeros = np.zeros([max_size, max_size, 3])

            print(fname)

            if np.max(image.size) > max_size:
                raise ValueError('Picture: ' + fname + ' is too large')
                pass

            zeros[x_leeway:image_array.shape[0]+x_leeway, y_leeway:image_array.shape[1]+y_leeway, :] = image_array

            loaded_images.append(zeros)

    normalized_images = np.floor_divide(loaded_images, np.mean(loaded_images))
    Y_norm = np.array(label_vectors)

    ndata = normalized_images.shape[0]
    permutation = list(np.random.permutation(ndata))
    X_shuffled = normalized_images[permutation, :].reshape(ndata,max_size,max_size,3)
    print(X_shuffled.shape)
    Y_shuffled = Y_norm[permutation, :].reshape((normalized_images.shape[0], Y_norm.shape[1]))
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