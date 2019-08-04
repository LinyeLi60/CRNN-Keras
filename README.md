# CRNN (CNN+RNN) 

OCR(Optical Character Recognition) consists of text localization + text recognition.
(text localization finds where the characters are, and text recognition reads the letters.)

You can use this [text localizaion model](https://github.com/qjadud1994/OCR_Detector) I have studied.

After performing localization, each text area is cropped and used as input for text recognition.
An example of text recognition is typically the CRNN

Combining the [text detector](https://github.com/qjadud1994/OCR_Detector) with a [CRNN](https://github.com/qjadud1994/CRNN-Keras) makes it possible to create an OCR engine that operates end-to-end.

## CRNN

**[CRNN](https://arxiv.org/pdf/1507.05717.pdf)** is a network that combines CNN and RNN to process images containing sequence information such as letters.

It is mainly used for OCR technology and has the following advantages.
1. End-to-end learning is possible.
2. Sequence data of arbitrary length can be processed because of LSTM which is free in size of input and output sequence.
3. There is no need for a detector or cropping technique to find each character one by one.

You can use CRNN for OCR, license plate recognition, text recognition, and so on. 
It depends on what data you are training.

I used a slightly modified version of the original CRNN model.
(Input size : 70x30 -> 128x64 & more CNN Layer)

## Network

![CRNN Network](https://github.com/qjadud1994/CRNN-Keras/blob/master/photo/Network.jpg)

### Convolutional Layer
Extracts features through CNN Layer (VGGNet, ResNet ...).

### Recurrent Layer
Splits the features into a certain size and inserts them into the input of the Bidirectional LSTM or GRU.

### Transcription Layer

Conversion of Feature-specific predictions to Label using CTC (Connectionist Temporal Classification).

- - -

## catpcha recognition using CRNN

I used CRNN to recognize catpcha.

![catpcha example](https://github.com/zstu-lly/CRNN-Keras/blob/master/examples/00aq.jpg)
![catpcha example](https://github.com/zstu-lly/CRNN-Keras/blob/master/examples/YndC.jpg)


I updated the [captcha generator](https://github.com/zstu-lly/CRNN-Keras/tree/master/generate_captcha) for those who lacked captcha pictures.


## Result
![Result](https://github.com/zstu-lly/CRNN-Keras/blob/master/examples/prediction.png)

CRNN works well for license plate recognition as follows.


## How to Training

First, you need a lot of cropped captcha images. <br/>
(The captcha 1234 is indicated as "1234.jpg"). <br/>

After creating training data in this way, put it in 'DB/train' directory and run [training.py](https://github.com/qjadud1994/CRNN-Keras/blob/master/training.py).

## File Description

os : Ubuntu 16.04.4 LTS

GPU : Telas V100 (16GB)

Python : 3.6.5

Tensorflow : 1.9.0

Keras : 2.1.3

CUDA, CUDNN : 9.0, 7.0

|       File         |Description                                       |
|--------------------|--------------------------------------------------|
|Model .py           |Network using CNN (VGG) + Bidirectional LSTM      |
|Model_GRU. py       |Network using CNN (VGG) + Bidirectional GRU       |
|Image_Generator. py |Image batch generator for training                |
|parameter. py       |Parameters used in CRNN                           |
|training. py        |CRNN training                                     |
|Prediction. py      |CRNN prediction                                   |
