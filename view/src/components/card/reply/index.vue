<template>
  <el-card>
    <div class="flex items-center justify-sb">
      <div class="flex items-center mb2">
        <router-link
          :to="{ name: 'userHomepage', params: { id: reply.user.id } }"
          class="link"
        >
          <img class="avatar mr3" :src="reply.user.avatar">
          <span class="mr3">{{ reply.user.username }}</span>
        </router-link>
        <div class="gray5">{{ reply.createdTime | dateFormat }}</div>
      </div>
      <div v-if="currentUser.id === reply.user.id">
        <el-button type="danger" size="small" @click="deleteReply">删除</el-button>
      </div>
    </div>
    <div class="">{{ reply.content }}</div>
  </el-card>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Card, Button, Message } from 'element-ui'
import { isOk, dateFormat } from '@/utils'

Vue.use(Card)
Vue.use(Button)

export default {
  name: 'ReplyCard',

  props: {
    reply: {},
  },

  computed: mapState([
    'currentUser',
    'token',
  ]),

  filters: {
    dateFormat,
  },

  methods: {
    deleteReply() {
      let url = `${this.$apiRoutes.deleteReply}/${this.reply.id}`
      this.$http.get(url, {
        params: { token: this.token },
      }).then((res) => {
        if (isOk(res.status)) {
          Message.success('删除成功')
          this.$emit('delete')
        } else {
          Message.error('删除失败')
        }
      }).catch(() => Message.error('服务器出错'))
    },
  },
}
</script>

<style lang="scss">

</style>
