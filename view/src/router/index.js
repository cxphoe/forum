import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Nav = () => import(/* webpackChunkName: "nav" */ '@/components/nav')
const TopicIndex = () => import(/* webpackChunkName: "topicindex" */ '@/components/topic/index')
const TopicEdit = () => import(/* webpackChunkName: "topicedit" */ '@/components/topic/edit')
const TopicDetail = () => import(/* webpackChunkName: "topicdetail" */ '@/components/card/topic/detail')
const Login = () => import(/* webpackChunkName: "login" */ '@/components/login')
const UserHomepage = () => import(/* webpackChunkName: "userhomepage" */ '@/components/user/homepage')
const UserSetting = () => import(/* webpackChunkName: "usersetting" */ '@/components/user/setting')

const indexRoutes = [
  {
    path: '/',
    redirect: '/topic',
  },
  {
    name: 'login',
    path: '/login',
    component: Login,
  },
]

const userRoutes = [
  {
    name: 'userHomepage',
    path: '/user/:id',
    components: {
      default: UserHomepage,
      nav: Nav,
    },
  },
  {
    name: 'userSetting',
    path: '/user/setting/:id',
    components: {
      default: UserSetting,
      nav: Nav,
    },
  },
]

const topicRoutes = [
  {
    name: 'topicIndex',
    path: '/topic',
    components: {
      default: TopicIndex,
      nav: Nav,
    },
  },
  {
    name: 'topicEdit',
    path: '/topic/edit',
    component: TopicEdit,
  },
  {
    name: 'topicDetail',
    path: '/topic/:id',
    components: {
      default: TopicDetail,
      nav: Nav,
    },
  }
]

export default new Router({
  mode: 'history',
  routes: [
    ...indexRoutes,
    ...userRoutes,
    ...topicRoutes,
  ],
})
