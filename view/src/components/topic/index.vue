<template>
  <div class="topic-index flex">
    <div class="topics">
      <transition-group name="fade-slide-u" mode="out-in">
        <topic-intro-card
          v-for="(t, index) in topics"
          :key="index"
          :topic="t"
        />
      </transition-group>
    </div>
    <div class="aside gutter--8px">
      <el-card class="user-card" :body-style="{ padding: '0' }">
        <div class="user-avatar">
          <img src="/static/img/avatar.png">
        </div>
        <el-row class="user-info">
          <el-col :span="8" class="flex flex-column tc">
            <span class="user-info-header">创建</span>
            <span class="user-info-body">0</span>
          </el-col>
          <el-col :span="8" class="flex flex-column tc">
            <span class="user-info-header">参与</span>
            <span class="user-info-body">0</span>
          </el-col>
          <el-col :span="8" class="flex flex-column tc">
            <span class="user-info-header">关注者</span>
            <span class="user-info-body">0</span>
          </el-col>
        </el-row>
      </el-card>
      <el-card class="">
        <div slot="header">话题分类</div>
      </el-card>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapMutations } from 'vuex'
import { Card, Row, Col } from 'element-ui'
import TopicIntroCard from '@/components/card/topic/intro'
import { copyProps, normalizeTimestamp } from '../../utils'

Vue.use(Card)
Vue.use(Row)
Vue.use(Col)

export default {
  name: 'TopicIndex',

  components: {
    TopicIntroCard,
  },

  data() {
    return {
      topics: [],
    }
  },

  methods: {
    getData() {
      this.$http.get(this.$apiRoutes.getTopics).then((res) => {
        let data = res.data.map((item) => {
          // 提取话题数据，通过复制处理
          let t = copyProps(item, [
            'id',
            'content',
            'title',
            'views',
            { from: 'user_id', to: 'userId' },
            { from: 'created_time', to: 'createdTime', handler: normalizeTimestamp },
            { from: 'updated_time', to: 'updatedTime', handler: normalizeTimestamp },
          ])
          t.shown = false
          return t
        })

        this.topics = data
      })
    },

    ...mapMutations([
      'clearUsers',
    ]),
  },

  mounted() {
    // 每次刷新页面时把缓存的用户数据清除
    this.clearUsers()
    this.getData()
  },
}
</script>

<style lang="scss">
.topic-index {
  .topics {
    flex-grow: 1;
  }
}

.aside {
  width: 250px;
  flex: 0 0 250px;

  & > * {
    * + & {
      margin-bottom: .5rem;
    }
  }

  .user-card {
    .user-avatar {
      display: flex;
      margin: 2rem 0;
      img {
        border-radius: 1rem;
        height: 5rem;
        margin: auto;
      }
    }

    .user-info {
      background-color: $color-light;
      padding: .75rem;

      & > * {
        cursor: pointer;
      }

      .user-info-header {
        color: $color-gray6;
        font-size: 14px;
      }
    }
  }
}
</style>
