## CAPTCHA generator. Just for fun :).

The CAPTCHA created like this:

![1](https://github.com/zstu-lly/CRNN-Keras/blob/master/examples/00aq.jpg)
![2](https://github.com/zstu-lly/CRNN-Keras/blob/master/examples/YndC.jpg)
![3](https://github.com/zstu-lly/CRNN-Keras/blob/master/examples/C1gw.jpg)


Actually this is used to generate training data of project [CRNN-Keras](https://github.com/zstu-lly/CRNN-Keras)

### example:
```python
from captcha.core import Captcha

c = Captcha(150, 40, debug=True)
c.batch_create_img(10)
```

#### TODO
 - improve performance.
 - support multi parameters.
