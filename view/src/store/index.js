import Vue from 'vue'
import Vuex from 'vuex'
import http from '@/http'
import routes from '@/http/routes'
import { isOk } from '@/utils'
import { baseUrl } from '@/config'
import { copyProps } from '../utils'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: {},
    messages: [],
    isGuest: true,
    token: null,
  },

  mutations: {
    setCurrentUser(state, payload) {
      let { user } = payload
      state.currentUser = user
      state.isGuest = !!user.is_guest
    },

    clearCurrentUser(state) {
      state.currentUser = {}
    },

    setMessages(state, { messages }) {
      state.messages = messages
    },

    setGuest(state, { user }) {
      state.guest = user
    },

    setToken(state, { token }) {
      state.token = token
    },
  },

  actions: {
    getCurrentUser({ commit, dispatch }) {
      http.get(routes.currentUser).then((res) => {
        if (isOk(res.status)) {
          // 会接受到表示用户的数据 或者 游客数据
          let user = copyProps(res.data, [
            'id',
            'avatar',
            'username',
            'is_guest',
            'follower_count',
            { from: 'followed_ids', to: 'followedIds' },
            { from: 'topic_count', to: 'topicCount' },
            { from: 'involved_count', to: 'involvedCount' },
          ])
          user.avatar = `${baseUrl}${user.avatar}`
          // 设置获得的 xsrf token
          let t = res.headers.token
          t && commit('setToken', { token: t })

          // 得到 token 之后，再获取 私信/信息
          dispatch('getMessages', { token: t })
          commit('setCurrentUser', { user })
        }
      })
    },

    getMessages({ commit }, { token }) {
      http.get(routes.getMessages, {
        params: { token },
      }).then((res) => {
        if (isOk(res.status)) {
          let ms = res.data
          ms.forEach((m) => {
            m.avatar = baseUrl + m.avatar
          })
          commit('setMessages', { messages: ms })
        }
      })
    },
  },
})
