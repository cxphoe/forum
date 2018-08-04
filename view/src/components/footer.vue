<template>
  <footer class="footer">
    <div class="social-link">
      <a href="https://github.com/phoeninee">
        <i class="fab fa-github"></i>
      </a>
    </div>
    <div class="copyright">
      Copyright&nbsp;©&nbsp;
      {{ year }}
      &nbsp;Phoenine's bbs
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',

  data() {
    return {
      year: (new Date()).getFullYear(),
    }
  },
}
</script>

<style lang="scss">
.footer {
  padding: 40px 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;

  @media screen and (max-width: 768px) {
    & {
      display: block;
      padding: 32px 8px;

      & > * {
        display: block;
        margin: auto;
        text-align: center;
        & + * {
          margin-top: 8px;
        }
      }
    }
  }

  .social-link a {
    font-size: 28px;
    color: #52aac1;
  }

  .copyright {
    line-height: 14px;
    font-size: 14px;
    color: #aaa;
  }
}
</style>
