<template>
  <div>
    <el-card
      class="mb2 br1 bg-white shadow--2dp topic-intro-card"
      :body-style="{ padding: 0 }"
    >
      <div class="f2 topic-detail-header">
        <div class="flex items-center">
          <img class="avatar mr3" :src="user.avatar">
          <div class="f3 mb fw6">{{ user.username }}</div>
        </div>
        <div class="lh-solid mb1 gray6">编辑于 {{ topic.updatedTime | dateFormat }}</div>
      </div>
      <div class="topic-detail-body">
        <div class="topic-content" v-html="markedContent"></div>
        <div class="flex">
          <div class="topic-board-tag ml-auto">编程</div>
        </div>
      </div>
      <div class="topic-detail-footer">comment</div>
    </el-card>
  </div>
</template>

<script>
import Vue from 'vue'
import { Card } from 'element-ui'
import marked from 'marked'
import {
  isOk,
  copyProps,
  dateFormat,
  normalizeTimestamp,
} from '@/utils'
import { baseUrl } from '@/config'

Vue.use(Card)

export default {
  name: 'TopicDetailCard',

  data() {
    return {
      topic: {},
      user: {},
    }
  },

  computed: {
    markedContent() {
      return marked(this.topic.content || '')
    },
  },

  filters: {
    dateFormat,
  },

  methods: {
    getData(id) {
      this.$http.get(`${this.$apiRoutes.getSingleTopic}/${id}`).then((res) => {
        this.getUser(res.data['user_id'])

        this.topic = copyProps(res.data, [
          'content',
          'title',
          'views',
          { from: 'user_id', to: 'userId' },
          { from: 'created_time', to: 'createdTime', handler: normalizeTimestamp },
          { from: 'updated_time', to: 'updatedTime', handler: normalizeTimestamp },
        ])
      })
    },

    getUser(id) {
      let url = `${this.$apiRoutes.getUser}/${id}`
      this.$http.get(url).then((res) => {
        if (isOk(res.status)) {
          let user = res.data
          user.avatar = `${baseUrl}${user.avatar}`
          this.user = user
        }
      })
    },
  },

  created() {
    let id = this.$route.params.id
    this.getData(id)
  },
}
</script>

<style lang="scss">
.topic-intro-card {
  .topic-board-tag {
    border: 1px solid $color-first;
    border-radius: 1rem;
    color: $color-first;
    padding: .25rem .5rem;
    line-height: 1;
  }

  .topic-detail-header {
    background-color: $color-light;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .avatar {
      width: 2.5rem;
      height: 2.5rem;
    }
  }

  .topic-detail-footer {
    border-top: 1px solid #ddd;
  }

  .topic-detail-header, .topic-detail-body, .topic-detail-footer {
    padding: 1.25rem;
  }
}
</style>
