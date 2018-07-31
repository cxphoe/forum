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
        <el-button class="mr5" type="primary" @click="pulish">发表</el-button>
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
import { Button } from 'element-ui'
import TopicEditor from '../editor/topic_editor'

Vue.use(Button)

export default {
  name: 'TopicEdit',

  components: {
    TopicEditor,
  },

  data() {
    return {
      data: {
        title: '测试',
        content: [{ type: 'text', data: 'testing...' }],
      },
      imgs: {},
    }
  },

  methods: {
    copy(o) {
      return JSON.parse(JSON.stringify(o))
    },
    pulish() {
      console.log(this.copy(this.data), this.copy(this.imgs))
      let form = new FormData()
      form.append('data', JSON.stringify(this.data))
      Object.values(this.imgs).forEach((img) => {
        let { name, file } = img
        form.append(name, file)
      })

      this.$http.post('/topic/add', form).then((res) => {
        console.log(res)
      }).catch((err) => {
        console.error(err)
      })
    },
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
