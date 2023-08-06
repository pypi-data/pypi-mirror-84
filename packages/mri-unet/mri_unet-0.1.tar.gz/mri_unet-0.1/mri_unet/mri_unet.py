#!/usr/bin/env python3

# System dependency imports

from __future__ import print_function

import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# The GPU id to use, usually either "0" or "1"
# os.environ["CUDA_VISIBLE_DEVICES"]="0"
import keras.models as models
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
import pfmisc
import time
np.random.seed(256)
import tensorflow as tf

from keras.models import Model,load_model
from keras.layers import Input, concatenate, Conv3D, MaxPooling3D, Conv3DTranspose, AveragePooling3D, ZeroPadding3D
from keras.optimizers import RMSprop, Adam, SGD
from keras.callbacks import ModelCheckpoint, CSVLogger
from keras import backend as K
from keras.regularizers import l2
from keras.utils import plot_model
K.set_image_data_format('channels_last')
import cv2
import sys
sys.path.append(os.path.dirname(__file__))

#print ("*************TEST FOR GPUs*****************")
#print(tf.test.gpu_device_name())

# import the Chris app superclass
from chrisapp.base import ChrisApp
from data3D import load_train_data, load_test_data, preprocess_squeeze,create_test_data

K.set_image_data_format('channels_last')

project_name = '3D-Dense-Unet'
img_rows = 256
img_cols = 256
img_depth = 16
smooth = 1.

class mri_unet(object):

    """
        mri_unet trains a unet model on mri images
        to do semantic segmentation

    """
    def log(self, *args):
        '''
        get/set the internal pipeline log message object.

        Caller can further manipulate the log object with object-specific
        calls.
        '''
        if len(args):
            self._log = args[0]
        else:
            return self._log

    def name(self, *args):
        '''
        get/set the descriptive name text of this object.
        '''
        if len(args):
            self.__name = args[0]
        else:
            return self.__name

    def description(self, *args):
        '''
        Get / set internal object description.
        '''
        if len(args):
            self.str_desc = args[0]
        else:
            return self.str_desc

    def __init__(self, **kwargs):
        
        self.str_desc                   = ""
        self.__name__                   = "mri_unet"

        self.str_inputDir               = ""
        self.str_outputDir              = ""
        self.str_inputFile              = ""
        self.str_outputFileStem         = ""
        self.str_outputFileType         = "png"
        self._b_image                   = False
        self.str_label                  = "label"
        self._b_normalize               = False
        self.str_lookupTable            = "__val__"
        self.str_skipLabelValueList     = ""
        self.str_filterLabelValueList   = "-1"
        self.str_wholeVolume            = ""
        self.l_skip                     = []
        self.l_filter                   = []
        self.__name__                   = "mri_unet"
        self.df_FSColorLUT              = None
        self.verbosity                  = 1
        self.str_version                = '1.4.42'
        self.dp                         = pfmisc.debug(
                                            verbosity   = self.verbosity,
                                            within      = self.__name__
                                            )

        for key, value in kwargs.items():
            if key == "inputFile":              self.str_inputFile              = value
            if key == "inputDir":               self.str_inputDir               = value
            if key == "outputDir":              self.str_outputDir              = value
            if key == "outputFileStem":         self.str_outputFileStem         = value
            if key == "outputFileType":         self.str_outputFileType         = value
            if key == "saveImages":             self._b_image                   = value
            if key == "label":                  self.str_label                  = value
            if key == "normalize":              self._b_normalize               = value
            if key == "lookupTable":            self.str_lookupTable            = value
            if key == "skipLabelValueList":     self.str_skipLabelValueList     = value
            if key == "filterLabelValueList":   self.str_filterLabelValueList   = value
            if key == "wholeVolume":            self.str_wholeVolume            = value
            if key == "verbosity":              self.verbosity                  = value
            if key == "version":                self.str_version                = value

        
    def tic(self):
        """
            Port of the MatLAB function of same name
        """
        global Gtic_start
        Gtic_start = time.time()

    def toc(self, *args, **kwargs):
        """
            Port of the MatLAB function of same name

            Behaviour is controllable to some extent by the keyword
            args:


        """
        global Gtic_start
        f_elapsedTime = time.time() - Gtic_start
        for key, value in kwargs.items():
            if key == 'sysprint':   return value % f_elapsedTime
            if key == 'default':    return "Elapsed time = %f seconds." % f_elapsedTime
        return f_elapsedTime

    def readFSColorLUT(self, str_filename):
        l_column_names = ["#No", "LabelName", "R", "G", "B", "A"]

        df_FSColorLUT = pd.DataFrame(columns=l_column_names)

        with open(str_filename) as f:
            for line in f:
                if line and line[0].isdigit():
                    line = re.sub(' +', ' ', line)
                    l_line = line.split(' ')
                    l_labels = l_line[:]
                    df_FSColorLUT.loc[len(df_FSColorLUT)] = l_labels
                    df_FSColorLUT['R'] = df_FSColorLUT['R'].astype(int)
                    df_FSColorLUT['G'] = df_FSColorLUT['G'].astype(int)
                    df_FSColorLUT['B'] = df_FSColorLUT['B'].astype(int)
                    df_FSColorLUT['A'] = df_FSColorLUT['A'].astype(int)    

        return df_FSColorLUT

    def get_unet(self):
        inputs = Input((img_depth, img_rows, img_cols, 1))
        conv11 = Conv3D(32, (3, 3, 3), activation='relu', padding='same')(inputs)
        conc11 = concatenate([inputs, conv11], axis=4)
        conv12 = Conv3D(32, (3, 3, 3), activation='relu', padding='same')(conc11)
        conc12 = concatenate([inputs, conv12], axis=4)
        pool1 = MaxPooling3D(pool_size=(2, 2, 2))(conc12)

        conv21 = Conv3D(64, (3, 3, 3), activation='relu', padding='same')(pool1)
        conc21 = concatenate([pool1, conv21], axis=4)
        conv22 = Conv3D(64, (3, 3, 3), activation='relu', padding='same')(conc21)
        conc22 = concatenate([pool1, conv22], axis=4)
        pool2 = MaxPooling3D(pool_size=(2, 2, 2))(conc22)

        conv31 = Conv3D(128, (3, 3, 3), activation='relu', padding='same')(pool2)
        conc31 = concatenate([pool2, conv31], axis=4)
        conv32 = Conv3D(128, (3, 3, 3), activation='relu', padding='same')(conc31)
        conc32 = concatenate([pool2, conv32], axis=4)
        pool3 = MaxPooling3D(pool_size=(2, 2, 2))(conc32)

        conv41 = Conv3D(256, (3, 3, 3), activation='relu', padding='same')(pool3)
        conc41 = concatenate([pool3, conv41], axis=4)
        conv42 = Conv3D(256, (3, 3, 3), activation='relu', padding='same')(conc41)
        conc42 = concatenate([pool3, conv42], axis=4)
        pool4 = MaxPooling3D(pool_size=(2, 2, 2))(conc42)

        conv51 = Conv3D(512, (3, 3, 3), activation='relu', padding='same')(pool4)
        conc51 = concatenate([pool4, conv51], axis=4)
        conv52 = Conv3D(512, (3, 3, 3), activation='relu', padding='same')(conc51)
        conc52 = concatenate([pool4, conv52], axis=4)

        up6 = concatenate([Conv3DTranspose(256, (2, 2, 2), strides=(2, 2, 2), padding='same')(conc52), conc42], axis=4)
        conv61 = Conv3D(256, (3, 3, 3), activation='relu', padding='same')(up6)
        conc61 = concatenate([up6, conv61], axis=4)
        conv62 = Conv3D(256, (3, 3, 3), activation='relu', padding='same')(conc61)
        conc62 = concatenate([up6, conv62], axis=4)

        up7 = concatenate([Conv3DTranspose(128, (2, 2, 2), strides=(2, 2, 2), padding='same')(conc62), conv32], axis=4)
        conv71 = Conv3D(128, (3, 3, 3), activation='relu', padding='same')(up7)
        conc71 = concatenate([up7, conv71], axis=4)
        conv72 = Conv3D(128, (3, 3, 3), activation='relu', padding='same')(conc71)
        conc72 = concatenate([up7, conv72], axis=4)

        up8 = concatenate([Conv3DTranspose(64, (2, 2, 2), strides=(2, 2, 2), padding='same')(conc72), conv22], axis=4)
        conv81 = Conv3D(64, (3, 3, 3), activation='relu', padding='same')(up8)
        conc81 = concatenate([up8, conv81], axis=4)
        conv82 = Conv3D(64, (3, 3, 3), activation='relu', padding='same')(conc81)
        conc82 = concatenate([up8, conv82], axis=4)

        up9 = concatenate([Conv3DTranspose(32, (2, 2, 2), strides=(2, 2, 2), padding='same')(conc82), conv12], axis=4)
        conv91 = Conv3D(32, (3, 3, 3), activation='relu', padding='same')(up9)
        conc91 = concatenate([up9, conv91], axis=4)
        conv92 = Conv3D(32, (3, 3, 3), activation='relu', padding='same')(conc91)
        conc92 = concatenate([up9, conv92], axis=4)

        conv10 = Conv3D(1, (1, 1, 1), activation='sigmoid')(conc92)

        model = Model(inputs=[inputs], outputs=[conv10])

        model.summary()
        #plot_model(model, to_file='model.png')

        model.compile(optimizer=Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.000000199), loss='binary_crossentropy', metrics=['accuracy'])

        return model

        
    

    def train(self, options):
        print('-'*30)
        print('Loading and preprocessing train data...')
        print('-'*30)


        imgs_train, imgs_mask_train = load_train_data(self)
        imgs_mask_train = imgs_mask_train.astype('float32')
        imgs_train = imgs_train.astype('float32')
        imgs_mask_train /= 255.  # scale masks to [0, 1]
        imgs_train /= 255.  # scale masks to [0, 1]


        print('-'*30)
        print('Creating and compiling model...')
        print('-'*30)

        model = self.get_unet()
        weight_dir =self.str_outputDir +'/weights'
        if not os.path.exists(weight_dir):
            os.mkdir(weight_dir)
        model_checkpoint = ModelCheckpoint(os.path.join(weight_dir, project_name + '.h5'), monitor='val_loss', save_best_only=True)

        log_dir = self.str_outputDir+'/logs'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        csv_logger = CSVLogger(os.path.join(log_dir,  project_name + '.txt'), separator=',', append=False)

        print('-'*30)
        print('Fitting model...')
        print('-'*30)


        model.fit(imgs_train, imgs_mask_train, batch_size=1, epochs=10, verbose=1, shuffle=True, validation_split=0.10, callbacks=[model_checkpoint, csv_logger])




        print('-'*30)
        print('Training finished')
        print('-'*30)
        
        
    def predict(self,options):



        print('-'*30)
        print('Loading and preprocessing test data...')
        print('-'*30)
        create_test_data(options)

        imgs_test = load_test_data(options)
        imgs_test = imgs_test.astype('float32')


        imgs_test /= 255.  # scale masks to [0, 1]


        print('-'*30)
        print('Loading saved weights...')
        print('-'*30)

        model = self.get_unet()
        weight_dir =options.inputdir+ '/weights'
        if not os.path.exists(weight_dir):
            os.mkdir(weight_dir)
        model.load_weights(os.path.join(weight_dir, project_name + '.h5'))

        print('-'*30)
        print('Predicting masks on test data...')
        print('-'*30)

        imgs_mask_test = model.predict(imgs_test, batch_size=1, verbose=1)

        npy_mask_dir = 'test_mask_npy'
        if not os.path.exists(npy_mask_dir):
            os.mkdir(npy_mask_dir)

        np.save(os.path.join(options.outputdir, project_name + '_mask.npy'), imgs_mask_test)

        print('-' * 30)
        print('Saving predicted masks to files...')
        print('-' * 30)

        imgs_mask_test = preprocess_squeeze(imgs_mask_test)
        # imgs_mask_test /= 1.7
        #imgs_mask_test = np.around(imgs_mask_test, decimals=0)
        #info = np.iinfo(np.uint16) # Get the information of the incoming image type
        #imgs_mask_test = imgs_mask_test.astype(np.uint16)
        #imgs_mask_test=imgs_mask_test* info.max # convert back to original class/labels
        imgs_mask_test = (imgs_mask_test*255.).astype(np.uint8)
        count_visualize = 1
        count_processed = 0
        pred_dir = 'preds'
        if not os.path.exists(pred_dir):
            os.mkdir(pred_dir)
        pred_dir = os.path.join(options.outputdir, project_name)
        if not os.path.exists(pred_dir):
            os.mkdir(pred_dir)
        for x in range(0, imgs_mask_test.shape[0]):
            for y in range(0, imgs_mask_test.shape[1]):
                if (count_visualize > 1) and (count_visualize < 16):
                    save_img=imgs_mask_test[x][y].astype(np.uint16)
                    imsave(os.path.join(pred_dir, 'pred_' +str( count_processed )+ '.png'), save_img)
                    count_processed += 1

                count_visualize += 1
                if count_visualize == 17:
                    count_visualize = 1
                if (count_processed % 100) == 0:
                    print('Done: {0}/{1} test images'.format(count_processed, imgs_mask_test.shape[0]*14))

        print('-'*30)
        print('Prediction finished')
        print('-'*30)

    def run(self):
    
        self.train(self)


class object_factoryCreate:
    """
    A class that examines input file string for extension information and
    returns the relevant convert object.
    """

    def __init__(self, args):
        """
        Parse relevant CLI args.
        """
        

        self.C_convert = mri_unet(
            inputFile            = args.inputFile,
            inputDir             = args.inputDir,
            outputDir            = args.outputDir,
            outputFileStem       = args.outputFileStem,
            outputFileType       = args.outputFileType,
            saveImages           = args.saveImages,
            label                = args.label,
            normalize            = args.normalize,
            lookupTable          = args.lookupTable,
            skipLabelValueList   = args.skipLabelValueList,
            filterLabelValueList = args.filterLabelValueList,
            wholeVolume          = args.wholeVolume,
            printElapsedTime     = args.printElapsedTime,
            man                  = args.man,
            synopsis             = args.synopsis,
            verbosity            = args.verbosity,
        )


