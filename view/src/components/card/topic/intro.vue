<template>
  <el-card
    class="mb2 br1 bg-white shadow--2dp topic-intro-card"
  >
    <div slot="header" class="f2 topic-meta">
      <div class="flex items-center">
        <img class="avatar mr3" src="/static/img/avatar.png">
        <div class="flex flex-column">
          <span class="f3 mb fw6">{{ topic.username || '' }}</span>
          <span class="lh-solid mb1 gray6">{{ topic.updatedTime | dateFormat }}</span>
        </div>
      </div>
      <div class="topic-board-tag">编程</div>
    </div>
    <div class="topic-intro">
      <div v-if="firstImg">
        <img :src="'http://localhost:2000' + firstImg">
      </div>
      <div class="topic-info" @click="showTopicDetail">
        <h3 class="f4 fw6">{{ topic.title }}</h3>
        <div class="topic-content" :style="{ height: firstImg ? '6rem' : '3rem' }">{{ topic.content }}</div>
      </div>
    </div>
  </el-card>
</template>

<script>
import Vue from 'vue'
import { Card } from 'element-ui'
import { dateFormat } from '@/utils'

Vue.use(Card)

export default {
  name: 'TopicIntroCard',

  props: {
    topic: {},
  },

  data() {
    return {
      firstImg: null,
    }
  },

  computed: {
    user() {
      let { userId } = this.topic
      return this.$store.state.users[userId]
    },
  },

  filters: {
    dateFormat,
  },

  methods: {
    getUser() {
      this.$store.dispatch('getUser', { id: this.topic.userId })
    },

    getFirstImgSrc() {
      let reg = /^<img src="(.*)">$/m
      let match = reg.exec(this.topic.content)
      if (match) {
        this.firstImg = match[1]
      }
    },

    showTopicDetail() {
      this.$router.push({
        name: 'topicDetail',
        params: { id: this.topic.id },
      })
    },
  },

  created() {
    this.getUser()
    this.getFirstImgSrc()
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

  .topic-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .topic-intro {
    display: flex;

    .topic-info {
      cursor: pointer;
      user-select: none;

      &:hover {
        h3 {
          color: #2a64ac;
        }
      }
    }

    .topic-content {
      overflow: hidden;
    }

    img {
      border-radius: 5px;
      width: 8rem;
    }

    & > * {
      & + * {
        margin-left: 1rem;
      }
    }
  }
}
</style>
