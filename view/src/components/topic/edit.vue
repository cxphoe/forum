<template>
  <div class="topic-edit-wrapper">
    <header class="topic-edit-header">
      <div class="logo">
        <img src="/static/img/logo.png">
      </div>
      <div class="status-wrapper">
        <div class="status">
          <span>发表话题</span>
        </div>
      </div>
      <div class="operation">
        <el-button class="mr5" type="primary" @click="submit">{{ action }}</el-button>
      </div>
    </header>
    <main class="topic-edit-main">
      <topic-editor
        class="topic-editor"
        :form-data="data"
        :imgs="imgs"
      ></topic-editor>
    </main>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Button, Notification } from 'element-ui'
import { copyProps, isOk } from '@/utils'
import { baseUrl } from '@/config'
import TopicEditor from '../editor/topic_editor'

Vue.use(Button)

export default {
  name: 'TopicEdit',

  components: {
    TopicEditor,
  },

  data() {
    return {
      topic: {
        title: '',
        content: '',
      },
      mode: null,
      data: {},
      imgs: {},
    }
  },

  computed: {
    action() {
      return this.mode === 'pulish' ? '发表' : '修改'
    },

    ...mapState([
      'currentUser',
      'token',
    ]),
  },

  methods: {
    copy(o) {
      return JSON.parse(JSON.stringify(o))
    },
    processTopic() {
      const decomposeContent = function (c) {
        if (!c) {
          return []
        }
        let parts = []
        let imgReg = /<img src="(.*)">/
        for (let piece of c.split('\n')) {
          // 处理含有 img 标签的文本
          let match = imgReg.exec(piece)
          if (match) {
            piece = piece.replace(match[0], `<img src="${baseUrl + match[1]}">`)
          }

          parts.push({
            type: 'text',
            data: piece,
          })
        }
        return parts
      }
      this.data = copyProps(this.topic, [
        'title',
        { from: 'content', to: 'content', handler: decomposeContent },
      ])
    },

    submit() {
      console.log('pulish:', this.copy(this.data), this.copy(this.imgs), Object.keys(this.imgs))
      let form = new FormData()
      form.append('data', JSON.stringify(this.data))
      form.append('user_id', this.currentUser.id)
      for (let key in this.imgs) {
        let { name, file } = this.imgs[key]
        console.log(`append file <${name}>`)
        form.append(name, file)
      }

      let url = this.mode === 'pulish'
        ? this.$apiRoutes.addTopic
        : `${this.$apiRoutes.updateTopic}/${this.topic.id}?token=${this.token || ''}`

      this.$http.post(url, form).then((res) => {
        if (isOk(res.status)) {
          Notification({
            title: `${this.action}成功`,
            type: 'success',
          })
        } else {
          Notification({
            title: `${this.action}失败`,
            type: 'error',
          })
        }
      }).catch(() => {
        Notification({
          title: '服务器出错',
          type: 'error',
        })
      })
    },

    getData() {
      let { mode, topicId } = this.$route.query
      this.mode = mode || 'pulish'
      if (topicId) {
        let url = `${this.$apiRoutes.getSingleTopic}/${topicId}`
        this.$http.get(url).then((res) => {
          if (isOk(res.status)) {
            this.topic = copyProps(res.data, [
              'id',
              'content',
              'title',
            ])
            this.processTopic()
          }
        })
      } else {
        this.processTopic()
      }
    },
  },

  created() {
    this.getData()
  },
}
</script>

<style lang="scss">
.topic-edit-wrapper {
  background-color: #fff;
  margin: 0 !important;
  max-width: 2000px !important;
  min-height: 1000px;
  padding-top: 6rem !important;

  .topic-edit-header {
    align-items: center;
    background-color: #fff;
    border-bottom: 1px solid #eee;
    display: flex;
    height: 3.5rem;
    justify-content: space-between;
    left: 0;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;

    .logo {
      left: 0;
      top: 0;

      img {
        margin: 0 1rem;
        width: 40px;
      }
    }

    .operation {
      top: 0;
      right: 2rem;
    }

    .logo, .operation {
      align-items: center;
      display: flex;
      position: absolute;
      height: 3.5rem;
    }

    .status-wrapper {
      width: 100%;

      .status {
        margin: auto;
        width: 700px;
      }
    }
  }

  .topic-editor {
    margin: auto;
    max-width: 700px;
    width: 100%;
  }
}
</style>
