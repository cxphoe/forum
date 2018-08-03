<template>
  <div class="content-editor">
    <input ref="imgInput" type="file" hidden accept="image/jpeg, image/jpg, image/png" @change="checkImg">
    <div class="formula-bar">
      <div @click="uploadImg">
        <i class="fas fa-images"></i>
      </div>
    </div>
    <div class="relative">
      <div
        ref="input"
        class="content-area"
        contenteditable="true"
        @input="handleInput"
        @focus="getSelect"
        v-html="content"
      ></div>
      <div v-if="contentEmpty" class="content-note">请输入正文...</div>
    </div>
  </div>
</template>

<script>
import { baseUrl } from '@/config'

const processPart = {
  text(data) {
    if (data.length === 0) {
      data = '<br>'
    }
    return `<div>${data}</div>`
  },
  img(data) {
    return `<img src=${data}>`
  },
}

const removeBaseUrl = function (url) {
  let sign = baseUrl
  let i = url.indexOf(sign)
  if (i > -1) {
    url = url.substring(i + sign.length)
  }
  console.log('url:', url)
  return url
}

export default {
  name: 'ContentEditor',

  props: {
    value: {},
    imgs: {},
  },

  data() {
    return {
      content: this.processContent(this.value),
      lastSelect: null,

      processNode: {
        '#text'(node) {
          return {
            type: 'text',
            data: node.data,
          }
        },
        IMG: (node) => {
          // 判断这张图片是否在上传文件中，如果没有，说明是文章原有的图片
          // 去掉链接中的 baseUrl，按文本返回
          return node.src in this.imgs
            ? {
              type: 'image',
              data: node.src,
              name: this.imgs[node.src].name,
            }
            : {
              type: 'text',
              data: `<img src="${removeBaseUrl(node.src)}">`,
            }
        },
        BR(node) {
          return {
            type: 'text',
            data: '',
          }
        },
        DIV: (node) => {
          return this.retrieveHtml(node)
        },
      },
    }
  },

  computed: {
    contentEmpty() {
      let parts = this.value
      return parts.length === 0
        || (parts.length === 1 && parts[0].data === '')
    },
  },

  methods: {
    uploadImg(event) {
      this.$refs.imgInput.click()
    },

    isInArea($el) {
      console.log('check $el\n', $el)
      while ($el !== document.body && $el !== this.$refs.input) {
        $el = $el.parentNode
        console.log($el)
      }
      console.log('end check $el')
      return $el === this.$refs.input
    },

    checkImg(event) {
      let $input = event.target
      let file = $input.files[0]
      console.log(file)
      if (file) {
        let imgUrl = URL.createObjectURL(file)
        this.imgs[imgUrl] = {
          name: file.name,
          file: file,
        }
        console.log(this.imgs)
        let s = this.lastSelect
        if (s !== null && this.isInArea(s)) {
          if (s.nodeName !== 'DIV') {
            s = s.parentNode
          }
          s.insertAdjacentHTML(
            s === this.$refs.input ? 'afterBegin' : 'afterEnd',
            `<div><img src="${imgUrl}"></div>`
          )
          this.handleInput()
        }
      }
    },

    handleInput() {
      let $el = this.$refs.input
      this.$emit('input', this.retrieveHtml($el))
      this.getSelect(event)
    },

    processContent(parts) {
      parts = parts.map((p) => {
        let { type, data } = p
        return processPart[type](data)
      })
      return parts.join('')
    },

    retrieveHtml(htmlElement) {
      let parts = []
      for (let child of htmlElement.childNodes) {
        let data = this.processNode[child.nodeName](child)
        // console.log('retrieve:', data)
        if (data instanceof Array) {
          parts.push(...data)
        } else {
          parts.push(data)
        }
      }
      return parts
    },

    getSelect(event) {
      let s = window.getSelection()
      setTimeout(() => {
        this.lastSelect = s.anchorNode
        // this.$emit('update:lastSelect', s.anchorNode)
        // console.log(s)
      }, 0)
    },
  },
}
</script>

<style lang="scss">
.content-editor {
  .content-area {
    min-height: 300px;
    outline: none;
    padding: 0 0 20rem;
    border: none !important;
    height: 100%;
    outline: none;
    resize: none;

    img {
      left: 2.5%;
      margin: 0 auto;
      position: relative;
      width: 95%;
    }
  }

  .content-note {
    color: $color-gray5;
    left: 0;
    position: absolute;
    top: 0;
    user-select: none;
  }
}
</style>
