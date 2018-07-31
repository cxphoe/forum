// https://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,
  parserOptions: {
    parser: 'babel-eslint'
  },
  env: {
    browser: true,
  },
  extends: [
    // https://github.com/vuejs/eslint-plugin-vue#priority-a-essential-error-prevention
    // consider switching to `plugin:vue/strongly-recommended` or `plugin:vue/recommended` for stricter rules.
    'plugin:vue/essential', 
    // https://github.com/standard/standard/blob/master/docs/RULES-en.md
    'standard'
  ],
  // required to lint *.vue files
  plugins: [
    'vue'
  ],
  // add your custom rules here
  rules: {
    // allow async-await
    'generator-star-spacing': 'off',
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    // 函数表达式必须有名字s
    "func-names": [0],
    "new-cap": [2, { newIsCap: true ,capIsNew: true, capIsNewExceptions: ['List', 'Map']}],
    "linebreak-style": [0],
    "brace-style": [2, "1tbs", { "allowSingleLine": false }],
    "camelcase": 2,
    "indent": [2, 2],
    "comma-spacing": [2, {
      "before": false,
      "after": true,
    }],
    "comma-dangle": [0],
    "consistent-this": [1, "that"],
    //函数定义时括号前面要不要有空格
    "space-before-function-paren": [0, "always"],
    "operator-linebreak": [2, "before"],
  }
}
