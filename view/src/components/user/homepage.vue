<template>
  <div class="user-homepage">
    <el-card class="shadow-2dp">
      <div class="user-meta">
        <img class="avatar" :src="user.avatar">
        <div>{{ user.username }}</div>
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
  </div>
</template>

<script>
import Vue from 'vue'
import { Card } from 'element-ui'
import { getUserDetail } from '@/http/requests'

Vue.use(Card)

export default {
  name: 'UserHomepage',

  data() {
    return {
      user: {},
    }
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

    .avatar {
      border-radius: .5rem;
      margin-right: 1.5rem;
      height: 4rem;
      width: 4rem;
    }
  }
}
</style>
