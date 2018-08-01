import http from './index'
import routes from './routes'
import { isOk } from '@/utils'
import { baseUrl } from '@/config'

const _getUser = function (url, resolve = () => {}, reject = () => {}) {
  http.get(url)
    .then((res) => {
      if (isOk(res.status)) {
        let user = res.data
        user.avatar = baseUrl + user.avatar
        resolve(user)
      } else {
        reject(res)
      }
    })
    .catch((err) => reject(err))
}

const getUser = function (id, resolve, reject) {
  let url = `${routes.getUser}/${id}`
  _getUser(url, resolve, reject)
}

const getUserDetail = function (id, resolve, reject) {
  let url = `${routes.getUserDetail}/${id}`
  _getUser(url, resolve, reject)
}

export {
  getUser,
  getUserDetail,
}
