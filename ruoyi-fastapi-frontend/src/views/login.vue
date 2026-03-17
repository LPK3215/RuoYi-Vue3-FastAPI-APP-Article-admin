<template>
  <div class="login">
    <div class="auth-shell">
      <div class="auth-brand">
        <div class="auth-brand__mark">{{ title }}</div>
        <div class="auth-brand__sub">软件库与教程管理后台</div>
        <div class="auth-brand__chips">
          <el-tag effect="plain" size="large" class="chip">软件看板</el-tag>
          <el-tag effect="plain" size="large" class="chip">批量管理</el-tag>
          <el-tag effect="plain" size="large" class="chip">导入导出</el-tag>
        </div>
        <div class="auth-brand__hint">
          统一维护软件与教程内容：筛选、批量管理、导入导出与发布审核。
        </div>
      </div>

      <el-form
        ref="loginRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <div class="form-head">
          <div class="form-title">登录</div>
          <div class="form-sub">进入 {{ title }} 管理后台</div>
        </div>
      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          type="text"
          size="large"
          auto-complete="off"
          placeholder="账号"
        >
          <template #prefix><svg-icon icon-class="user" class="el-input__icon input-icon" /></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          size="large"
          auto-complete="off"
          placeholder="密码"
          @keyup.enter="handleLogin"
        >
          <template #prefix><svg-icon icon-class="password" class="el-input__icon input-icon" /></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="code" v-if="captchaEnabled">
        <el-input
          v-model="loginForm.code"
          size="large"
          auto-complete="off"
          placeholder="验证码"
          style="width: 63%"
          @keyup.enter="handleLogin"
        >
          <template #prefix><svg-icon icon-class="validCode" class="el-input__icon input-icon" /></template>
        </el-input>
        <div class="login-code">
          <img :src="codeUrl" @click="getCode" class="login-code-img"/>
        </div>
      </el-form-item>
      <el-checkbox v-model="loginForm.rememberMe" style="margin:0px 0px 25px 0px;">记住密码</el-checkbox>
      <el-form-item style="width:100%;">
        <el-button
          :loading="loading"
          size="large"
          type="primary"
          style="width:100%;"
          native-type="submit"
          @click.prevent="handleLogin"
        >
          <span v-if="!loading">登 录</span>
          <span v-else>登 录 中...</span>
        </el-button>
        <div style="float: right;" v-if="register">
          <router-link class="link-type" :to="'/register'">立即注册</router-link>
        </div>
      </el-form-item>
      </el-form>
    </div>
    <!--  底部  -->
    <div class="el-login-footer">
      <span>{{ footerContent }}</span>
    </div>
  </div>
</template>

<script setup>
import { getCodeImg } from "@/api/login";
import Cookies from "js-cookie";
import { encrypt, decrypt } from "@/utils/jsencrypt";
import useUserStore from '@/store/modules/user'
import defaultSettings from '@/settings'
import { APP_TITLE } from '@/config/brand'

const title = APP_TITLE;
const footerContent = defaultSettings.footerContent
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const { proxy } = getCurrentInstance();

const loginForm = ref({
  username: "",
  password: "",
  rememberMe: false,
  code: "",
  uuid: ""
});

const loginRules = {
  username: [{ required: true, trigger: "blur", message: "请输入您的账号" }],
  password: [{ required: true, trigger: "blur", message: "请输入您的密码" }],
  code: [{ required: true, trigger: "change", message: "请输入验证码" }]
};

const codeUrl = ref("");
const loading = ref(false);
// 验证码开关
const captchaEnabled = ref(true);
// 注册开关
const register = ref(false);
const redirect = ref(undefined);

watch(route, (newRoute) => {
    redirect.value = newRoute.query && newRoute.query.redirect;
}, { immediate: true });

function handleLogin() {
  proxy.$refs.loginRef.validate(valid => {
    if (valid) {
      loading.value = true;
      // 勾选了需要记住密码设置在 cookie 中设置记住用户名和密码
      if (loginForm.value.rememberMe) {
        Cookies.set("username", loginForm.value.username, { expires: 30 });
        Cookies.set("password", encrypt(loginForm.value.password), { expires: 30 });
        Cookies.set("rememberMe", loginForm.value.rememberMe, { expires: 30 });
      } else {
        // 否则移除
        Cookies.remove("username");
        Cookies.remove("password");
        Cookies.remove("rememberMe");
      }
      // 调用action的登录方法
      userStore.login(loginForm.value).then(() => {
        const query = route.query;
        const otherQueryParams = Object.keys(query).reduce((acc, cur) => {
          if (cur !== "redirect") {
            acc[cur] = query[cur];
          }
          return acc;
        }, {});
        router.push({ path: redirect.value || "/", query: otherQueryParams });
      }).catch(() => {
        loading.value = false;
        // 重新获取验证码
        if (captchaEnabled.value) {
          getCode();
        }
      });
    }
  });
}

function getCode() {
  getCodeImg().then(res => {
    captchaEnabled.value = res.captchaEnabled === undefined ? true : res.captchaEnabled;
    register.value = res.registerEnabled === undefined ? false : res.registerEnabled;
    if (captchaEnabled.value) {
      codeUrl.value = "data:image/gif;base64," + res.img;
      loginForm.value.uuid = res.uuid;
    }
  });
}

function getCookie() {
  const username = Cookies.get("username");
  const password = Cookies.get("password");
  const rememberMe = Cookies.get("rememberMe");
  loginForm.value = {
    username: username === undefined ? loginForm.value.username : username,
    password: password === undefined ? loginForm.value.password : decrypt(password),
    rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
  };
}

getCode();
getCookie();
</script>

<style lang='scss' scoped>
.login {
  min-height: 100vh;
  padding: 28px 18px 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(900px circle at 14% 16%, rgba(14, 165, 233, 0.22), transparent 55%),
    radial-gradient(860px circle at 84% 22%, rgba(48, 176, 143, 0.18), transparent 55%),
    radial-gradient(900px circle at 44% 86%, rgba(254, 193, 113, 0.16), transparent 60%),
    linear-gradient(180deg, rgba(246, 247, 251, 0.82), rgba(246, 247, 251, 0.92)),
    url("../assets/images/login-background.jpg");
  background-size: cover;
  background-position: center;
}

html.dark .login {
  background:
    radial-gradient(900px circle at 14% 16%, rgba(14, 165, 233, 0.20), transparent 55%),
    radial-gradient(860px circle at 84% 22%, rgba(48, 176, 143, 0.18), transparent 55%),
    radial-gradient(900px circle at 44% 86%, rgba(254, 193, 113, 0.14), transparent 60%),
    linear-gradient(180deg, rgba(7, 10, 16, 0.84), rgba(7, 10, 16, 0.94)),
    url("../assets/images/login-background.jpg");
  background-size: cover;
  background-position: center;
}

.login:before {
  content: "";
  position: absolute;
  inset: -2px;
  pointer-events: none;
  background-image:
    repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.06) 1px, transparent 1px, transparent 3px),
    repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.04) 1px, transparent 1px, transparent 3px);
  opacity: 0.32;
  mix-blend-mode: overlay;
}

.auth-shell {
  width: min(980px, 100%);
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 16px;
  align-items: stretch;
  position: relative;
  z-index: 1;
}

@media (max-width: 920px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }
}

.auth-brand {
  border-radius: 18px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface-2) 70%, transparent);
  box-shadow: var(--app-shadow);
  padding: 20px 18px 18px;
  overflow: hidden;
  position: relative;

  @supports ((-webkit-backdrop-filter: blur(10px)) or (backdrop-filter: blur(10px))) {
    -webkit-backdrop-filter: blur(10px) saturate(1.15);
    backdrop-filter: blur(10px) saturate(1.15);
  }
}

.auth-brand__mark {
  font-size: 22px;
  font-weight: 850;
  letter-spacing: -0.02em;
  color: var(--el-text-color-primary);
}

.auth-brand__sub {
  margin-top: 6px;
  color: var(--el-text-color-secondary);
  font-weight: 600;
}

.auth-brand__chips {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border-radius: 999px;
  font-weight: 650;
}

.auth-brand__hint {
  margin-top: 12px;
  color: var(--el-text-color-regular);
  line-height: 20px;
}

.login-form {
  border-radius: 18px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  box-shadow: var(--app-shadow);
  padding: 18px 18px 6px;
  z-index: 1;

  @supports ((-webkit-backdrop-filter: blur(10px)) or (backdrop-filter: blur(10px))) {
    -webkit-backdrop-filter: blur(10px) saturate(1.15);
    backdrop-filter: blur(10px) saturate(1.15);
  }

  .el-input {
    height: 40px;
    input {
      height: 40px;
    }
  }
  .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 0px;
  }
}

html.dark .login-form {
  background: var(--el-bg-color);
}
.form-head {
  margin-bottom: 14px;
}

.form-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--el-text-color-primary);
}

.form-sub {
  margin-top: 4px;
  color: var(--el-text-color-secondary);
}

.login-tip {
  font-size: 13px;
  text-align: center;
  color: #bfbfbf;
}
.login-code {
  width: 33%;
  height: 40px;
  float: right;
  img {
    cursor: pointer;
    vertical-align: middle;
  }
}
.el-login-footer {
  height: 40px;
  line-height: 40px;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: var(--app-font-sans);
  font-size: 12px;
  letter-spacing: 1px;
  opacity: 0.88;
}
.login-code-img {
  height: 40px;
  padding-left: 12px;
}
</style>

