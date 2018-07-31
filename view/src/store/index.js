import Vue from 'vue'
import Vuex from 'vuex'
import http from '@/http'
import routes from '@/http/routes'
import { isOk } from '@/utils'
import { baseUrl } from '@/config'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: {},
    users: {},
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
          }
          commit('setCurrentUser', { user })
        }
      })
    },

    getUser({ commit }, payload) {
      let { id } = payload
      http.get(`${routes.getUser}/${id}`).then((res) => {
        if (isOk(res.status)) {
          let user = res.data
          user.avatar = `${baseUrl}${user.avatar}`
          commit('setUser', {
            id,
            user,
          })
        }
      })
    },
  },
})
