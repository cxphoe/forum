<template>
  <el-card
    class="mb2 br1 bg-white shadow--2dp topic-intro-card"
  >
    <div slot="header" class="f2 topic-meta">
      <div class="flex items-center">
        <img class="avatar mr3" :src="user.avatar">
        <div class="flex flex-column">
          <span class="f3 mb fw6">{{ user.username }}</span>
          <span class="lh-solid mb1 gray6">{{ topic.updatedTime | dateFormat }}</span>
        </div>
      </div>
      <div class="flex items-center">
        <div class="topic-board-tag">编程</div>
        <topic-operation
          v-if="topic.userId === currentUser.id"
          :topic-id="topic.id"
          class="ml3"
        />
      </div>
    </div>
    <div class="topic-intro">
      <div v-if="firstImg">
        <img :src="firstImg">
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
import { mapState, mapMutations } from 'vuex'
import { Card } from 'element-ui'
import { dateFormat } from '@/utils'
import { baseUrl } from '@/config'
import { getUser } from '@/http/requests'
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
      user: {},
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
    getUser() {
      let id = this.topic.userId
      let u = this.$store.state.users[id]
      if (u) {
        this.user = u
      } else {
        this.user = {}
        getUser(id, (user) => {
          this.user = user
          this.setUser({ id, user })
        })
      }
    },

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
