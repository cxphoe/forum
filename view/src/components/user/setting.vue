<template>
  <el-card class="user-setting">
    <input
      ref="avatar" type="file"
      @change="handleImg"
      accept="image/jpg, image/jpeg, image/png"
      hidden
    >
    <div class="avatar" @click="avatarUpload">
      <img :src="user.avatar">
      <div class="note">
        <i class="fas fa-camera"></i>
        <div>修改我的头像</div>
      </div>
    </div>
    <el-form :model="user" class="user-form" label-width="80px">
      <el-form-item label="用户名字">
        <el-input v-model="user.username" @change="handleChange($event, 'username')"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="upload">保存</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import Vue from 'vue'
import { mapActions } from 'vuex'
import { Button, Card, Form, FormItem, Input, Notification } from 'element-ui'
import { buildFormdata, isOk } from '@/utils'
import { getUser } from '@/http/requests'

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
      avatarFile: null,
      uploadData: {},
    }
  },

  methods: {
    getUser(id) {
      getUser(id, (user) => {
        this.user = user
      }, () => {
        Notification({
          title: '用户数据数据不存在',
          type: 'error',
        })
      })
    },

    handleImg(event) {
      let file = event.target.files[0]
      if (file) {
        let url = URL.createObjectURL(file)
        this.user.avatar = url
        this.uploadData.avatar = file
      }
    },

    handleChange(value, prop) {
      this.uploadData[prop] = value
    },

    avatarUpload() {
      this.$refs.avatar.click()
    },

    upload() {
      let form = buildFormdata(this.uploadData)
      this.$http.post(`${this.$apiRoutes.updateUser}/${this.user.id}`, form).then((res) => {
        if (isOk(res.status)) {
          Notification({
            title: '修改成功',
            type: 'success',
          })
          this.getCurrentUser()
        } else {
          Notification({
            title: '修改失败',
            type: 'error',
          })
        }
      })
    },

    clear() {
      this.uploadData = {}
      this.avatarFile = null
    },

    ...mapActions([
      'getCurrentUser',
    ]),
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
