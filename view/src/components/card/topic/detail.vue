<template>
  <div>
    <el-card
      class="mb2 br1 bg-white shadow--2dp topic-intro-card"
      :body-style="{ padding: 0 }"
    >
      <div class="f2 topic-detail-header">
        <div class="flex items-center">
          <router-link
            :to="{ name: 'userHomepage', params: { id: topic.user.id || -1 } }"
            class="link"
          >
            <img class="avatar mr3" :src="topic.user.avatar">
            <span class="f3 mb fw6">{{ topic.user.username }}</span>
          </router-link>
        </div>
        <div class="lh-solid mb1 gray6 f3 flex items-center">
          <div class="mr3">编辑于 {{ topic.updatedTime | dateFormat }}</div>
          <topic-operation v-if="currentUser.id === topic.id" :topic-id="topic.id" />
        </div>
      </div>
      <div class="topic-detail-body">
        <div class="topic-content markdown-body" v-html="formattedContent"></div>
        <div class="flex mt2">
          <div class="topic-board-tag ml-auto">编程</div>
        </div>
      </div>
      <div ref="footer" class="topic-detail-footer">
        <div ref="re-wrapper" class="re-wrapper">
          <reply-editor
            v-if="topic.id" ref="replyEditor"
            :topic-id="topic.id" @post="getReplys"
          />
        </div>
        <div class="replys">
          <div class="mb2">{{ replys.length }} 条回复</div>
          <reply-card
            v-for="r in replys"
            :key=r.id
            :reply="r"
            @delete="getReplys"
          ></reply-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import { Card } from 'element-ui'
import ReplyEditor from '@/components/editor/reply_editor'
import TopicOperation from './operation'
import ReplyCard from '../reply'
import marked from 'marked'
import {
  isOk,
  copyProps,
  dateFormat,
  normalizeTimestamp,
  addBaseUrl,
} from '@/utils'
import { baseUrl } from '@/config'

Vue.use(Card)

export default {
  name: 'TopicDetailCard',

  components: {
    ReplyCard,
    ReplyEditor,
    TopicOperation,
  },

  data() {
    return {
      topic: {
        user: {},
      },
      replys: [],
    }
  },

  computed: {
    /**
     * 为数据库存储的内容字符串中的 img 加上 baseUrl
     */
    formattedContent() {
      let c = this.topic.content || ''
      let imgReg = /<img src="(.*)">/ig
      let match = imgReg.exec(c)
      while (match) {
        c = c.replace(match[0], `<div><img src="${baseUrl + match[1]}"></div>`)
        match = imgReg.exec(c)
      }
      return marked(c)
    },

    ...mapState([
      'currentUser',
    ]),
  },

  filters: {
    dateFormat,
  },

  methods: {
    getData(id) {
      this.$http.get(`${this.$apiRoutes.getSingleTopic}/${id}`).then((res) => {
        this.topic = copyProps(res.data, [
          'id',
          'content',
          'title',
          'views',
          { from: 'user', to: 'user', handler: addBaseUrl(baseUrl, ['avatar']) },
          { from: 'created_time', to: 'createdTime', handler: normalizeTimestamp },
          { from: 'updated_time', to: 'updatedTime', handler: normalizeTimestamp },
        ])
      })
    },

    getReplys(id) {
      id = id || this.topic.id
      let url = this.$apiRoutes.getReplys
      this.$http.get(url, {
        params: { 'topic_id': id },
      }).then((res) => {
        if (isOk(res.status)) {
          this.replys = res.data.map((r) => {
            let result = copyProps(r, [
              'id',
              'content',
              { from: 'user', to: 'user', handler: addBaseUrl(baseUrl, ['avatar']) },
              { from: 'created_time', to: 'createdTime', handler: normalizeTimestamp },
            ])
            return result
          }).sort((self, other) => other.createdTime - self.createdTime)
        }
      })
    },

    handleScroll() {
      let f = this.$refs.footer
      let re = this.$refs['re-wrapper']
      console.log(f.offsetTop, window.scrollY + window.innerHeight)
      if (f.offsetTop <= window.scrollY + window.innerHeight) {
        re.classList.remove('fix')
      } else {
        re.classList.add('fix')
      }
    },
  },

  created() {
    let id = this.$route.params.id
    this.getData(id)
    this.getReplys(id)
    window.addEventListener('scroll', () => {
      this.handleScroll()
    })
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
    background-color: $color-gray1;
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
    padding-top: 0 !important;
    position: relative;

    .replys {
      margin-top: 1.5rem;
    }

    .re-wrapper {
      width: 100%;;

      &.fix {
        bottom: 0;
        left: 0;
        margin: auto;
        position: fixed;

        .reply-editor {
          width: 1000px;
          margin: auto;
        }
      }
    }
  }

  .topic-detail-header, .topic-detail-body, .topic-detail-footer {
    padding: 1.5rem;
  }

  .topic-content {
    img {
      left: 2.5%;
      position: relative;
      width: 95%;
    }
  }
}
</style>
