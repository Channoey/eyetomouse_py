<template>
<!--  <div class="d2">-->
  <div>
    <div>
      <h1 style="font-size: 30px; color: #3333CC;z-index:2;position: absolute;left: 260px;top:550px">状态信息：</h1>
      <h1 style="font-size: 30px; color: #3333CC;-webkit-filter:blur(10px);-moz-filter:blur(10px);z-index:2;position: absolute;left: 260px;top:600px">{{message}}</h1>
      <h1 style="font-size: 30px; color: #3333CC;z-index:2;position: absolute;left: 260px;top:600px">{{message}}</h1>
      <h1 style="font-size: 20px; color: black;z-index:2;position: absolute;left: 260px;top:100px">欢迎使用眼动交互系统，详细说明请点击下方按钮</h1>
      <div style="width: 400px; height: 400px; line-height: 200px; border-radius: 50%; background-color: #1E90FF;
        font-size: 40px; color: #fff; text-align: center; cursor: pointer; box-shadow: 0 0 30px rgba(0, 0, 0, .2);
         opacity: 0;position: absolute;top:190px;left:610px;z-index: 1;-webkit-filter:blur(1px);-moz-filter:blur(1px);" @click="handleStart">
      </div>
      <iframe src="http://resource.xcmwh0929.top/file/eyetomouse/background/" height="600" width="1200" style="z-index: 0" scrolling="no" frameborder="0px"></iframe>
      <button id="btn" @click="openInNewTab('http://resource.xcmwh0929.top/file/eyetomouse/mddocument.html')">转到文档</button>
    </div>

  </div>






</template>

<script>


export default {
  name: "test",
  mounted() {
    this.loadMessage()
    this.timer = window.setInterval(() => {
      setTimeout(() => {
        this.loadMessage()
      },0)
    },1000)
    iframe.attachEvent
  },
  methods:{
    handleStart(){
      const username = this.user.username
      this.request.post("/start",{user: username})
    },
    openInNewTab(url) {
      window.open(url, '_blank', 'noreferrer');
    },
    loadMessage(){
      this.request.get("/message").then(res=>{
          console.log(res.data)
          if(res.data==="-4"){
            this.$alert('未检测到眼睛', '发生错误', {
              confirmButtonText: '好的',
              callback: action => {
                this.$message({
                  type: 'info',
                  message: `action: ${ action }`
                });
              }
            });
          }
          else if(res.data==="-6"){
            this.$alert('未训练模型，结束程序！', '发生错误', {
              confirmButtonText: '好的',
              callback: action => {
                this.$message({
                  type: 'info',
                  message: `action: ${ action }`
                });
              }
            });
          }
          else{
            this.message = res.data
          }

          }
      )
    }
  },
  destroyed() {
    window.clearInterval(this.timer)
  },
  data(){
    return{
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      message: "I am message!"
    }
  }
}
</script>

<style scoped>
.d2 {
  min-width: 50%;
  width: 100px;
  height: 100px;
  position: absolute;
  display:flex;
  justify-content:flex-end;
}
.btn1 {
  position: relative;
  right: 10px;
  top: 100px;
  margin-right: 100px;
}

#btn {
  font-size: 20px;
  height: 40px;
  margin: 6px 0;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  border: none;
  font-weight: bold;
}

#btn{
  margin-top: 20px;
  cursor:pointer;
  position: absolute;
  overflow: hidden;
  top: 125px;
  left: 260px;
  transition: 0.7s;
}

#btn:hover{
  background-color: rgb(144, 160, 167);
}

#btn::before,#btn::after{
  content: "";
  height:90px;
  width: 100px;
  display: block;
  background-color: mediumaquamarine;
  opacity: 0.5;
  filter: blur(30px);
  position: absolute;
  overflow: hidden;
  left:0;
  top:0;
  transform: skewX(-20deg);
  transform: translateX(-100px);
}

#btn::after{
  filter:blur(6px);
  width: 40px;
  left:60px;
  opacity: 0;
  background-color: rgba(64, 224, 208, 0.307);
}

#btn:hover::before{
  transform: translateX(320px);
  transition: 1s;
  opacity: 1;

}
#btn:hover::after{
  transform: translateX(320px);
  transition: 1s;
  opacity: 1;
}

</style>