<template>
  <div>
    <router-link
      :to="{ name: 'topicEdit', query: { topicId, mode: 'modify' } }"
      ref="toEditor"
      hidden
    />
    <el-button size="small" type="primary" @click="editTopic">编辑</el-button>
    <el-button size="small" type="danger" @click="deleteTopic">删除</el-button>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Button, Message } from 'element-ui'
import { isOk } from '@/utils'

Vue.use(Button)

const notifySuccess = function (msg) {
  Message.success(msg)
}

const notifyFail = function (msg) {
  Message.error(msg)
}

export default {
  name: 'TopicOperation',

  props: {
    topicId: Number,
  },

  computed: {
    ...mapState([
      'token'
    ]),
  },

  methods: {
    deleteTopic() {
      let url = `${this.$apiRoutes.deleteTopic}/${this.topicId}`
      this.$http.get(url, {
        params: { token: this.token || '' },
      }).then((res) => {
        if (isOk(res.status)) {
          notifySuccess('删除成功')
        } else {
          notifyFail('删除失败')
        }
      }).catch(() => notifyFail('服务器出错'))
    },

    editTopic() {
      this.$refs.toEditor.$el.click()
    },
  },
}
</script>

<style lang="scss">

</style>
