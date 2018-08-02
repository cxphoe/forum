import Vue from 'vue'
import Vuex from 'vuex'
import http from '@/http'
import routes from '@/http/routes'
import { isOk } from '@/utils'
import { baseUrl } from '@/config'
import { getUser } from '@/http/requests'
import { copyProps } from '../utils'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: {},
    messages: [],
    isGuest: true,
    users: [],
    token: null,
  },

  mutations: {
    setCurrentUser(state, payload) {
      let { user } = payload
      console.log(user)
      state.currentUser = user
      state.isGuest = !!user.is_guest
    },

    clearCurrentUser(state) {
      state.currentUser = {}
    },

    setMessages(state, { messages }) {
      state.messages = messages
    },

    setUser(state, payload) {
      let { id, user } = payload
      state.users[id] = user
    },

    setGuest(state, { user }) {
      state.guest = user
    },

    clearUsers(state) {
      state.users = []
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

    getUser({ commit }, payload) {
      let { id } = payload
      getUser(id, (user) => {
        commit('setUser', { id, user })
      })
    },
  },
})
