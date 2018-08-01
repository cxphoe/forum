import Vue from 'vue'
import Vuex from 'vuex'
import http from '@/http'
import routes from '@/http/routes'
import { isOk } from '@/utils'
import { baseUrl } from '@/config'
import { getUser } from '@/http/requests'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: {},
    users: {},
    token: null,
  },

  mutations: {
    setCurrentUser(state, payload) {
      let { user } = payload
      state.currentUser = user
    },

    setUser(state, payload) {
      let { id, user } = payload
      state.users[id] = user
    },

    clearUsers(state) {
      state.users = []
    },

    setToken(state, { token }) {
      state.token = token
    },
  },

  actions: {
    getCurrentUser({ commit }) {
      http.get(routes.currentUser).then((res) => {
        if (isOk(res.status)) {
          // 如果没有返回用户数据，说明当前没有 cookie 或 cookie 已过期
          // 直接返回一个空对象
          let user = res.data || null
          if (res.data) {
            user.avatar = `${baseUrl}${user.avatar}`
            // 设置获得的 xsrf token
            commit('setToken', { token: res.headers.token })
          }
          commit('setCurrentUser', { user })
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
