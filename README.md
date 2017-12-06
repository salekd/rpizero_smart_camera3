# Smart security camera with Raspberry Pi Zero and OpenFaaS

This repository shows how to turn Raspberry Pi Zero into a smart security camera using serverless functions. The solution is based on the following key components:
* use of available **Motion** software to detect movement,
* use serverless function deployed by **OpenFaaS**, running **TensorFlow Object Detection API** with the **SDD MobileNet v1** model,
* use serverless funciton deployed by **OpenFaaS** to upload images into **Amazon S3** and send e-mail notifications,
* enable remote live video steaming through **remot3.it**

The installation procedure is documented here https://github.com/salekd/rpizero_smart_camera3/wiki

![](https://github.com/salekd/rpizero_smart_camera/blob/master/camera.JPG)
