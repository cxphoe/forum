<template>
  <div class="content-editor">
    <input ref="imgInput" type="file" hidden accept="image/jpeg, image/jpg, image/png" @change="checkImg">
    <div class="formula-bar">
      <div @click="uploadImg">
        <i class="fas fa-images"></i>
      </div>
    </div>
    <div
      ref="input"
      class="content-area"
      contenteditable="true"
      @input="handleInput"
      @focus="getSelect"
      v-html="content"
    ></div>
  </div>
</template>

<script>
import { getFilename } from '@/utils'

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
            data: node.data
          }
        },
        IMG: (node) => {
          return {
            type: 'image',
            data: node.src,
            name: getFilename(this.imgs[node.src].name)
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

  methods: {
    uploadImg(event) {
      this.$refs.imgInput.click()
    },

    checkImg(event) {
      let $input = event.target
      let file = $input.files[0]
      console.log(file)
      if (file) {
        console.log(file)
        let imgUrl = URL.createObjectURL(file)
        console.log(file)
        this.imgs[imgUrl] = {
          name: getFilename(file.name),
          file: file,
        }
        console.log(this.imgs)
        let s = this.lastSelect
        if (s !== null) {
          if (s.nodeName !== 'DIV') {
            s = s.parentNode
          }
          s.insertAdjacentHTML(
            s === this.$el ? 'afterBegin' : 'afterEnd',
            `<img src="${imgUrl}">`
          )
        }
      }
    },

    handleInput(event) {
      let $el = event.target
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
        console.log(s)
      }, 0)
    },
  }
}
</script>

<style lang="scss">
.content-area {
  border: none !important;
  outline: none;
  resize: none;
}
</style>
