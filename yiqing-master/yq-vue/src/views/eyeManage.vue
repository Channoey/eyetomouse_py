<template>
  <div>
    <h1 style="margin-top: 25px; margin-left:150px;font-size: 25px; color: #697eff;margin-right: 100px">屏幕分辨率：</h1>
    <el-select v-model="value" placeholder="请选择" value="1080*720" style="margin-top: 20px;margin-left: 150px;font-size: 25px;" size="big">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
      </el-option>
    </el-select>
    <h1 style="margin-top: 50px; margin-left:150px;font-size: 25px; color: #697eff;margin-right: 100px">检测间隔（ms）：</h1>
<!--    <span class="demonstration"></span>-->
    <el-slider v-model="interval" style="width: 300px;margin-left: 150px;margin-top: 20px;"></el-slider>
    <el-button type="primary" style="width: 150px;height:70px;margin-left: 150px;margin-top: 50px;font-size: 30px" @click="clickStart">开始检测</el-button>
    <p style="margin-left: 200px;margin-top: 10px">按q退出</p>
    <h1 style="margin-top: 50px; font-size: 30px; color: #697eff;margin-right: 100px;margin-left: 150px">状态信息：</h1>
    <h1 style="margin-top: 30px; font-size: 30px; color: #697eff;margin-left: 150px">{{message}}</h1>
  </div>


</template>

<script >
export default {
  name: "eyeManage",
  mounted() {
    this.loadMessage()
    this.timer = window.setInterval(() => {
      setTimeout(() => {
        this.loadMessage()
      },0)
    },1000)
  },
  destroyed() {
    window.clearInterval(this.timer)
  },
  data(){
    return {
      options: [{
        value: '1080*720',
        label: '1080*720'
      }, {
        value: '1920*1080',
        label: '1920*1080'
      }, {
        value: '2560*1440',
        label: '2560*1440'
      }, {
        value: '3440*2560',
        label: '3440*2560'
      }, {
        value: '4600*2400',
        label: '4600*2400'
      }],
      value: '',
      interval: 10,
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      message: "I am a message!"
    }
  },
  methods:{
    clickStart(){
      const username = this.user.username
      if(this.value===''){
        this.$alert('请填入分辨率！', '提示', {
          confirmButtonText: '好的',
        });
      }else{
        console.log(this.value)
        this.$confirm('分辨率：'+this.value+'            间隔时间:'+this.interval+"ms", '是否要继续', {
          confirmButtonText: '继续',
          cancelButtonText: '取消',
          type: 'info'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '等待检测程序启动!'
          });
          this.request.post("/train",{user: username})
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消！'
          });
        });
      }

    },
    loadMessage(){
      this.request.get("/message").then(res=>{
          this.message = res.data
          }
      )
    }
  }
}
</script>

<style scoped>

</style>