<template>
  <div id="app">
    <router-view name="nav"/>
    <router-view class="app-main"/>
    <Footer/>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import Footer from '@/components/footer'

export default {
  name: 'App',

  components: {
    Footer,
  },

  methods: mapActions([
    'getCurrentUser'
  ]),

  created() {
    // 在页面创建时请求用户数据
    this.getCurrentUser()
  },
}
</script>

<style lang="scss">
html, body {
  background-color: $color-gray1 !important;
  height: 100%;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $color-text;
  height: 100%;
  position: relative;

  .app-main {
    width: 100%;
    max-width: 1000px;
    margin: 0 auto 6rem;
    padding-top: 4rem;

    @media screen and (max-width: 670px) {
      padding-top: 0;
    }
  }

  *::selection {
    background: #b3d4fc;
    text-shadow: none;
  }
}
</style>
