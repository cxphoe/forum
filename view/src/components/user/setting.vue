<template>
  <el-card class="user-setting">
    <div class="avatar">
      <img :src="user.avatar">
      <div class="note">
        <i class="fas fa-camera"></i>
        <div>修改我的头像</div>
      </div>
    </div>
    <el-form :model="user" class="user-form" label-width="80px">
      <el-form-item label="用户名字">
        <el-input v-model="user.username"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="upload">提交</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import Vue from 'vue'
import { Button, Card, Form, FormItem, Input } from 'element-ui'
import { baseUrl } from '@/config'

Vue.use(Button)
Vue.use(Card)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)

export default {
  name: 'UserSetting',

  data() {
    return {
      user: {},
    }
  },

  methods: {
    getUser(id) {
      let url = `${this.$apiRoutes.getUser}/${id}`
      this.$http.get(url).then((res) => {
        let u = res.data
        u.avatar = baseUrl + u.avatar
        this.user = u
      })
    },

    upload() {
      
    },
  },

  created() {
    let id = this.$route.params.id
    this.getUser(id)
  },
}
</script>

<style lang="scss">
.user-setting {

  .avatar {
    border-radius: .5rem;
    cursor: pointer;
    display: inline-block;
    height: auto;
    position: relative;
    width: auto;
    user-select: none;

    img {
      height: 10rem;
      width: 10rem;
    }

    .note {
      color: #fff;
      font-size: 1.5rem;
      left: 50%;
      position: absolute;
      text-align: center;
      top: 50%;
      transform: translate(-50%, -50%);
      width: 10rem;

      div {
        font-size: 1rem;
        margin-top: 1.5rem;
      }
    }
  }

  .user-form {
    display: flex;
    flex-direction: column;
    margin-top: 2rem;
    width: 25rem;
  }
}
</style>
