// api 路由
const routes = {
  currentUser: '/current-user',
  updateUser: '/user/update',
  getUser: '/user',
  getUserDetail: '/user/detail',
  login: '/login',
  logout: '/logout',
  register: '/register',
  getTopics: '/topic/',
  getSingleTopic: '/topic',
  addTopic: '/topic/add',
  deleteTopic: '/topic/delete',
  updateTopic: '/topic/update',
  getReplys: '/reply/',
  addReply: '/reply/add',
  deleteReply: '/reply/delete',
  getMessages: '/message/',
  getBoards: '/board/',
  getBoardTopics: '/board/topics',
  addFollow: '/follow/add',
  deleteFollow: '/follow/delete',
  getFollowers: '/follow/followers',
  getFollowedUsers: '/follow/followed_users',
}

export default routes
