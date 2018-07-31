import axios from 'axios'
import { log } from '@/utils'
// import { baseUrl } from '@/config'

// axios.defaults.baseURL = baseUrl

// 添加一个请求拦截器
axios.interceptors.request.use(function (config) {
  // Do something before request is sent
  // 跨域请求带凭证
  config.withCredentials = true
  config.validateStatus = function (status) {
    return status < 500 // 状态码在大于或等于500时才会 reject
  }

  log('request config:', config)
  return config
}, function (error) {
  // Do something with request error
  log('request error:', error)
  return Promise.reject(error)
})

// 添加一个响应拦截器
axios.interceptors.response.use(function (response) {
  // Do something with response data
  log('response:', response)
  return response
}, function (error) {
  // Do something with response error
  log('response error:', error)
  return Promise.reject(error)
})

export default axios
