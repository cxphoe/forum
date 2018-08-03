<template>
  <div class="user-homepage">
    <el-card class="shadow-2dp">
      <div class="user-meta">
        <img class="avatar" :src="user.avatar">
        <div>{{ user.username }}</div>
        <el-button
          v-if="!isGuest && !isFollowed && currentUser.id !== user.id"
          type="primary"
          size="small"
          @click="follow"
        >关注</el-button>
        <el-button
          v-else-if="!isGuest"
          type="danger"
          size="small"
          @click="unfollow"
        >取消关注</el-button>
      </div>
    </el-card>
    <el-card class="shadow-2dp">
      <div
        v-for="(t, index) in user.topics"
        :key="index"
      >
        <div>{{ `${user.username} ${t.pulished ? '发表' : '回复'}` }}</div>
        <router-link :to="{ name: 'topicDetail', params: { id: t.id } }">{{ t.title }}</router-link>
      </div>
    </el-card>
    <el-card>
      <div slot="header">关注者</div>
      <router-link
        v-for="f in user.followers"
        :key="f.id"
        :to="{ name: 'userHomepage', params: { id: f.id } }"
        class="link"
      >
        <img class="avatar" :src="baseUrl + f.avatar">
        <span>{{ f.username }}</span>
      </router-link>
    </el-card>
    <el-card>
      <div slot="header">关注的人</div>
      <router-link
        v-for="f in user.followed"
        :key="f.id"
        :to="{ name: 'userHomepage', params: {id : f.id} }"
        class="link"
      >
        <img class="avatar" :src="baseUrl + f.avatar">
        <span>{{ f.username }}</span>
      </router-link>
    </el-card>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Card, Button, Message } from 'element-ui'
import { getUserDetail } from '@/http/requests'
import { isOk } from '../../utils'
import { baseUrl } from '@/config'

Vue.use(Button)
Vue.use(Card)

export default {
  name: 'UserHomepage',

  data() {
    return {
      user: {},
      baseUrl,
    }
  },

  computed: {
    isFollowed() {
      let followedIds = this.currentUser.followedIds || []
      return followedIds.includes(this.user.id)
    },

    ...mapState([
      'isGuest',
      'currentUser',
      'token',
    ]),
  },

  methods: {
    follow() {
      let url = this.$apiRoutes.addFollow
      this.$http.post(url, {
        user_id: this.user.id,
        follower_id: this.currentUser.id,
      }, {
        params: { token: this.token },
      }).then((res) => {
        if (isOk(res.status)) {
          Message.success('关注成功')
        } else {
          Message.error('关注失败')
        }
      })
    },

    unfollow() {
      let url = this.$apiRoutes.deleteFollow
      this.$http.post(url, {
        user_id: this.user.id,
        follower_id: this.currentUser.id,
      }, {
        params: { token: this.token },
      }).then((res) => {
        if (isOk(res.status)) {
          Message.success('取消关注成功')
        } else {
          Message.error('取消关注失败')
        }
      })
    },
  },

  created() {
    let id = this.$route.params.id
    getUserDetail(id, (user) => {
      this.user = user
    })
  },
}
</script>

<style lang="scss">
.user-homepage {
  .user-meta {
    align-items: center;
    display: flex;

    & > * + * {
      margin-left: 1rem;
    }

    .avatar {
      border-radius: .5rem;
      height: 4rem;
      width: 4rem;
    }
  }
}
</style>
