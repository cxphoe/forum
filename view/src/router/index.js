import Vue from 'vue'
import Router from 'vue-router'
import Nav from '@/components/nav'
import TopicIndex from '@/components/topic/index'
import TopicEdit from '@/components/topic/edit'
import TopicDetail from '@/components/card/topic/detail'
import Login from '@/components/login'
import UserHomepage from '@/components/user/homepage'
import UserSetting from '@/components/user/setting'

Vue.use(Router)

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
