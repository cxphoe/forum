/**
 * 用于 develop log
 * @param {*} args log 参数，直接传给 console.log
 */
const log = function (...args) {
  let now = new Date()
  console.log(now.toLocaleString(), ...args)
}

const isOk = function (status) {
  status = Number(status)
  return status >= 200 && status < 304
}

/**
 * 根据时间戳返回时间格式
 */
const dateFormat = function (timestamp) {
  let date = new Date(timestamp)
  let year = date.getFullYear()
  let month = date.getMonth() + 1
  let day = date.getDate()
  return `${month}月 ${day < 10 ? '0' + day : day}, ${year}`
}

/**
 * 根据给定的属性，在对象中（浅）复制一个新对象
 * @param {*} source 复制的源对象
 * @param {[String | {from: String, to: String, handler: Function}]} props 要复制的属性：是字符串或一个设置复制对象
 * @param {*} target 复制的目标对象
 */
const copyProps = function (source, props, target) {
  target = target || {}
  for (let p of props) {
    if (typeof p === 'string') {
      // 是字符串就直接按照给定的 prop 进行浅复制
      target[p] = source[p]
    } else {
      // 根据给定的设置 target[to] = handler(srouce[from])
      let { from, to, handler } = p
      target[to] = typeof handler === 'function'
        ? handler(source[from])
        : source[from]
    }
  }
  return target
}

const getFilename = function (name) {
  let dotIndex = name.lastIndexOf('.')
  if (dotIndex > -1) {
    name = name.slice(0, dotIndex)
  }
  return name
}

/**
 * 格式化时间戳
 */
const normalizeTimestamp = (ts) => {
  ts = ts.toString()
  if (ts.length > 13) {
    ts = ts.split('').slice(0, 13).join('')
  } else {
    ts = ts.padEnd(13, '0')
  }
  return Number(ts)
}

/**
 * 将对象的所有属性设置为给定的值
 * @param {*} obj 要清除的对象
 * @param {*} value 清除时设置的值
 */
const clearObj = function (obj, value = '') {
  for (let key in obj) {
    obj[key] = value
  }
}

/**
 * 把对象的属性值构建成一个表格数据，并返回
 * @param {*} obj 数据的来源对象
 * @param { [String] } props 从对象提取的属性，当没有传入值时，默认是提取对象的所有属性
 * @param { FormData } form 提取属性之后存储的地方，当没有传入值时，默认创建一个新的表格数据
 * @returns { FormData }
 */
const buildFormdata = function (obj, props, form) {
  props = props || Object.keys(obj)
  form = form || new FormData()
  for (let p of props) {
    form.append(p, obj[p])
  }
  return form
}

export {
  log,
  isOk,
  dateFormat,
  copyProps,
  getFilename,
  normalizeTimestamp,
  clearObj,
  buildFormdata,
}
