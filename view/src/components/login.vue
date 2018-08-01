<template>
  <div class="login-wrapper">
    <img src="static/img/bg.png">
    <el-card class="board">
      <transition :name="transitionName" mode="out-in">
        <div :key="1" v-if="mode === 'login'" class="flex flex-column">
          <el-form ref="login" :model="login.form" :rules="login.rules">
            <el-form-item prop="username">
              <el-input v-model="login.form.username" class="text-input" placeholder="用户名" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="login.form.password" class="text-input" placeholder="密码" type="password" />
            </el-form-item>
          </el-form>
          <div v-html="result.login" />
          <el-button class="mt4" type="primary" @click="handleLogin">登陆</el-button>
          <div class="flex justify-sb mt5">
            <div/>
            <div class="link" @click="mode = 'register'">注册</div>
          </div>
        </div>

        <div :key="2" v-else-if="mode === 'register'" class="flex flex-column auth-form">
          <el-form ref="register" :model="register.form" :rules="register.rules">
            <el-form-item prop="username">
              <el-input v-model="register.form.username" class="text-input" placeholder="用户名" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="register.form.password" class="text-input" placeholder="密码" type="password" />
            </el-form-item>
            <el-form-item prop="verifyPwd">
              <el-input v-model="register.form.verifyPwd" class="text-input" placeholder="确认密码" type="password" />
            </el-form-item>
          </el-form>
          <div v-html="result.register" />
          <el-button class="mt4" type="primary" @click="handleRegister">注册</el-button>
          <div class="flex justify-sa mt5">
            <div>
              已经注册？
              <span class="link" @click="mode = 'login'">登陆</span>
            </div>
          </div>
        </div>
      </transition>
    </el-card>
  </div>
</template>

<script>
import Vue from 'vue'
import { Button, Card, Form, FormItem, Input } from 'element-ui'
import { isOk, clearObj, buildFormdata } from '@/utils'
import { baseUrl } from '@/config'

Vue.use(Button)
Vue.use(Card)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)

export default {
  name: 'Login',

  data() {
    const form = {
      login: {
        username: '',
        password: '',
      },
      register: {
        username: '',
        password: '',
        verifyPwd: '',
      }
    }
    const validators = {
      username(rule, value, callback) {
        let errMsg = null
        let parts = value.split('')
        // 字母、中文开头
        let first = /[a-zA-z\u4e00-\u9fa5]/
        let firstMatch = first.exec(parts[0])
        // 字母、数字、下划线、中文
        let middle = /[a-zA-Z0-9_\u4e00-\u9fa5]*/
        let middleMatch = middle.exec(parts.slice(1).join(''))

        if (!value) {
          errMsg = '用户名不能为空'
        } else if (value.length < 2) {
          errMsg = '用户名字符不能少于 2 个'
        } else if (!firstMatch) {
          errMsg = '第一个字符只能是字母或中文'
        } else if (!middleMatch) {
          errMsg = '只能包括字母、中文、数字以及下划线'
        }

        return callback(errMsg ? (new Error(errMsg)) : undefined)
      },

      password(rule, value, callback) {
        if (value.length < 3) {
          return callback(new Error('密码不能少于3个字符'))
        } else {
          return callback()
        }
      },

      verifyPwd(rule, value, callback) {
        if (value !== form.register.password) {
          return callback(new Error('前后两次输入的密码不一致'))
        } else {
          return callback()
        }
      },
    }

    return {
      mode: 'login',
      result: {
        login: '',
        register: '',
      },
      login: {
        form: form.login,
        rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' }
          ],
        },
      },
      register: {
        form: form.register,
        rules: {
          username: [
            { validator: validators.username, trigger: 'change' }
          ],
          password: [
            { validator: validators.password, trigger: 'change' }
          ],
          verifyPwd: [
            { validator: validators.verifyPwd, trigger: 'change' }
          ],
        },
      },
    }
  },

  computed: {
    transitionName() {
      return this.mode === 'login' ? 'fade-slide-l' : 'fade-slide-r'
    }
  },

  methods: {
    successResult(text) {
      return `<span style="color:green">${text}</span>`
    },

    failResult(text) {
      return `<span style="color:red">${text}</span>`
    },

    handleLogin() {
      this.$refs.login.validate((valid) => {
        if (valid) {
          let formdata = buildFormdata(this.login.form)

          this.$http.post(this.$apiRoutes.login, formdata).then((res) => {
            if (isOk(res.status)) {
              let user = res.data
              user.avatar = baseUrl + user.avatar
              this.$store.commit('setCurrentUser', { user })
              this.$router.push({ name: 'topicIndex' })
            } else {
              this.failResult(res.data)
            }
          }).catch(() => {
            this.result.login = this.failResult('服务器内部出错')
          })
        }
      })
    },

    handleRegister() {
      this.$refs.register.validate((valid) => {
        if (valid) {
          let formdata = buildFormdata(this.register.form, ['username', 'password'])

          this.$http.post(this.$apiRoutes.register, formdata).then((res) => {
            if (isOk(res.status)) {
              this.successResult(res.data)
              this.mode = 'login'
            } else {
              this.failResult(res.data)
            }
          }).catch(() => {
            this.result.register = this.failResult('服务器内部出错')
          })
        }
      })
    },
  },

  mounted() {
    for (let dict of [this.login.form, this.register.form, this.result]) {
      clearObj(dict)
    }
  },

  created() {
    // 根据路由传参觉得一开始展示哪个界面
    let mode = this.$route.params.mode
    this.mode = mode || 'login'
  },
}
</script>

<style lang="scss">
.login-wrapper {
  background: linear-gradient(180deg, transparent, #fff);
  height: 100%;
  max-width: none !important;
  overflow: hidden;
  padding: 0 !important;
  position: relative;
  margin: 0 !important;

  .board {
    border-radius: .5rem;
    left: 50%;
    padding: 2rem 0 1rem;
    position: absolute;
    transform: translate(-50%, -50%);
    top: 50%;
    width: 360px;

    .link {
      color: $color-first;

      &:hover {
        color: $color-gray7;
      }
    }

    .text-input {
      padding: 0;

      input {
        border: none;
        border-bottom: 1px solid #ddd;
        border-radius: 0;
        font-size: 1rem;
        outline: none;
        padding: 5px;
      }
    }
  }
}
</style>
