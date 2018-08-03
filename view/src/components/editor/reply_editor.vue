<template>
  <div class="reply-editor shadow--2dp">
    <div v-show="focus" class="flex items-center mb2 justify-sb">
      <div>回复</div>
      <el-button
        type="primary" size="small"
        @click="postReply"
      >回复</el-button>
    </div>
    <el-input
      @focus="focus = true"
      type="textarea" :rows="3"
      placeholder="请输入内容" v-model="content"
    />
  </div>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Button, Input, Message } from 'element-ui'
import { isOk } from '@/utils'

Vue.use(Button)
Vue.use(Input)

export default {
  name: 'ReplyEditor',

  props: {
    topicId: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      content: '',
      focus: false,
    }
  },

  computed: {
    ...mapState([
      'token',
    ]),
  },

  methods: {
    postReply() {
      let form = new FormData()
      for (let [prop, data] of [
        ['content', this.content],
        ['topic_id', this.topicId],
      ]) {
        form.append(prop, data)
      }

      let url = this.$apiRoutes.addReply
      this.$http.post(url, form, {
        params: { token: this.token }
      }).then((res) => {
        if (isOk(res.status)) {
          Message.success('回复成功')
          this.$emit('post')
        } else {
          Message.error('回复失败')
        }
      })
    },
  },

  created() {
    window.addEventListener('click', (event) => {
      let t = event.target
      while (t !== document.body && t !== this.$el) {
        t = t.parentNode
      }
      if (t !== this.$el) {
        this.focus = false
      }
    })
  },
}
</script>

<style lang="scss">
.reply-editor {
  background: #fff;
  border: 1px solid #ddd;
  padding: 1rem;
}
</style>
