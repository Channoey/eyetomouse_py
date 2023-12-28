## 1.前端

yiqing-master/yq-vue/src/views/eye.vue：眼动开始界面，背景图用iframe嵌入，下方的状态信息隔很短的时间自动向后端发起请求（后端收到请求到数据库里查信息）

yiqing-master/yq-vue/src/views/eyeManage.vue： 录入照片界面，选择的分辨率和间隔时间都是虚拟的，答辩的时候可以说是选择了之后给每个用户都会存起来



## 2.后端

接口都集中在 yiqing-master/src/main/java/com/dzl/controller/EyeController.java

/start接口：前端眼动开始界面点击开始后到这，然后执行python文件eyetomouse_py/run.py

/train接口：前端录入照片界面点击开始后到这，然后执行python文件eyetomouse_py/train_model.py

/message接口：前端的轮询状态信息查询到这，然后查询数据库，查到最新的信息返回



## 3.python文件

**run.py:**

1.后端传入用户名开始运行

2.键盘按键绑定事件，按q直接全部退出

3.对已有照片进行训练，得到模型，训练过程描述 https://zhuanlan.zhihu.com/p/374618762 

4.开始循环主程序

5.函数scan用于后面鼠标的移动，函数scan2用于眨眼功能和眨眼画面的绘制

6.FLAG_START用于判断是否为第一次，如果是第一次，就判断是否检测到眼睛，如果检测不到退出

7.而后根据函数scan和scna2返回数据进行相应操作，如果检测到双眼，并且开启移动功能，如果检测到一只眼，或者没检测到眼睛，根据是否开启眨眼功能进行判断

8.各个步骤都有相应的向数据库里插状态信息的过程



**Train_model.py:**

1.后端传入用户名开始运行，如果没有相应用户数据则新建文件夹

2.键盘绑定，按q结束，鼠标绑定，当点击鼠标左键时执行拍照程序

3.开始拍照，并截取眼睛图片和鼠标坐标存储，过程参照 https://zhuanlan.zhihu.com/p/374618762 

4.每进行一次截取就往数据库里存入现在的次数，让前端状态信息可以看到当前的次数信息