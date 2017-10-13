# python3_spidertbmm
Python3抓取淘宝网淘女郎个人信息和所有照片

[淘女郎首页地址](https://mm.taobao.com/search_tstar_model.htm?spm=5679.126488.640745.2.69891757XQaub1)

### 流程分析
1. 打开首页发现首页的个人信息都是异步加载的，chrome或者fiddler可以看到请求的一些信息，还有分页，构造请求信息访问获取所有用户基本信息+userid
2. 随便点击一个人信息进去,如这个地址：https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20=176817195. 
查看相册，发现相册都是跟用户id关联的，也就是说根据用户id可以获取到这个用户的所有albumid(相册id)（当然相册里面也有分页，这个就没做，有兴趣的自己再改正下）
3. 随便点击一个相册进去，经过分析，每个相册的所有照片可以根据userid+albumid得到。
所以根据前俩步获取到的userid和albumid替换下面的地址，返回json，可获取到这个相册的所有图片id(picid)和图片地址
https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=176817195&album_id=10000962815
4. 发现3页面的图片也是异步post请求获取的，请求地址为：https://mm.taobao.com/album/json/get_photo_data.htm?_input_charset=utf-8，
post参数根据chrome查看的请求头构造。
5. 图片的真实地址找到了，直接保存就好了
