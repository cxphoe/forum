<template>
  <el-card
    class="mb2 br1 bg-white shadow--2dp topic-intro-card"
  >
    <div slot="header" class="f2 topic-meta">
      <div class="flex items-center">
        <router-link
          :to="{ name: 'userHomepage', params: { id: topic.user.id } }"
          class="link"
        >
          <img class="avatar mr3" :src="topic.user.avatar">
        </router-link>
        <div class="flex flex-column">
          <router-link
            :to="{ name: 'userHomepage', params: { id: topic.user.id } }"
            class="link"
          >
            <span class="f3 mb fw6">{{ topic.user.username }}</span>
          </router-link>
          <span class="lh-solid mb1 gray6">{{ topic.updatedTime | dateFormat }}</span>
        </div>
      </div>
      <div class="flex items-center">
        <div class="topic-board-tag">{{ topic.boardName }}</div>
        <topic-operation
          v-if="topic.user.id === currentUser.id"
          :topic-id="topic.id"
          class="ml3"
        />
      </div>
    </div>
    <div class="topic-intro" @click="showTopicDetail">
      <div v-if="firstImg" class="img-wrapper">
        <img :src="firstImg">
      </div>
      <div class="topic-info">
        <h3 class="f4 fw6">{{ topic.title }}</h3>
        <div class="topic-content" :style="{ height: firstImg ? '6rem' : '3rem' }">{{ topic.content }}</div>
      </div>
    </div>
    <div class="mt2 f2 gray5">
      <span class="mr3">
        <i class="fas fa-eye"></i>
        <span class="ml1">{{ topic.views }} 次浏览</span>
      </span>
      <span>
        <i class="fas fa-comments"></i>
        <span class="ml1">{{ topic.replyCount }} 条评论</span>
      </span>
    </div>
  </el-card>
</template>

<script>
import Vue from 'vue'
import { mapState, mapMutations } from 'vuex'
import { Card } from 'element-ui'
import { dateFormat } from '@/utils'
import { baseUrl } from '@/config'
import TopicOperation from './operation'

Vue.use(Card)

export default {
  name: 'TopicIntroCard',

  components: {
    TopicOperation,
  },

  props: {
    topic: {},
  },

  data() {
    return {
      firstImg: null,
    }
  },

  computed: {
    ...mapState([
      'currentUser',
    ]),
  },

  filters: {
    dateFormat,
  },

  methods: {
    getFirstImgSrc() {
      let reg = /^<img src="(.*)">$/m
      let match = reg.exec(this.topic.content)
      if (match) {
        this.firstImg = baseUrl + match[1]
      }
    },

    showTopicDetail() {
      this.$router.push({
        name: 'topicDetail',
        params: { id: this.topic.id },
      })
    },

    ...mapMutations([
      'setUser',
    ]),
  },

  created() {
    this.getFirstImgSrc()
  },
}
</script>

<style lang="scss">
.topic-intro-card {
  .el-card__header {
    border: none;
    padding-bottom: 0;
  }

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
    cursor: pointer;
    display: flex;
    user-select: none;

    .topic-info {
      h3 {
        line-height: 1.5rem;
      }

      &:hover {
        h3 {
          color: #2a64ac;
        }
      }
    }

    .topic-content {
      overflow: hidden;
      flex-grow: 1;
    }

    .img-wrapper {
      border-radius: 5px;
      height: 8rem;
      overflow: hidden;
      position: relative;
      flex: 0 0 11rem;
      img {
        height: 100%;
        left: 50%;
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
      }
    }

    & > * {
      & + * {
        margin-left: 1rem;
      }
    }
  }
}
</style>
