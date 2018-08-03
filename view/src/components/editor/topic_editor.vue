<template>
  <div class="topic-editor">
    <input v-model="formData.title" class="title-input" type="text" placeholder="请输入标题"/>
    <div class="pt2">
      分类:&nbsp;
      <el-select v-model="formData.board_id" placeholder="请选择分类">
        <el-option
          v-for="b in boards"
          :key="b.id"
          :label="b.name"
          :value="b.id"
        />
      </el-select>
    </div>

    <content-editor
      ref="contentInput"
      v-if="showContent"
      v-model="formData.content"
      :imgs="imgs"
    />
  </div>
</template>

<script>
import Vue from 'vue'
import { Option, Select } from 'element-ui'
import ContentEditor from './content_editor'

Vue.use(Option)
Vue.use(Select)

export default {
  name: 'TopicEditor',

  components: {
    ContentEditor,
  },

  props: {
    formData: {},
    imgs: {},
    boards: {},
  },

  computed: {
    showContent() {
      return this.formData.content !== undefined
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
}
</style>
