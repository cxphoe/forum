<template>
  <div class="topic-editor">
    <input v-model="formData.title" class="title-input" type="text" placeholder="请输入标题"/>
    <div class="pt2">
      <!-- <el-select placeholder="请选择分类"/> -->
    </div>

    <content-editor
      ref="contentInput"
      v-model="formData.content"
      :imgs="imgs"
    />
    <button @click="show">show</button>
  </div>
</template>

<script>
import Vue from 'vue'
import { Select } from 'element-ui'
import ContentEditor from './content_editor'

Vue.use(Select)

export default {
  name: 'TopicEditor',

  components: {
    ContentEditor,
  },

  props: {
    formData: {},
    imgs: {},
  },

  data() {
    return {
    }
  },

  methods: {
    show() {
      console.log(this.formData, this.$refs.contentInput)
    },
  },
}
</script>

<style lang="scss">
.topic-editor {
  display: flex;
  flex-direction: column;

  .title-input {
    border: none !important;
    outline: none;
    font-size: 1.75rem;
    font-weight: 600;
  }

  .formula-bar {
    border-color: #ddd;
    border-style: solid;
    border-width: 1px 0;
    color: $color-gray6;
    display: flex;
    margin: 1rem 0 2rem;
    padding: .25rem;
    width: 100%;

    & > * {
      border-radius: 2px;
      cursor: pointer;
      height: 1.75rem;
      width: 1.75rem;
      position: relative;
      transition: 300ms;

      &:hover {
        background-color: $color-gray1;
      }

      & > * {
        left: 50%;
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
      }
    }
  }

  .content-editor {
    min-height: 300px;
    outline: none;
    padding: 0 0 20rem;

    img {
      width: 100%;
    }
  }
}
</style>
