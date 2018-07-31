// api 路由
const routes = {
  currentUser: '/current-user',
  getUser: '/user',
  getUserDetail: '/user/detail',
  login: '/login',
  logout: '/logout',
  register: '/register',
  getTopics: '/topic/',
  getSingleTopic: '/topic',
}

Object.keys(routes).forEach((k) => {
  routes[k] = `/api${routes[k]}`
})

export default routes
