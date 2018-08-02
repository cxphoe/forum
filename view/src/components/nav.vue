<template>
  <header class="nav-wrapper">
    <nav class="nav">
      <ul>
        <li>
          <router-link
            :to="{ name: 'topicIndex' }"
          ><img class="logo-img" src="/static/img/logo.png"></router-link>
        <li>
        <li>
          <router-link
            :to="{ name: 'topicIndex' }"
            class="link pv2 ph3 gray6 hover-blue"
          >首页</router-link>
        <li>
          <router-link
            :to="{ name: 'topicIndex' }"
            class="link pv2 ph3 gray6 hover-blue"
          >分类</router-link>
        </li>
        <li class="">
          <el-button type="primary" class="pa0">
            <router-link
              :to="{ name: 'topicEdit' }"
              class="block pv2 ph3 link white hover-white"
              target="_blank"
            >发表话题</router-link>
          </el-button>
        </li>
      </ul>

      <!-- 没有用户数据时，展示登陆/注册按钮 -->
      <ul v-show="isGuest">
        <li>
          <el-button type="primary" class="pa0">
            <router-link
              :to="{ name: 'login' }"
              class="pv2 ph3 block link white hover-white"
            >登陆</router-link>
          </el-button>
        </li>
        <li>
          <el-button type="" class="pa0">
            <router-link
              :to="{ name: 'login', params: { mode: 'register' } }"
              class="pv2 ph3 block link signup-btn"
            >注册</router-link>
          </el-button>
        </li>
      </ul>

      <!-- 有用户数据，展示提醒/私信/用户相关按钮 -->
      <ul v-show="!isGuest" class="icons">
        <li>
          <div v-popover:note class="link gray6 f4">
            <i class="fas fa-bell"></i>
          </div>
        </li>
        <li>
          <div v-popover:message class="link gray6 f4 relative">
            <i class="fas fa-comments"></i>
            <div v-if="newMessages.length > 0" class="absolute sign-note" />
          </div>
        </li>
        <li>
          <div v-popover:user class="link">
            <img class="nav-avatar" :src="currentUser.avatar">
          </div>
        </li>
      </ul>
    </nav>

    <el-popover
      ref="note"
      trigger="click"
      width="360"
    >
      <div class="popover-content text">
        <div>note1</div>
        <div>note2</div>
        <div>note3</div>
      </div>
    </el-popover>
    <el-popover
      ref="message"
      trigger="click"
      width="360"
    >
      <div class="popover-content text">
        <template v-if="messages.length > 0">
          <div
            v-for="m in messages"
            :key="m.id"
            class="flex items-center"
          >
            <img class="avatar mr3" :src="m.avatar">
            <span>{{ m.title }}</span>
          </div>
        </template>
        <div v-else class="note">没有信息</div>
      </div>
    </el-popover>
    <el-popover
      ref="user"
      trigger="hover"
      width="100"
      class="user-popover"
    >
      <div class="popover-content user">
        <div @click="toHomepage">主页</div>
        <div @click="toSetting">设置</div>
        <div @click="logout">退出</div>
      </div>
    </el-popover>
  </header>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Button, Popover, Notification } from 'element-ui'
import { isOk } from '@/utils'

Vue.use(Button)
Vue.use(Popover)

export default {
  name: 'Nav',

  computed: {
    newMessages() {
      // 返回还没被读过的信息
      return this.messages.filter((m) => m.read === false)
    },

    ...mapState([
      'currentUser',
      'isGuest',
      'messages',
    ]),
  },

  methods: {
    toHomepage() {
      this.$router.push({
        name: 'userHomepage',
        params: { id: this.currentUser.id },
      })
    },

    toSetting() {
      this.$router.push({
        name: 'userSetting',
        params: { id: this.currentUser.id },
      })
    },

    logout() {
      this.$http.get(this.$apiRoutes.logout).then((res) => {
        if (isOk(res.status)) {
          Notification({
            title: res.data,
            type: 'success',
          })
          this.$store.commit('clearCurrentUser')
          this.$store.dispatch('getCurrentUser')
        }
      })
    },
  },
}
</script>

<style lang="scss">
.nav-wrapper {
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  left: 0;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;

  .nav {
    align-items: center;
    display: flex;
    height: 3.5rem;
    justify-content: space-between;
    margin: auto;
    max-width: 1000px;

    .logo-img {
      width: 2.5rem;
    }

    .signup-btn {
      color: $color-first;
    }

    .nav-avatar {
      border-radius: 4px;
      height: 30px;
      width: 30px;
    }

    & > ul {
      align-items: center;
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
      & > li {
        display: inline-flex;
        & + li {
          margin-left: 1rem;
        }
      }

      &.icons {
        & > li + li {
          margin-left: 2rem;
        }

        .sign-note {
          background: $color-contrary;
          border-radius: 50%;
          padding: .25rem;
          position: absolute;
          right: 0;
          top: 4px;
        }
      }
    }
  }
}

.popover-content {
  position: relative;

  .avatar {
    border-radius: 4px;
  }

  .note {
    color: $color-gray5;
    font-size: 1.5rem;
    left: 50%;
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
  }

  &.text {
    height: 400px;
    overflow-y: scroll;

    & > * {
      margin: 0 1rem;
      padding: 1rem 0;
    }
  }

  &.user > * {
    cursor: pointer;
    margin: 0;
    padding: .5rem;

    &:hover {
      background-color: $color-light;
    }
  }
}
</style>
