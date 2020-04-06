---
layout: post
published: true
title: tensorflow-gpu error
subtitle: Failed to get convolution algorithm. This is probably because cuDNN failed to initialize
date: '2020-04-06'
---

Tensorflow-gpu 2.1, 

nvidia rtx 2070(cuda10.2 driver, 440.64), 

cuda 10.1(runtime) 

cudnn 7.6.2 , 

ubuntu 18.04

위 환경에서 Tensorflow-gpu package쓰려고하면 



Failed to get convolution algorithm. This is probably because cuDNN failed to initialize ...



이런 메세지를 볼 수도 있다. 



아래와 같이하면 해결은 되는데 근본적인 해결책인지는 좀 알아봐야할 듯 하다.

```python
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)
```



물론 상황에 맞는 gpu index를 주면 되고, multi-GPU 환경은 아니라서 그부분 해결책이 필요하다면 또 찾아봐야한다.

